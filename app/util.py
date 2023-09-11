from datetime import datetime, timedelta
from typing import Dict, Tuple, List
import time
import concurrent.futures
import openai
from app.config import EMBEDDING_MODEL, TOP_N, MAX_LENGTH, GPT_MODEL, ALLOWED_EXTENSIONS, MAIN_TEMP_DIR
import tiktoken
from scipy import spatial
import os
import re
from nltk.tokenize import word_tokenize, sent_tokenize
import pandas as pd
from PyPDF2 import PdfReader
import docx2txt
import requests
import shutil


def check_api_key(api_key: str) -> bool:
    openai.api_key = api_key

    try:
        headers = {
            'Authorization': f'Bearer {api_key}',
        }
        response = requests.get('https://api.openai.com/v1/models', headers=headers)
        if response.status_code == 200:
            return True
    except requests.exceptions.RequestException:
        return False


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def remove_directory(directory_path):
    if not os.path.exists(directory_path):
        print(f"The directory {directory_path} does not exist.")
        return
    shutil.rmtree(directory_path)
    print(f"The directory {directory_path} has been removed.")


def is_stale(path, threshold_minutes=180):
    mtime = datetime.fromtimestamp(os.path.getmtime(path))
    return datetime.utcnow() - mtime > timedelta(minutes=threshold_minutes)


def cleanup_path(path, threshold_minutes=180):
    for root, dirs, files in os.walk(path, topdown=False):  # `topdown=False` ensures we iterate from leaves to root
        for file in files:
            file_path = os.path.join(root, file)
            if is_stale(file_path, threshold_minutes):
                try:
                    os.remove(file_path)
                    print(f"Deleted stale file: {file_path}")
                except (OSError, Exception) as e:
                    print(f"Error deleting file {file_path}: {e}")

        for dir in dirs:
            dir_path = os.path.join(root, dir)
            if is_stale(dir_path, threshold_minutes):
                try:
                    shutil.rmtree(dir_path)
                    print(f"Deleted stale directory: {dir_path}")
                except (OSError, Exception) as e:
                    print(f"Error deleting directory {dir_path}: {e}")


def scheduled_cleanup():
    cleanup_path(MAIN_TEMP_DIR)


def get_first_10_words(text):
    """Retrieve the first 10 words from the text."""
    words = word_tokenize(text)
    return ' '.join(words[:10])


def num_tokens(text: str, model: str = GPT_MODEL) -> int:
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))


def preprocess_text(text):
    # Remove copyright and source information
    text = re.sub(r'©.*?\n', '', text)

    # Remove download instructions
    text = re.sub(r'Download : Download full-size image', '', text)

    # Replace newline characters with space
    text = re.sub(r'\n', ' ', text)

    # Replace multiple spaces with a single space
    text = re.sub(r'\s+', ' ', text)

    return text


def split_text(text, document_title):
    text = preprocess_text(text)
    sentences = sent_tokenize(text)

    sections = []
    current_section = {"title": document_title, "loc": "", "text": "", "tokens": 0}
    current_sentences = []

    for sentence in sentences:
        # Note: I'm assuming a function called `num_tokens` exists that calculates token count
        tokens_count = num_tokens(sentence)

        if current_section["tokens"] + tokens_count > MAX_LENGTH:
            # If adding the next sentence would exceed the max_length,
            # finalize the current section and start a new one.
            current_section["text"] = ' '.join(current_sentences)
            current_section["loc"] = get_first_10_words(current_section["text"])
            sections.append(current_section)
            current_sentences = [sentence]
            current_section = {"title": document_title, "loc": "", "text": "", "tokens": tokens_count}
        else:
            # Otherwise, add the sentence to the current section.
            current_sentences.append(sentence)
            current_section["tokens"] += tokens_count

    # Don't forget to add the last section.
    if current_sentences:
        current_section["text"] = ' '.join(current_sentences)
        current_section["loc"] = get_first_10_words(current_section["text"])
        sections.append(current_section)

    return sections


def extract_text_from_file(filepath):
    """Return the text content of a file based on its extension."""
    ext = os.path.splitext(filepath)[1].lower()

    if ext == ".pdf":
        # Extract text from pdf using PyPDF2
        with open(filepath, 'rb') as file:
            reader = PdfReader(file)
            extracted_text = ""
            for page in reader.pages:
                extracted_text += page.extract_text()

    elif ext == ".txt":
        # Read text from plain text file
        with open(filepath, 'r', encoding="utf-8") as file:
            extracted_text = file.read()

    elif ext == ".docx":
        # Extract text from docx using docx2txt
        extracted_text = docx2txt.process(filepath)

    else:
        # Unsupported file type
        raise ValueError("Unsupported file type: {}".format(ext))

    return extracted_text


def gather_text_sections(folder_path):
    dfs = []
    for filename in os.listdir(folder_path):
        filepath = os.path.join(folder_path, filename)
        if filename.endswith((".txt", ".pdf", ".docx")):
            extracted_text = extract_text_from_file(filepath)
            original_title = os.path.splitext(filename)[0]
            sections = split_text(extracted_text, original_title)
            df = pd.DataFrame(sections)
            dfs.append(df)

    return pd.concat(dfs, ignore_index=True)


def get_embedding(text: str, api_key, model: str = EMBEDDING_MODEL, retry_limit=3, retry_delay=5) -> list[float]:
    openai.api_key = api_key

    for i in range(retry_limit):
        try:
            time.sleep(0.1)  # Wait for a tiny interval of time between each call
            result = openai.Embedding.create(
                model=model,
                input=text
            )
            return result["data"][0]["embedding"]
        except openai.error.RateLimitError:
            print("Rate limit reached. Switching API key...")
            print("New API key set. Waiting for 1 minute...")
            time.sleep(5)
        except openai.error.OpenAIError as e:
            print(f"Error: {e}")
            return None
        print(f"Retrying... (attempt {i + 1})")
        time.sleep(retry_delay)
    return None


def compute_doc_embeddings(df: pd.DataFrame, api_key, batch_size=3, num_workers=6) -> Dict[
    Tuple[str, str], List[float]]:
    api_key = api_key
    embeddings = {}

    def process_batch(batch: pd.DataFrame) -> Dict[Tuple[str, str], List[float]]:
        batch_embeddings = {}
        texts = [r.text for idx, r in batch.iterrows()]
        for j, text in enumerate(texts):
            embedding = get_embedding(text, api_key)
            if embedding is None:
                print("Failed to compute embedding for document with index:", batch.index[j])
            else:
                batch_embeddings[batch.index[j]] = embedding
        return batch_embeddings

    with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
        futures = []
        for i in range(0, len(df), batch_size):
            batch = df.iloc[i:i + batch_size]
            futures.append(executor.submit(process_batch, batch))

        for future in concurrent.futures.as_completed(futures):
            embeddings.update(future.result())

    return embeddings


def add_embeddings_to_df(df, api_key):
    api_key = api_key
    document_embeddings = compute_doc_embeddings(df, api_key)

    df["embeddings"] = document_embeddings
    return df


def strings_ranked_by_relatedness(query: str, df: pd.DataFrame, api_key,
                                  relatedness_fn=lambda x, y: 1 - spatial.distance.cosine(x, y),
                                  top_n: int = TOP_N) -> pd.DataFrame:
    openai.api_key = api_key
    query_embedding_response = openai.Embedding.create(
        model=EMBEDDING_MODEL,
        input=query,
    )
    query_embedding = query_embedding_response["data"][0]["embedding"]

    df['relatedness'] = df['embeddings'].apply(lambda x: relatedness_fn(query_embedding, x))
    sorted_df = df.sort_values(by='relatedness', ascending=False).head(top_n)
    return sorted_df


def process_filenames(filenames: List[str]) -> List[str]:
    """Remove .txt extension from filenames if it's present."""
    return [filename.replace('.txt', '') for filename in filenames]


def query_message(query: str, df: pd.DataFrame, api_key, model: str, token_budget: int, specific_documents=None) -> str:
    df['title'] = df['title'].astype(str)
    if specific_documents:
        specific_documents = process_filenames(specific_documents)
        df_filtered = df[df['title'].isin(specific_documents)]
    else:
        df_filtered = df

    sorted_df = strings_ranked_by_relatedness(query, df_filtered, api_key)
    introduction = 'Use the below textual excerpts to answer the subsequent question. If the answer cannot be found in the provided text, write "I could not find an answer."'
    question = f"\n\nQuestion: {query}"

    message = introduction
    full_message = introduction

    docs_used = []
    for _, row in sorted_df.iterrows():
        doc_info = f'\n\nTitle: {row["title"]}\nLocation: {row["loc"]}'
        next_article = doc_info + f'\nTextual excerpt section:\n"""\n{row["text"]}\n"""'
        if num_tokens(full_message + next_article + question, model=model) <= token_budget:
            message += doc_info
            full_message += next_article
            docs_used.append((row["title"], row["loc"]))
    full_message += question
    return message, full_message, docs_used


def ask(query: str, df: pd.DataFrame, api_key, model: str = GPT_MODEL, specific_documents=None):
    openai.api_key = api_key
    prompt = query
    max_tokens = 7096
    token_budget = max_tokens - num_tokens(prompt, model=model)

    message, full_message, docs_used = query_message(prompt, df, api_key, model=model, token_budget=token_budget,
                                                     specific_documents=specific_documents)

    max_tokens = max_tokens - num_tokens(prompt + full_message, model=model)
    messages = [
        {
            "role": "system",
            "content": f"Given a question, try to answer it using the content of the file extracts below, and if you cannot answer, or find " \
                       f"a relevant file, just output \"I couldn't find the answer to that question in your docs.\".\n\n" \
                       f"If the answer is not contained in the files or if there are no file extracts, respond with \"I couldn't find the answer " \
                       f"to that question in your docs.\" In the cases where you can find the answer, give the answer in markdown format."
        },
        {"role": "user", "content": full_message},
    ]

    response_content = ""
    # This needs to be replaced with the actual streaming call to OpenAI.
    for chunk in openai.ChatCompletion.create(model=model, messages=messages, max_tokens=max_tokens, temperature=.5,
                                              stream=True):
        content = chunk["choices"][0].get("delta", {}).get("content", "")
        if content:
            yield content
    yield "\n\nDocuments used:\n"
    for title, loc in docs_used:
        yield f'Title: {title}\n'

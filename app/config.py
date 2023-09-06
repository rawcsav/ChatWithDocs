import tiktoken
import os

SECRET_KEY = os.urandom(24)
SESSION_TYPE = "filesystem"
SESSION_PERMANENT = True
PERMANENT_SESSION_LIFETIME = 21600
TOKENIZER = tiktoken.get_encoding("cl100k_base")
EMBEDDING_MODEL = "text-embedding-ada-002"
GPT_MODEL = "gpt-4"
MAIN_TEMP_DIR = "app/main_user_directory"
MAX_LENGTH = 300
TOP_N = 5
BATCH_SIZE = 10
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'docx'}

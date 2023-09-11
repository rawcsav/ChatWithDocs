<div align="center">
<h1 align="center">
<img src="https://raw.githubusercontent.com/PKief/vscode-material-icon-theme/ec559a9f6bfd399b82bb44393651661b08aaf7ba/icons/folder-markdown-open.svg" width="100" />
<br>ChatWithDocs
</h1>
<h3>◦ Unlock knowledge, Connect with docs!</h3>
<h3>◦ Developed with the software and tools listed below.</h3>

<p align="center">
<img src="https://img.shields.io/badge/tqdm-FFC107.svg?style&logo=tqdm&logoColor=black" alt="tqdm" />
<img src="https://img.shields.io/badge/SVG-FFB13B.svg?style&logo=SVG&logoColor=black" alt="SVG" />
<img src="https://img.shields.io/badge/JavaScript-F7DF1E.svg?style&logo=JavaScript&logoColor=black" alt="JavaScript" />
<img src="https://img.shields.io/badge/HTML5-E34F26.svg?style&logo=HTML5&logoColor=white" alt="HTML5" />
<img src="https://img.shields.io/badge/Jinja-B41717.svg?style&logo=Jinja&logoColor=white" alt="Jinja" />
<img src="https://img.shields.io/badge/SciPy-8CAAE6.svg?style&logo=SciPy&logoColor=white" alt="SciPy" />

<img src="https://img.shields.io/badge/OpenAI-412991.svg?style&logo=OpenAI&logoColor=white" alt="OpenAI" />
<img src="https://img.shields.io/badge/Python-3776AB.svg?style&logo=Python&logoColor=white" alt="Python" />
<img src="https://img.shields.io/badge/AIOHTTP-2C5BB4.svg?style&logo=AIOHTTP&logoColor=white" alt="AIOHTTP" />
<img src="https://img.shields.io/badge/pandas-150458.svg?style&logo=pandas&logoColor=white" alt="pandas" />
<img src="https://img.shields.io/badge/NumPy-013243.svg?style&logo=NumPy&logoColor=white" alt="NumPy" />
<img src="https://img.shields.io/badge/Flask-000000.svg?style&logo=Flask&logoColor=white" alt="Flask" />
</p>
<img src="https://img.shields.io/github/languages/top/rawcsav/ChatWithDocs?style&color=5D6D7E" alt="GitHub top language" />
<img src="https://img.shields.io/github/languages/code-size/rawcsav/ChatWithDocs?style&color=5D6D7E" alt="GitHub code size in bytes" />
<img src="https://img.shields.io/github/commit-activity/m/rawcsav/ChatWithDocs?style&color=5D6D7E" alt="GitHub commit activity" />
<img src="https://img.shields.io/github/license/rawcsav/ChatWithDocs?style&color=5D6D7E" alt="GitHub license" />
</div>

---

## 📒 Table of Contents
- [📒 Table of Contents](#-table-of-contents)
- [📍 Overview](#-overview)
- [⚙️ Features](#-features)
- [📂 Project Structure](#project-structure)
- [🧩 Modules](#modules)
- [🚀 Getting Started](#-getting-started)

---


## 📍 Overview

This project is a comprehensive text analysis tool that provides functionalities such as text processing, document embedding, text retrieval, and ranking. The purpose of this tool is to enable users to upload and analyze text documents, extract relevant information, and generate responses to user queries using the OpenAI API. Its value proposition lies in its ability to simplify complex text analysis tasks and provide a foundation for building applications for natural language processing.

---

## ⚙️ Features

| Feature                | Description                           |
| ---------------------- | ------------------------------------- |
| **⚙️ Architecture**     | The system follows a modular architecture with a Flask web application as the core. Flask Blueprints are used to separate concerns such as authentication and handling different routes. It follows a client-server architecture for handling user interactions. The codebase is well-organized and follows best practices. |
| **📖 Documentation**   | The codebase has comprehensive and well-documented code. Each file in the repository has a summary explaining its purpose and functionality. Additionally, the code contains inline comments explaining complex logic. |
| **🔗 Dependencies**    | The system relies on Flask, a web framework, and other commonly used Python libraries for various functionalities. Specifically, OpenAI API is used for tasks related to text analysis. |
| **🧩 Modularity**      | The codebase is highly modular, making it easy to understand, maintain, and extend. The functionalities are divided into separate files and functions, promoting code reusability and separation of concerns. The modular structure allows for independent development and testing of components. |
| **✔️ Testing**          | The codebase lacks specific information about testing strategies and tools. However, as it is a Flask application, it is possible to implement tests using frameworks like pytest or Flask's built-in testing tools. Proper test coverage and automated testing infrastructure could improve reliability and maintainability. |
| **⚡️ Performance**      | As the codebase largely interacts with external APIs for text processing tasks, its performance depends on the response times of these APIs. However, the codebase appears to be efficient, leveraging appropriate libraries for tasks like file manipulation and text processing. Proper caching and optimization techniques could further enhance performance. |
| **🔐 Security**        | The codebase includes security measures such as session management, token encoding, and route-specific authentication using Flask Blueprints. Although further analysis is required, the basic security measures appear to protect data and maintain functionality. Proper handling of user input and careful consideration of security best practices would enhance security further. |
| **🔀 Version Control** | The codebase is version controlled using Git. The presence of a public GitHub repository allows for easy collaboration, tracking of changes, and maintaining a well-documented history of the project. Proper branching and code review processes would facilitate collaboration and improve code quality. |
| **🔌 Integrations**    | The system integrates with external services such as the OpenAI API for text analysis. It interacts with these services using appropriate wrappers and libraries, ensuring seamless integration and leveraging the functionalities provided by these services. |
| **📶 Scalability**     | The system's scalability is not evident from the codebase alone. To assess scalability, factors like the number of concurrent users, the scalability of external APIs, and potential bottlenecks in terms of data processing need to be considered. Proper load testing, monitoring, and optimization can help ensure the system can handle growth in users and data. |

---


## 📂 Project Structure




---

## 🧩 Modules

<details closed><summary>Root</summary>

| File                                                               | Summary                                                                                                                                                                                                                                                                           |
| ---                                                                | ---                                                                                                                                                                                                                                                                               |
| [run.py](https://github.com/rawcsav/ChatWithDocs/blob/main/run.py) | This code initializes and runs a Flask application with debugging mode enabled on port 8080. The create_app function is responsible for creating and configuring the app object. When the code is run as the main script, the application starts listening for incoming requests. |

</details>

<details closed><summary>App</summary>

| File                                                                         | Summary                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| ---                                                                          | ---                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| [config.py](https://github.com/rawcsav/ChatWithDocs/blob/main/app/config.py) | This Python code sets various configurations for a web application, including session management, token encoding, models, directory paths, and file restrictions.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| [util.py](https://github.com/rawcsav/ChatWithDocs/blob/main/app/util.py)     | The code provides various functionalities that are used in the context of processing and analyzing text data. Here's a summary of the core functionalities:1. API Key Validation:-`check_api_key`: Checks if an API key is valid by querying the OpenAI API.2. File Manipulation:-`allowed_file`: Checks if a file has an allowed extension based on a list of allowed extensions.-`remove_directory`: Removes a directory and all its contents.-`is_stale`: Checks if a file or directory is stale based on its modification timestamp.-`cleanup_path`: Recursively deletes stale files and directories within a given directory.-`scheduled_cleanup`: Calls `cleanup_path` with a default directory path for scheduled cleanup.3. Text Processing:-`get_first_10_words`: Retrieves the first 10 words from a text.-`num_tokens`: Calculates the number of tokens in a text using a specified language model.-`preprocess_text`: Preprocesses a text by removing specific patterns and formatting.-`split_text`: Splits a text into sections based on a maximum length and token count.4. Text Extraction:-`extract_text_from_file`: Extracts the text content of a file based on its file extension.-`gather_text_sections`: Gathers text sections from files within a specified folder path.5. Document Embedding:-`get_embedding`: Calculates the embedding vector for a given text using the OpenAI Embedding API.-`compute_doc_embeddings`: Calculates document embeddings for a DataFrame of text sections using the OpenAI Embedding API.-`add_embeddings_to_df`: Adds the document embeddings to a DataFrame containing text sections.6. Text Retrieval and Ranking:-`strings_ranked_by_relatedness`: Ranks text sections in a DataFrame based on their relatedness to a query text.-`process_filenames`: Removes the `.txt` extension from filenames.-`query_message`: Generates a query message for a given query and DataFrame of text sections based on relatedness scoring.-`ask`: Initiates a chat conversation with the GPT API and retrieves responses based on the query and document sections.These functionalities provide a comprehensive set of tools for manipulating text files, extracting relevant text sections from files, calculating document embeddings, and ranking sections based on relatedness to a query. The code is a valuable foundation for building text analysis applications and addressing various natural language processing tasks. |

</details>

<details closed><summary>Templates</summary>

| File                                                                                     | Summary                                                                                                                                                                                                                                             |
| ---                                                                                      | ---                                                                                                                                                                                                                                                 |
| [index.html](https://github.com/rawcsav/ChatWithDocs/blob/main/app/templates/index.html) | This HTML code creates a web interface for users to upload text documents, set their OpenAI API key, ask questions about the documents, and receive answers from the OpenAI API. It also provides instructions and displays the uploaded documents. |

</details>

<details closed><summary>Routes</summary>

| File                                                                                      | Summary                                                                                                                                                                                                                                                                                                                            |
| ---                                                                                       | ---                                                                                                                                                                                                                                                                                                                                |
| [auth.py](https://github.com/rawcsav/ChatWithDocs/blob/main/app/routes/auth.py)           | This code defines a Flask Blueprint for authentication. It includes a route for setting an API key and a before_request function to set the API key globally. The API key is stored in the session and used for OpenAI requests.                                                                                                   |
| [query.py](https://github.com/rawcsav/ChatWithDocs/blob/main/app/routes/query.py)         | This code defines a Flask endpoint that handles a POST request containing a query and selected documents. It reads a JSON file, performs a search using the query and selected documents, and streams the results back as a text/plain response.                                                                                   |
| [documents.py](https://github.com/rawcsav/ChatWithDocs/blob/main/app/routes/documents.py) | The code allows users to upload documents, convert them to text, and generate embeddings using an API key. The files are saved and processed in a thread-safe manner, and the resulting embeddings are saved to a JSON file for later use. Additionally, the code includes error handling and validation for file types and sizes. |

</details>

---

## 🚀 Getting Started


### 📦 Installation

1. Clone the ChatWithDocs repository:
```sh
git clone https://github.com/rawcsav/ChatWithDocs
```

2. Change to the project directory:
```sh
cd ChatWithDocs
```

3. Install the dependencies:
```sh
pip install -r requirements.txt
```

### 🎮 Using ChatWithDocs

```sh
python run.py
```

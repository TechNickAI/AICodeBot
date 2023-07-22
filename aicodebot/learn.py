from aicodebot.config import get_local_data_dir
from aicodebot.helpers import logger
from git import Repo
from langchain.document_loaders import GitLoader, NotebookLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter, Language, RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from pathlib import Path

DEFAULT_EXCLUDE = [".csv", ".enex", ".json", ".jsonl"]


def load_documents_from_repo(repo_dir, exclude=DEFAULT_EXCLUDE):
    """Load a repo into the vector store."""

    repo = Repo(repo_dir)
    assert not repo.bare, f"Repo {repo_dir} does not appear to be a valid git repository"

    # Check main first, then master, then give up
    for branch in ["main", "master"]:
        if branch in repo.heads:
            default_branch = branch
            break
    else:
        raise ValueError(f"Repo {repo_dir} does not have a main or master branch")

    loader = GitLoader(repo_path=repo_dir, branch=default_branch)

    documents = loader.load()
    logger.info(f"Loaded {len(documents)} documents from {repo_dir}")

    # Clean up
    cleaned = []
    logger.info("Cleaning up documents")
    for document in documents:
        content = document.page_content
        if not content:
            logger.debug(f"Skipping empty file {document.metadata['file_path']}")
            continue

        file_type = document.metadata["file_type"].lower()
        if file_type in exclude:
            logger.debug(f"Skipping excluded file {document.metadata['file_path']}")
            continue

        # Reload notebooks
        if file_type == ".ipynb":
            logger.debug(f"Reloading notebook {document.metadata['file_path']}")
            new_document = NotebookLoader(repo_dir / document.metadata["file_path"]).load()[0]
            # Use the original metadata, because it contains file_type
            new_document.metadata = document.metadata
            cleaned.append(new_document)
        else:
            cleaned.append(document)

    return cleaned


def store_documents(documents, vector_store_dir):
    """Store documents in the vector store."""
    vector_store_file = Path(vector_store_dir / "faiss_index")
    embeddings = OpenAIEmbeddings()
    if Path(vector_store_file).exists():
        logger.info(f"Loading existing vector store {vector_store_file}")
        return FAISS.load_local(vector_store_file, embeddings)

    logger.info(f"Creating new vector store {vector_store_file}")

    language_extension_map = {
        ".py": Language.PYTHON,
        ".ipynb": Language.PYTHON,
        ".js": Language.JS,
        ".ts": Language.JS,
        ".html": Language.HTML,
        ".md": Language.MARKDOWN,
        ".mdx": Language.MARKDOWN,
        ".go": Language.GO,
        ".java": Language.JAVA,
        ".c": Language.CPP,
        ".cpp": Language.CPP,
        ".php": Language.PHP,
        ".rb": Language.RUBY,
        ".xml": Language.HTML,
    }

    files = 0
    chunks = []
    for document in documents:
        file_type = document.metadata["file_type"].lower()
        files += 1

        # Clean up
        # Remove magic text that breaks processing
        content = document.page_content.replace("<|end" + "of" + "text|>", "")  # noqa: ISC003

        if file_type in language_extension_map:
            # Use a recursive splitter for code files
            logger.debug(
                f"Processing {document.metadata['file_path']} as {language_extension_map[file_type].value} code"
            )
            splitter = RecursiveCharacterTextSplitter.from_language(
                language=language_extension_map[document.metadata["file_type"].lower()],
                chunk_size=50,
                chunk_overlap=0,
            )
        else:
            # TODO: Check if it's a text file
            if file_type not in [".txt", ".md", ".yml", ".yaml"]:
                logger.info(f"Processing {document.metadata['file_path']} as a text file")
            splitter = CharacterTextSplitter(separator="\n", chunk_size=1_000, chunk_overlap=200)

        chunks += splitter.create_documents([content])

    logger.info(f"Storing {len(chunks)} chunks from {files} files in {vector_store_dir}")
    vector_store = FAISS.from_documents(chunks, embeddings)
    vector_store.save_local(vector_store_file)
    return vector_store


def load_learned_repo(repo_name):
    """Load a vector store from a learned repo."""
    vector_store_file = Path(get_local_data_dir() / "vector_stores" / repo_name / "faiss_index")
    if not vector_store_file.exists():
        raise ValueError(
            f"Vector store for {repo_name} does not exist. Please run `aicodebot learn $githuburl` first."
        )

    embeddings = OpenAIEmbeddings()
    return FAISS.load_local(vector_store_file, embeddings)

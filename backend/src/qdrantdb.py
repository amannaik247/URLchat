import os
from langchain_community.vectorstores import Qdrant
from qdrant_client import QdrantClient, models
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings

from dotenv import load_dotenv

load_dotenv(override=True)

qdrant_api_key = os.getenv("QDRANT_API_KEY")
qdrant_url = os.getenv("QDRANT_URL")
collection_name = "Websites"
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")


client = QdrantClient(url=qdrant_url, api_key=qdrant_api_key)


vector_store = Qdrant(
    client=client,
    collection_name=collection_name,
    embeddings=GoogleGenerativeAIEmbeddings(model="models/embedding-001"),
)

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000, chunk_overlap=20, length_function=len
)


def create_collection(collection_name):
    client.create_collection(
        collection_name=collection_name,
        vectors_config=models.VectorParams(size=768, distance=models.Distance.COSINE),
    )
    print(f"Collection {collection_name} created successfully")


def upload_website_to_collection(url: str):
    if not client.collection_exists(collection_name=collection_name):
        create_collection(collection_name)

    loader = WebBaseLoader(url)
    docs = loader.load_and_split(text_splitter)
    for doc in docs:
        doc.metadata = {"source_url": url}

    vector_store.add_documents(docs)
    return f"Successfully uploaded {len(docs)} documents to collection {collection_name} from {url}"


# create_collection(collection_name)
# upload_website_to_collection("https://hamel.dev/blog/posts/evals/")

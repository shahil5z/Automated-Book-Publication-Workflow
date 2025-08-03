import chromadb
from dotenv import load_dotenv
import os
import base64

load_dotenv()
client = chromadb.PersistentClient(path=os.getenv("CHROMA_DB_PATH"))

def store_version(content, version, content_type, screenshot_path=None):
    collection = client.get_or_create_collection(name="book_versions")

    # Encode the screenshot as base64 if available
    screenshot_data = None
    if screenshot_path and os.path.exists(screenshot_path):
        with open(screenshot_path, "rb") as image_file:
            screenshot_data = base64.b64encode(image_file.read()).decode('utf-8')

    # Ensure metadata fields are strings or appropriately handled
    metadata = {
        "version": str(version),  # Ensure version is a string
        "type": content_type or "",  # Provide a default empty string if content_type is None
        "screenshot": screenshot_data if screenshot_data else ""  # Provide a default empty string if no screenshot data
    }

    collection.add(
        documents=[content],
        metadatas=[metadata],
        ids=[str(version)]
    )

def search_versions(query):
    collection = client.get_collection(name="book_versions")
    # Perform a keyword search in the documents
    results = collection.query(query_texts=[query], n_results=5)
    return [
        {
            "version": results["metadatas"][0][i]["version"],
            "type": results["metadatas"][0][i]["type"],
            "content": results["documents"][0][i][:200] + "...",  # Display a snippet
            "screenshot": results["metadatas"][0][i].get("screenshot", "")
        }
        for i in range(len(results["documents"][0]))
    ]
import os
from flask import request, jsonify
from dotenv import load_dotenv
from langchain_mistralai import MistralAIEmbeddings
from langchain_community.vectorstores.upstash import UpstashVectorStore
from langchain_core.documents import Document

load_dotenv()
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
UPSTASH_VECTOR_REST_URL = os.getenv("UPSTASH_VECTOR_REST_URL")
UPSTASH_VECTOR_REST_TOKEN = os.getenv("UPSTASH_VECTOR_REST_TOKEN")

# create embeddings and insert into vector store
def embed_service():
    try:
        data = request.get_json()
        text = data["c_message"]
        c_id = data["c_id"]
        
        embeddings = MistralAIEmbeddings(
            model="mistral-embed",
        )

        # Store the c_id in the metadata for later retrieval
        documents = [Document(page_content=text, metadata={"c_id": c_id})]

        store = UpstashVectorStore(
            embedding=embeddings
        )

        store.add_documents(documents)

        return jsonify({"message": "Successfully inserted vectors"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400

# query vector store and return index for similar complaints
def query_service():
    try:
        data = request.get_json()
        query_text = data["c_message"]

        embeddings = MistralAIEmbeddings(
            model="mistral-embed",
        )

        store = UpstashVectorStore(
            embedding=embeddings
        )

        results = store.similarity_search(query_text, k=5)

        # Extract c_ids from the metadata of similar documents
        similar_complaints = []
        for doc in results:
            if "c_id" in doc.metadata:
                similar_complaints.append({
                    "c_id": doc.metadata["c_id"],
                    "content_preview": doc.page_content[:100] + "..." if len(doc.page_content) > 100 else doc.page_content
                })

        return jsonify({"similar_complaints": similar_complaints}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400

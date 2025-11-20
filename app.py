# app.py
import os
from flask import Flask, request, jsonify
from whoosh.index import open_dir
from whoosh.qparser import QueryParser

# Ensure index is downloaded at startup
if not os.path.exists("index"):
    print("Index not found locally, attempting download...")
    import download_index
    # download_index will exit on failure

# open whoosh index
ix = open_dir("index")

app = Flask(__name__)

@app.get("/")
def home():
    return "Yaadi OCR Search API is running"

@app.get("/search")
def search():
    q = request.args.get("q", "")
    if not q:
        return jsonify({"error":"missing q parameter"}), 400

    results = []
    with ix.searcher() as s:
        parser = QueryParser("content", ix.schema)
        query = parser.parse(q)
        hits = s.search(query, limit=100)
        for h in hits:
            results.append({
                "file": h['file'],
                "page": h['page'],
                "text": (h['content'][:400] + "...") if len(h['content'])>400 else h['content']
            })
    return jsonify(results)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

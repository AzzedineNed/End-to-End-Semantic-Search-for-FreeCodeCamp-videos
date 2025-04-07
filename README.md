---
# 🎯 End-to-End Semantic Search for freeCodeCamp Videos

Semantic search system to explore freeCodeCamp YouTube content using vector similarity and sentence embeddings. Built for educational search via natural language queries.

---

## 📌 Features

- 🔍 **Semantic Search** over freeCodeCamp videos using sentence-transformers.
- ⚙️ **ETL Pipeline** for fetching, processing, and embedding YouTube video data.
- 🚀 **FastAPI Backend**, containerized with Docker and deployed on **Google Cloud Run**.
- 🌐 **Gradio UI** hosted on **Hugging Face Spaces**, secured with Identity Token.
- ☁️ **CI/CD** using GitHub Actions & **Google Cloud Build** for auto-deployments.

---

## 🏗️ System Architecture

![System Architecture](https://github.com/AzzedineNed/End-to-End-Semantic-Search-for-FreeCodeCamp-videos/blob/main/end-to-end-semantic-search-for-freecodecamp-videos.png)

---

## 🧪 Semantic Search Logic

The search engine uses [all-MiniLM-L6-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2) to generate sentence embeddings. Queries are compared using **Manhattan distance** (L1 norm), retrieving the closest matches from the index.

- Embeddings stored in `video-index.parquet`.
- Results sorted by **lowest Manhattan distance** to the query embedding.

---

## 📂 Directory Structure

```
azzedinened-end-to-end-semantic-search-for-freecodecamp-videos/
├── README.md
├── Dockerfile
├── requirements.txt
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── search_function.py
│   └── data/
│       ├── README.md
│       ├── video-descriptions.parquet
│       ├── video-ids.parquet
│       └── video-index.parquet
├── data_pipeline/
│   ├── Data_Pipeline.py
│   ├── ETL.py
│   └── requirements.txt
└── .github/
    └── workflows/
        └── data-pipeline.yml
```

---

## 🔄 Data Pipeline

Automated via GitHub Actions:

- ⏰ Runs every **Saturday at 4:00 AM** or on manual trigger.
- 📥 Fetches latest videos using YouTube API v3.
- 🧹 Cleans and transforms video metadata.
- 🧠 Embeds using `sentence-transformers`.
- 💾 Saves processed `.parquet` files to `app/data/`.

---

## 🚀 Deployment

- **Backend:** FastAPI app in Docker.
- **Port:** `8080`
- **Hosting:** Google Cloud Run with Cloud Build CI/CD.
- **Trigger:** Any push to the repo (including data pipeline updates).

> The Docker container only includes the `app/` directory.

---

## 🌐 Interface

- Built with [Gradio](https://gradio.app/).
- Hosted on [Hugging Face Spaces](https://huggingface.co/spaces/Azzedine01/End-to-End-Semantic-Search-for-FreeCodeCamp-videos).
- Access is secured via an **Identity Token**.

---

## 🐳 Docker

### Build the container

```bash
docker build -t semantic-search-app .
```

### Run locally

```bash
docker run -p 8080:8080 semantic-search-app
```

---

## 🔧 Local Development

### Run the FastAPI backend

```bash
cd app
uvicorn main:app --host 0.0.0.0 --port 8080
```

### Run the ETL pipeline

```bash
cd data_pipeline
python Data_Pipeline.py
```

---

## 🧪 Test the API

Once the app is running on `localhost:8080`, you can test it with:

```bash
curl -X POST "http://localhost:8080/search" \
     -H "Content-Type: application/json" \
     -d '{"query": "how to learn python"}'
```

---

## ✨ Credits

Embeddings via [Sentence Transformers](https://www.sbert.net/)  
Data from [freeCodeCamp YouTube Channel](https://www.youtube.com/c/Freecodecamp)

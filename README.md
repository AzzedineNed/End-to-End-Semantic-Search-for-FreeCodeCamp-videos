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

- ⏰ Runs every **Saturday at 4:00 AM** or manually on-demand.
- 📥 Fetches latest videos using the YouTube API v3.
- 🧹 Cleans and transforms video metadata.
- 🧠 Embeds using `sentence-transformers`.
- 💾 Saves `.parquet` files to `app/data/`.

> Note: Only the `app/` directory is included in the final Docker image.

---

## 🔐 Secrets & Configuration

To securely run the data pipeline via GitHub Actions, set the following repository secrets:

| Secret Name            | Description                                          |
|------------------------|------------------------------------------------------|
| `YT_API_KEY`           | YouTube Data API v3 key from your Google Console     |
| `PERSONAL_ACCESS_TOKEN`| GitHub Personal Access Token (for workflow commits)  |

- 🔒 Secrets keep credentials out of source code.
- ✅ Ensures smooth, authenticated pipeline execution.

➡️ **Setup via:** GitHub → `Settings` → `Secrets and variables` → `Actions`

---

## 🚀 Deployment

- **Backend:** FastAPI app containerized with Docker.
- **Port:** `8080`
- **Hosted on:** Google Cloud Run.
- **CI/CD:** Google Cloud Build + GitHub Actions trigger deployments on push.

---

## 🌐 Interface

- Built using [Gradio](https://gradio.app/).
- Hosted on [Hugging Face Spaces](https://huggingface.co/spaces/Azzedine01/End-to-End-Semantic-Search-for-FreeCodeCamp-videos).
- Secured with an **Identity Token** for controlled access.

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

Once the app is running on `localhost:8080`, test the endpoint using:

```bash
curl -X POST "http://localhost:8080/search" \
     -H "Content-Type: application/json" \
     -d '{"query": "how to learn python"}'
```

---

## ✨ Credits

- Embeddings via [Sentence Transformers](https://www.sbert.net/)
- Video content from [freeCodeCamp YouTube Channel](https://www.youtube.com/c/Freecodecamp)

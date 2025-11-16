# Single-Cell Atlas Builder

[![Python](https://img.shields.io/badge/python-3.10+-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Build Status](https://img.shields.io/badge/build-passing-brightgreen)](#)

**Single-Cell Atlas Builder** is an open-source platform for building, analyzing, and visualizing single-cell RNA-seq atlases.  
It integrates widely used single-cell analysis tools (Scanpy, CellTypist, pySCENIC) with a FastAPI backend, SQLAlchemy-managed database, and an optional Streamlit frontend for interactive visualization. LLaMA 3 is used for cluster/pathway summarization.

---

## System Architecture

```

───────────────────────────────┐
│           Client UI          │
│ (Streamlit / Dash / Swagger) │
└──────────────┬───────────────┘
│ REST API
┌──────────────▼───────────────┐
│         FastAPI Server       │
│   /upload  /integrate  /visualize  │
└──────────────┬───────────────┘
│ SQLAlchemy ORM
┌──────────────▼───────────────┐
│     PostgreSQL / SQLite      │
└──────────────┬───────────────┘
│
┌──────────────▼───────────────┐
│  Analysis Engine (Scanpy,    │
│  CellTypist, LLaMA 3, pySCENIC) │
└───────────────────────────────┘

```

---

## Features

* **Upload & Manage Datasets:** Supports `.h5ad`, `.csv`, `.mtx` formats.
* **Preprocessing:** QC, filtering, normalization, PCA, UMAP.
* **Clustering & Annotation:** Leiden clustering and optional CellTypist integration.
* **Integration:** Merge multiple datasets into a unified atlas.
* **Interactive Visualization:** Streamlit-based UMAP and gene expression plots.
* **LLM Summarization:** Optional cluster/pathway summaries using LLaMA 3.
* **Reproducible Deployment:** Docker-ready for local or cloud deployment.

---

## Screenshots

![UMAP Example](https://via.placeholder.com/600x400?text=UMAP+Plot+Example)
*Streamlit UMAP visualization example*

---

## Repository Structure

```

scatlas-builder/
├── app/
│   ├── main.py             # FastAPI entrypoint
│   ├── routers/            # API endpoints: upload, integrate, visualize
│   ├── services/           # Processing and clustering functions
│   ├── schemas.py          # Pydantic models
│   ├── tables.py           # SQLAlchemy ORM models
│   ├── database.py         # Database connection
│   ├── utils/              # File and helper utilities
│   └── ui/                 # Streamlit application
├── uploads/                # Uploaded datasets
├── docker/                 # Dockerfile
├── requirements.txt
└── README.md

````

---

## Installation

### Prerequisites

* Python 3.9+
* Conda recommended for scientific packages
* SQLite (default) or PostgreSQL

### Setup

```bash
git clone https://github.com/yourusername/scatlas-builder.git
cd scatlas-builder
pip install -r requirements.txt
````

### Running Locally

```bash
uvicorn app.main:app --reload
```

* API docs: `http://127.0.0.1:8000/docs`
* Streamlit UI: `streamlit run app/ui/streamlit_app.py`

### Running via Docker

```bash
docker build -t scatlas-builder .
docker run -p 8000:8000 scatlas-builder
```

---

## API Endpoints

| Endpoint                       | Method | Description                                             |
| ------------------------------ | ------ | ------------------------------------------------------- |
| `/upload`                      | POST   | Upload a dataset with metadata                          |
| `/integrate/run/{dataset_id}`  | POST   | Run preprocessing, clustering, and integration pipeline |
| `/visualize/umap/{dataset_id}` | GET    | Generate UMAP plot of processed dataset                 |

---

## Example Workflow

```python
from app.services import preprocessing, clustering, llm_summary
import scanpy as sc

# Load dataset
adata = preprocessing.load_input("uploads/sample.h5ad")

# Preprocessing
adata = preprocessing.run_qc_and_normalize(adata)
adata = preprocessing.run_pca_umap(adata)

# Clustering
adata = clustering.run_leiden(adata)

# Plot UMAP
sc.pl.umap(adata, color='leiden')

# Optional LLaMA 3 summarization
markers = {'0': ['GeneA', 'GeneB'], '1': ['GeneC', 'GeneD']}
summary = llm_summary.summarize_cluster_markers(markers)
print(summary)
```

---

## Roadmap

* [ ] Add CellTypist integration for automatic cell-type annotation
* [ ] LLaMA 3-based cluster/pathway summarization
* [ ] Celery + Redis for background processing of large datasets
* [ ] Streamlit dashboard enhancements for interactive exploration
* [ ] Multi-dataset integration (Harmony, scVI)

---

## Citation

If you use this project, please cite:

```
Manish Kumar, Single-Cell Atlas Builder, 2025.  
GitHub: https://github.com/man4ish/scatlas-builder


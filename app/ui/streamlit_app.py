"""
Single-Cell Atlas Builder - Streamlit Viewer

This module provides a Streamlit-based frontend to interact with the Single-Cell Atlas Builder backend.
Users can:
1. Upload single-cell datasets (.h5ad, .csv)
2. Trigger preprocessing, QC, normalization, PCA, UMAP, and clustering pipelines
3. Visualize processed UMAP embeddings

Dependencies:
- streamlit
- requests
- base64
"""

import streamlit as st
import requests
import base64

# Base API URL, defaulting to localhost or set via Streamlit secrets
API_URL = st.secrets.get("API_URL", "http://127.0.0.1:8000")

# App title
st.title("Single-Cell Atlas Builder - Viewer")

# Sidebar navigation for selecting actions
st.sidebar.header("Actions")
action = st.sidebar.selectbox("Action", ["Upload", "Process", "View UMAP"])


def upload_dataset():
    """
    Handle dataset upload through Streamlit UI and send it to FastAPI backend.

    - Validates file type (.h5ad or .csv)
    - Requires dataset name
    - Optional metadata
    - Sends POST request to /upload endpoint
    """
    st.header("Upload dataset")
    uploaded = st.file_uploader("Choose a .h5ad or .csv file", type=["h5ad", "csv"])
    name = st.text_input("Dataset name")
    metadata = st.text_area("Metadata (optional)")

    if st.button("Upload"):
        if uploaded and name:
            # Prepare files and form data for POST request
            files = {"file": (uploaded.name, uploaded.getvalue())}
            data = {"name": name, "metadata": metadata}

            # Send upload request to backend
            resp = requests.post(f"{API_URL}/upload/", files=files, data=data)
            st.write(resp.json())
        else:
            st.error("Provide a file and a name")


def process_dataset():
    """
    Trigger background preprocessing and integration pipeline for a dataset.

    - User inputs Dataset ID
    - Sends POST request to /integrate/run/{dataset_id} endpoint
    - Pipeline runs asynchronously in the backend
    """
    st.header("Start processing")
    ds_id = st.number_input("Dataset ID", min_value=1, step=1)

    if st.button("Start"):
        resp = requests.post(f"{API_URL}/integrate/run/{int(ds_id)}")
        st.write(resp.json())


def view_umap():
    """
    Display UMAP plot for a processed dataset.

    - User inputs Dataset ID
    - Sends GET request to /visualize/umap/{dataset_id} endpoint
    - Receives base64-encoded PNG image and renders it in Streamlit
    """
    st.header("View UMAP")
    ds_id = st.number_input("Dataset ID to view", min_value=1, step=1, key="view")

    if st.button("Show UMAP"):
        resp = requests.get(f"{API_URL}/visualize/umap/{int(ds_id)}")
        if resp.status_code == 200 and "image_base64" in resp.json():
            img_b64 = resp.json()["image_base64"]
            st.image(base64.b64decode(img_b64))
        else:
            st.error(f"Failed to get UMAP: {resp.text}")


# Map actions to functions
if action == "Upload":
    upload_dataset()
elif action == "Process":
    process_dataset()
elif action == "View UMAP":
    view_umap()

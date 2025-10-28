import streamlit as st
import requests
import base64

API_URL = st.secrets.get("API_URL", "http://127.0.0.1:8000")

st.title("Single-Cell Atlas Builder - Viewer")

st.sidebar.header("Actions")
action = st.sidebar.selectbox("Action", ["Upload", "Process", "View UMAP"])

if action == "Upload":
    st.header("Upload dataset")
    uploaded = st.file_uploader("Choose a .h5ad or .csv file", type=["h5ad", "csv"])
    name = st.text_input("Dataset name")
    metadata = st.text_area("Metadata (optional)")
    if st.button("Upload"):
        if uploaded and name:
            files = {"file": (uploaded.name, uploaded.getvalue())}
            data = {"name": name, "metadata": metadata}
            resp = requests.post(f"{API_URL}/upload/", files=files, data=data)
            st.write(resp.json())
        else:
            st.error("Provide a file and a name")

if action == "Process":
    st.header("Start processing")
    ds_id = st.number_input("Dataset ID", min_value=1, step=1)
    if st.button("Start"):
        resp = requests.post(f"{API_URL}/integrate/run/{int(ds_id)}")
        st.write(resp.json())

if action == "View UMAP":
    st.header("View UMAP")
    ds_id = st.number_input("Dataset ID to view", min_value=1, step=1, key="view")
    if st.button("Show UMAP"):
        resp = requests.get(f"{API_URL}/visualize/umap/{int(ds_id)}")
        if resp.status_code == 200 and "image_base64" in resp.json():
            img_b64 = resp.json()["image_base64"]
            st.image(base64.b64decode(img_b64))
        else:
            st.error(f"Failed to get UMAP: {resp.text}")

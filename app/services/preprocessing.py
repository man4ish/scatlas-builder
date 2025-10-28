import scanpy as sc
import anndata
import os

def load_input(path: str):
    ext = path.split(".")[-1].lower()
    if ext == "h5ad":
        adata = sc.read_h5ad(path)
    elif ext == "csv":
        import pandas as pd
        df = pd.read_csv(path, index_col=0)
        adata = anndata.AnnData(df)
    else:
        raise ValueError("Unsupported format in load_input")
    return adata

def run_qc_and_normalize(adata):
    sc.pp.filter_cells(adata, min_genes=200)
    sc.pp.filter_genes(adata, min_cells=3)
    adata.var['mt'] = adata.var_names.str.startswith('MT-')  # human mitochondrial
    sc.pp.calculate_qc_metrics(adata, qc_vars=['mt'], percent_top=None, log1p=False, inplace=True)
    sc.pp.normalize_total(adata, target_sum=1e4)
    sc.pp.log1p(adata)
    return adata

def run_pca_umap(adata, n_pcs=50):
    sc.pp.highly_variable_genes(adata, n_top_genes=2000, subset=True)
    sc.tl.pca(adata, svd_solver='arpack', n_comps=n_pcs)
    sc.pp.neighbors(adata, n_pcs=min(n_pcs, adata.obsm['X_pca'].shape[1]))
    sc.tl.umap(adata)
    return adata

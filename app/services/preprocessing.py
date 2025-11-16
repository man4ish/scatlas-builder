"""
preprocessing.py

Single-Cell RNA-Seq Preprocessing Module for Single-Cell Atlas Builder.

This module provides functions to load single-cell data, perform quality control (QC),
filtering, normalization, PCA, neighborhood graph computation, and UMAP embedding.

Functions:
- load_input(path): Load .h5ad or .csv data into an AnnData object.
- run_qc_filter(adata, ...): Perform QC filtering based on genes per cell, mitochondrial content, etc.
- normalize_log(adata, ...): Normalize total counts per cell and log-transform data.
- run_pca_umap(adata, ...): Select highly variable genes, perform PCA, compute neighbors, and UMAP.
- preprocess_pipeline(path): Complete preprocessing pipeline combining all steps.
"""

import scanpy as sc
import anndata
import pandas as pd

def load_input(path: str) -> anndata.AnnData:
    """
    Load single-cell data from a file.

    Parameters:
    - path (str): Path to the input file (.h5ad or .csv).

    Returns:
    - adata (anndata.AnnData): Loaded single-cell AnnData object.

    Raises:
    - ValueError: If file format is unsupported.
    """
    ext = path.split(".")[-1].lower()
    if ext == "h5ad":
        adata = sc.read_h5ad(path)
    elif ext == "csv":
        df = pd.read_csv(path, index_col=0)
        adata = anndata.AnnData(df)
    else:
        raise ValueError(f"Unsupported file format: {ext}")
    return adata


def run_qc_filter(adata: anndata.AnnData,
                  min_genes_per_cell: int = 200,
                  max_genes_per_cell: int = 7500,
                  max_mt_pct: float = 10.0,
                  min_cells_per_gene: int = 3) -> anndata.AnnData:
    """
    Perform quality control on cells and genes.

    Parameters:
    - adata (AnnData): Input AnnData object.
    - min_genes_per_cell (int): Minimum genes per cell.
    - max_genes_per_cell (int): Maximum genes per cell.
    - max_mt_pct (float): Maximum percent mitochondrial counts.
    - min_cells_per_gene (int): Minimum cells expressing a gene.

    Returns:
    - adata (AnnData): Filtered AnnData object.
    """
    sc.pp.filter_cells(adata, min_genes=min_genes_per_cell)
    sc.pp.filter_cells(adata, max_genes=max_genes_per_cell)
    sc.pp.filter_genes(adata, min_cells=min_cells_per_gene)

    # Human mitochondrial genes start with 'MT-'
    adata.var['mt'] = adata.var_names.str.startswith('MT-')
    sc.pp.calculate_qc_metrics(adata, qc_vars=['mt'], percent_top=None, log1p=False, inplace=True)

    # Filter cells with high mitochondrial content
    adata = adata[adata.obs.pct_counts_mt < max_mt_pct, :]
    
    return adata


def normalize_log(adata: anndata.AnnData, target_sum: float = 1e4) -> anndata.AnnData:
    """
    Normalize total counts per cell and log-transform.

    Parameters:
    - adata (AnnData): Input AnnData object.
    - target_sum (float): Target total counts per cell.

    Returns:
    - adata (AnnData): Normalized and log-transformed AnnData object.
    """
    sc.pp.normalize_total(adata, target_sum=target_sum)
    sc.pp.log1p(adata)
    return adata


def run_pca_umap(adata: anndata.AnnData, n_top_genes: int = 2000, n_pcs: int = 50, n_neighbors: int = 15) -> anndata.AnnData:
    """
    Perform PCA, compute neighbors, and run UMAP.

    Parameters:
    - adata (AnnData): Input AnnData object.
    - n_top_genes (int): Number of highly variable genes to use.
    - n_pcs (int): Number of principal components.
    - n_neighbors (int): Number of neighbors for graph construction.

    Returns:
    - adata (AnnData): AnnData object with PCA, neighbors, and UMAP embeddings.
    """
    sc.pp.highly_variable_genes(adata, n_top_genes=n_top_genes, subset=True)
    sc.tl.pca(adata, svd_solver='arpack', n_comps=n_pcs)
    sc.pp.neighbors(adata, n_neighbors=n_neighbors, n_pcs=min(n_pcs, adata.obsm['X_pca'].shape[1]))
    sc.tl.umap(adata)
    return adata


def preprocess_pipeline(path: str) -> anndata.AnnData:
    """
    Full preprocessing pipeline: load -> QC/filter -> normalize -> PCA/UMAP.

    Parameters:
    - path (str): Path to input dataset.

    Returns:
    - adata (AnnData): Fully preprocessed AnnData object.
    """
    adata = load_input(path)
    adata = run_qc_filter(adata)
    adata = normalize_log(adata)
    adata = run_pca_umap(adata)
    return adata


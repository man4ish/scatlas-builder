"""
clustering.py

Single-Cell Clustering Module for Single-Cell Atlas Builder.

This module provides functions for clustering cells using the Leiden algorithm
and ranking marker genes for each cluster.
"""

import scanpy as sc
from anndata import AnnData

def run_leiden(adata: AnnData, resolution: float = 0.5, method: str = 't-test') -> AnnData:
    """
    Perform Leiden clustering and rank marker genes per cluster.

    Parameters:
    - adata (AnnData): Preprocessed AnnData object.
    - resolution (float): Leiden clustering resolution parameter (higher = more clusters).
    - method (str): Method for ranking marker genes. Options: 't-test', 'wilcoxon', 'logreg'.

    Returns:
    - adata (AnnData): AnnData object with 'leiden' clusters and 'rank_genes_groups' results.
    """
    # Run Leiden clustering
    sc.tl.leiden(adata, resolution=resolution)
    
    # Rank genes for each cluster
    sc.tl.rank_genes_groups(adata, groupby='leiden', method=method)
    
    return adata

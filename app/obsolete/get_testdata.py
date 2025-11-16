import scanpy as sc
import anndata
import numpy as np
import pandas as pd

# Create a 10 cells x 5 genes matrix with random counts
data = np.random.rand(10, 5) * 100  # avoid too small numbers

# AnnData object
adata = anndata.AnnData(X=data)

# Add minimal obs (cells) and var (genes)
adata.obs['cell_id'] = [f'cell{i}' for i in range(10)]
adata.var['gene_symbols'] = [f'gene{i}' for i in range(5)]

# Add n_counts for QC to avoid empty slice errors
adata.obs['n_counts'] = adata.X.sum(axis=1)
adata.var['n_counts'] = adata.X.sum(axis=0)

# Save h5ad
adata.write("sample_test_fixed.h5ad")
print("Fixed dummy dataset created: sample_test_fixed.h5ad")

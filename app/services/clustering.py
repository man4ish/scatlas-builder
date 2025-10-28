import scanpy as sc

def run_leiden(adata, resolution: float = 0.5):
    sc.tl.leiden(adata, resolution=resolution)
    sc.tl.rank_genes_groups(adata, 'leiden', method='t-test')
    return adata

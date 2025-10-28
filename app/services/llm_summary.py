# placeholder for LLM summarization integration
# implement LLM calls (local Ollama, HF, or API) here

def summarize_cluster_markers(markers: dict, top_n: int = 10) -> str:
    """
    markers: dict mapping cluster -> [marker genes]
    returns: short text summary (string)
    """
    # simple template until LLM is connected
    lines = []
    for cluster, genes in markers.items():
        top_genes = genes[:top_n]
        lines.append(f"Cluster {cluster}: top markers: {', '.join(top_genes)}")
    return "\n".join(lines)

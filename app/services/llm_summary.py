"""
app/services/llm_summary.py

Module for cluster and pathway summarization using LLaMA 3 from Hugging Face.

This implementation uses Hugging Face's transformers pipeline for text generation.
"""

from typing import Dict, List
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
import torch

# Load LLaMA 3 model and tokenizer
# Note: Make sure you have HF authentication token if needed
MODEL_NAME = "meta-llama/Llama-3-7b-hf"  # or 13b-hf for bigger model
DEVICE = 0 if torch.cuda.is_available() else -1  # GPU if available

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME, device_map="auto")

generator = pipeline("text-generation", model=model, tokenizer=tokenizer, device=DEVICE)

def summarize_cluster_markers(markers: Dict[int, List[str]], top_n: int = 10, max_length: int = 150) -> str:
    """
    Generate a textual summary of top marker genes per cluster using LLaMA 3.

    Args:
        markers (Dict[int, List[str]]): Dictionary mapping cluster IDs to lists of marker genes.
        top_n (int): Number of top genes to include per cluster.
        max_length (int): Maximum length of the generated summary.

    Returns:
        str: Generated summary text.
    """
    prompt_lines = ["Summarize the following single-cell clusters and their top marker genes:"]
    for cluster, genes in markers.items():
        top_genes = genes[:top_n]
        prompt_lines.append(f"Cluster {cluster}: {', '.join(top_genes)}")
    prompt = "\n".join(prompt_lines)

    output = generator(prompt, max_new_tokens=max_length, do_sample=True, temperature=0.7)
    summary = output[0]["generated_text"]

    return summary

# 🧬 SchnitzelLMTagger

**From messy medical reports to structured cancer data — powered by open-source LLMs, prompts, and RAG.**

> An NLP pipeline for extracting oncological attributes from German pathology reports using Large Language Models and Retrieval-Augmented Generation (RAG).

---

## 📌 Overview

OncoPrompt is a research-grade pipeline that leverages the power of open-source large language models (LLMs), prompt engineering, and RAG techniques to extract structured medical information from unstructured German-language pathology reports.

This project explores zero-shot, few-shot, and RAG-enhanced prompting strategies to automatically identify key clinical attributes for cancer registry documentation, including:

- ICD-10 / ICD-O Codes  
- Tumor Grading and Staging (TNM, UICC)  
- Vascular, Lymphovascular, and Perineural Invasion  
- Residual Tumor Classification  

---

## ⚙️ Features

- ✅ **Support for German medical texts**
- 🧠 **LLM support:** Mistral, LLaMA, Mixtral, SauerkrautLM variants (4-bit quantized)
- 🔁 **Three prompting strategies:** Zero-shot, few-shot, and RAG with reranking
- 📦 **Modular pipeline** using [`LlamaIndex`](https://github.com/jerryjliu/llama_index)
- 🔍 **Vector-based retrieval** with `DuckDB` and `jina-embeddings-v2-base-de`
- 📊 **Performance evaluation** using precision, recall, and macro-averaged F1-score

---

## 🏥 Use Case

Designed for German hospital settings, this tool automates entity recognition for oncology documentation, enabling:

- Faster cancer registry updates  
- Reduced clinician workload  
- Higher consistency in medical coding  
- Improved research data quality

---

## 🚀 Getting Started

### Requirements

- Python 3.12+
- Ollama or GPU support for LLM inference
- Docker (recommended for local deployment)
- [LlamaIndex](https://github.com/jerryjliu/llama_index), `pydantic`, `jina`, `duckdb`, `faiss`, etc.

### Installation

```bash
git clone https://github.com/your-username/OncoPrompt.git
cd SchnitzelLMTagger
pip install -r requirements.txt

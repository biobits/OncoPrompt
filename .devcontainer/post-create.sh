#!/usr/bin/env bash
pip3 install --upgrade pip
pip3 install -r requirements.txt
python -c "import os; from llama_index.embeddings.huggingface import HuggingFaceEmbedding; HuggingFaceEmbedding(model_name="mixedbread-ai/deepset-mxbai-embed-de-large-v1",)" 
python -c "import os; from FlagEmbedding import FlagReranker; FlagReranker('BAAI/bge-reranker-v2-m3')" 

    
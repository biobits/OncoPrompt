import pandas as pd
import sys
sys.path.append('.')
import oncoprompt_lib as opl
import promptlibrary as pl
import time

from llama_index.llms.ollama import Ollama
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings,Document, StorageContext
from llama_index.core.prompts import PromptTemplate
#from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.core.node_parser import SentenceSplitter
from llama_index.llms.ollama import Ollama
from llama_index.vector_stores.duckdb import DuckDBVectorStore
from llama_index.core import StorageContext
from llama_index.core.postprocessor import SentenceTransformerRerank
## Infos for RAG
# https://docs.llamaindex.ai/en/stable/examples/structured_outputs/structured_outputs/
baseurl="some.server.de:11434"
## Set the embedding model to Jina Embedding
Settings.embed_model = OllamaEmbedding(model_name="jina/jina-embeddings-v2-base-de",
                                       base_url=baseurl
Settings.context_window  = 128000
# ollama models #
# llama3.2:3b-instruct-q4_1
# mistral-nemo:12b-instruct-2407-q4_K_M
# cyberwald/llama-3.1-sauerkrautlm-8b-instruct
# llama3.3:70b-instruct-q4_K_M
# mixtral:8x7b-instruct-v0.1-q4_K_M

run_id="20250227_RAG_FewShot_Jina_RERANKNOTEMP_SimpSUm"
my_models={
          "sauermix8x7":"hf.co/mradermacher/SauerkrautLM-Mixtral-8x7B-Instruct-GGUF:Q4_K_M"		
           "sauernemo":"cyberwald/sauerkrautlm-nemo-12b-instruct:q6_k",
          "ll3sauer":"cyberwald/llama-3.1-sauerkrautlm-8b-instruct",
           "llama3_3":"llama3.3:70b-instruct-q4_K_M",
           "mistralsmall":"mistral-small:24b-instruct-2501-q4_K_M"
           }

# IAll documents
rep= pd.read_csv('goldstandard.csv', sep=';',encoding='utf-8')
# remove unwanted columns
rep = rep.drop(columns=['NEG_MUT','NEG_DIAG_PATHO','PROT','GEN','PUB'])

# # Prepare RAG pipeline by adding onco docs to the index
# Load created vector store from disk
vector_store = DuckDBVectorStore.from_local("./vec_store/vectorstore_full_Jina.duckdb")
index = VectorStoreIndex.from_vector_store(vector_store, show_progress=True,embed_model=Settings.embed_model)

p_template=PromptTemplate(pl.qa_prompt_tmpl_de)
query=pl.queries_de_RAG

## Reranker to improve speed
reranker =  SentenceTransformerRerank(
    model="BAAI/bge-reranker-v2-m3", top_n=2
)
##reranker end
## Pipeline Parameter
_response_mode="simple_summarize"
_temperature=0.00
_stk=2 #similarity_top_k
_node_postprocessors=[reranker]


#Iterate over models
for mod in my_models:
    print("Model: ",my_models[mod])
    llm = Ollama( model=my_models[mod],base_url=baseurl, request_timeout=1200.0, show_progress=True, temperature=_temperature)
    #You can convert any LLM to a "structured LLM" by attaching an output class to it through as_structured_llm.
    sllm=llm.as_structured_llm(output_cls=opl.OncoStruct)
    query_engine = index.as_query_engine(llm=sllm,
                                          similarity_top_k=_stk,
                                          node_postprocessors=_node_postprocessors,
                                          response_mode=_response_mode,
                                          seed=123)
    query_engine.update_prompts(
    {"response_synthesizer:text_qa_template": p_template}
        ) 
    # Iteration over the documents
    for i, row in rep.iterrows():
        _report=   row['report']
        _reportid= row['reportid']

        # Visualize Progress
        print("-----------------------Nummer: ",i,"-----------------------------")
        print("Diag_Patho: ",row["DIAG_PATHO"], "| ICD10: ",row["ICD10"], "| ICD_O_LOK: ",row["ICD_O_LOK"], "| ICD_O_HIST: ",row["ICD_O_HIST"], "| UICC_STAGE: ",row["UICC_STAGE"], "| T_STATUS: ",row["T_STATUS"], "| N_STATUS: ",row["N_STATUS"], "| GRAD: ",row["GRAD"], "| R_STATUS: ",row["R_STATUS"],"| M_STATUS: ",row["M_STATUS"] ,"| VI: ",row["VI"], "| PNI: ",row["PNI"], "| LI: ",row["LI"] )

        _res=opl.query_local_RAG(query_engine,_report,_reportid,query,run_id,mod)
        print(_res["result"])
        print("----------------------------------------------------")
        print("Time: ",_res["time"])
        print("----------------------------------------------------")
        print("")
        print("")


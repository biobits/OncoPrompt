import pandas as pd
import oncoprompt_lib as opl
import promptlibrary as pl
import time
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.core.prompts import PromptTemplate
from llama_index.llms.ollama import Ollama

# Load documents
rep= pd.read_csv('goldstandard.csv', sep=';',encoding='utf-8')
# remove unwanted columns
rep = rep.drop(columns=['NEG_MUT','NEG_DIAG_PATHO','PROT','GEN','PUB'])
# Base URL for Ollama Service
baseurl="some.server.de:11434"
# ID for the run
run_id="20250227_ll3sauer_OneShot"
# Models
my_models={"sauernemo":"cyberwald/sauerkrautlm-nemo-12b-instruct:q6_k",
           "sauermix8x7":"hf.co/mradermacher/SauerkrautLM-Mixtral-8x7B-Instruct-GGUF:Q4_K_M",
          "ll3sauer":"cyberwald/llama-3.1-sauerkrautlm-8b-instruct",           
           "mistralsmall":"mistral-small:24b-instruct-2501-q4_K_M",
           "llama3_3":"llama3.3:70b-instruct-q4_K_M"
           }

#Iterate over models
for mod in my_models:
    llm = Ollama( model=my_models[mod],base_url=baseurl, request_timeout=1360.0)

    # Iteration over the documents
    for i, row in rep.iterrows():
        _report=   row['report']
        _reportid= row['reportid']
        prompt=PromptTemplate(pl.prompt_de_oneshot)
        t = time.time()
         ## Print progress
        print("--------------Model: ",mod,"---------Nummer: ",i,"-----------------------------")
        print("Diag_Patho: ",row["DIAG_PATHO"], "| ICD10: ",row["ICD10"], "| ICD_O_LOK: ",row["ICD_O_LOK"], "| ICD_O_HIST: ",row["ICD_O_HIST"], "| UICC_STAGE: ",row["UICC_STAGE"], "| T_STATUS: ",row["T_STATUS"], "| N_STATUS: ",row["N_STATUS"], "| GRAD: ",row["GRAD"], "| R_STATUS: ",row["R_STATUS"],"| M_STATUS: ",row["M_STATUS"] ,"| VI: ",row["VI"], "| PNI: ",row["PNI"], "| LI: ",row["LI"])
        print("-------------------------------------------------------------")
        response = llm.structured_predict(opl.OncoStruct,prompt,text=_report ,reportid=_reportid)
        json_output = response.model_dump_json()
        print(json_output)
        elapsed_time = time.time() - t
   
        opl.save_json_data_to_duckdb("model_results",mod, json_output,_reportid ,run_id,elapsed_time,"success","OK")
        ## Print progress
        print("Reportid: ",_reportid, " | Model: ",mod, " | Nummer: ",i, " | time: ",elapsed_time)
        print("-------------------------------------------------------------")
        print("")
        print("")
  





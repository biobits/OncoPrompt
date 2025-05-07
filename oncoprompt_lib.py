from pydantic import BaseModel, Field
import json
import pandas as pd
import duckdb
from IPython.display import Markdown, display
import subprocess
from llama_index.llms.ollama import Ollama
import time
import promptlibrary as pl

#############################################################################################
# Pydantic models for the structured prediction
#############################################################################################

class OncoStruct(BaseModel):
    reportid: str #= Field(description="Die ID des Patientenberichts")
    diagnose_text: str #= Field(description="Die freitextliche Hauptdiagnose an, z.B. \"Adenokarzinom des Kolons\" und keine weitere Codierung")
    icd_10: str #= Field(pattern= r'\b[A-Z]\d{2}(?:\.\d+|-)?\b|N\.D\.')
    icd_o_lokalisation: str #= Field(pattern= r'\bC\d{2}(?:\.\d+)?\b|N\.D\.')
    icd_o_histologie: str #= Field(pattern= r'\d{4}(?:/\d[012369])?\b')
    uicc_status: str #= Field(description="Das UICC Stadium das im Bericht dokumentiert wurde")
    t_status: str #= Field(pattern=r'(c|p|yc|yp|r|rp|a)T([0-4]|is|X)(a|b|c|d|\+|\(m\)|\(\d+\))*')#description="Das t Stadium, welches im Bericht dokumentiert wurde. Gib nur den Status mit Präfix an, z.B. pT1, T2, T3, T4a, T4b,cT2a, cT2b")
    n_status: str #= Field(description="Das n Stadium, welches im Bericht dokumentiert wurde. Gib hier nur den Status mit Präfix an, z.B. N0, cN1, N2, N3,pN3")
    grading: str #= Field(description="Das histologische Grading, welches im Bericht dokumentiert wurde")
    r_status: str #= Field(description="Der Resektionsstatus, der im Bericht dokumentiert wurde")
    m_stadium: str #= Field(description="Der M-Status, der im Bericht dokumentiert wurde")
    veneninvasion: str #= Field(description="Die Veneninvasion, die im Bericht dokumentiert wurde")
    perineurale_invasion: str #= Field(description="Die perineurale Invasion, die im Bericht dokumentiert wurde")
    lymphgefaessinvasion: str #= Field(description="Die Lymphgefäßinvasion, die im Bericht dokumentiert wurde")s


#############################################################################################
# Helper Functions for the project
#############################################################################################

def start_ollama():
    """
    Starts the Ollama server and waits for 15 seconds to ensure that the server is running.
    """
    # Start the Ollama server
    sub=subprocess.Popen("ollama serve", shell=True, stdout=subprocess.PIPE)
    time.sleep(5)

    return sub


def get_duckdb_connection(db_file="out/llmresults.duckdb"):
    """
    Returns a connection to a DuckDB database.
    Parameters:
    db_file (str): The path to the DuckDB database file.

    Returns:
    duckdb.DuckDB: A connection to a DuckDB database.
    """
    conn = duckdb.connect(database=db_file, read_only=False)
    return conn

def save_error_data_to_duckdb(table_name,modelname,id,run_id,elapsed_time, status,status_message):
    """

    """
    insert_query = f"INSERT INTO {table_name} (runid, model, reportid, responsetime, status, status_message) VALUES (\
    '{run_id}','{modelname}','{id}',{elapsed_time},'{status}','{status_message}')"
    print(insert_query)
    try:
        # connection erstellen
        conn= get_duckdb_connection()
        
        # Insert data with named placeholders
        conn.execute(insert_query) 
        print("data saved successfully.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Verbindung schließen
        conn.close()

def save_json_data_to_duckdb(table_name,modelname, json_response,id, runid,responsetime,status,status_message):
    """
    Saves data from a JSON response into an existing table in a duchdb.
    Each new column can have a specified prefix.

    Parameters:
    existing_df (pd.DataFrame): The existing DataFrame to which data will be added.
    json_response (str): The JSON response as a string.
    prefix (str): The prefix to be added to each new column name.

    Returns:
    pd.DataFrame: The merged DataFrame containing the new data.
    """
    # Step 1: Parse JSON
    parsed_json = json.loads(json_response)

    # Step 2: Create a new DataFrame from the JSON data with prefixed column names
    new_data = {
        f'runid': runid,
        f'model': modelname,
        f'reportid': id,
        f'diagnose_text': parsed_json['diagnose_text'],
        f'ICD10': parsed_json['icd_10'],
        f'ICD_O_LOK': parsed_json['icd_o_lokalisation'],
        f'ICD_O_HIST': parsed_json['icd_o_histologie'],
        f'UICC_STAGE': parsed_json['uicc_status'],
        f'T_STATUS': parsed_json['t_status'],
        f'N_STATUS': parsed_json['n_status'],
        f'GRAD': parsed_json['grading'],
        f'R_STATUS': parsed_json['r_status'],
        f'M_STATUS': parsed_json['m_stadium'],
        f'VI': parsed_json['veneninvasion'],
        f'PNI': parsed_json['perineurale_invasion'],
        f'LI': parsed_json['lymphgefaessinvasion'],
        f'responsetime': str(responsetime),
        f'status': status,
        f'status_message': status_message
       # f'mutations_gen': parsed_json['mutationen'][0]['gen'],  # Extract the first mutation's gene
       # f'mutations_status': parsed_json['mutationen'][0]['mutationsstatus']
    }
     # Step 3: Insert the new data into the table
    columns = ', '.join(new_data.keys())
    placeholders = ', '.join(['?'] * len(new_data))  # Create placeholders for parameterized query

    insert_query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
    
    #print(insert_query)
    try:
        # connection erstellen
        conn= get_duckdb_connection()        
        # inseer datat with named placeholders 
        conn.execute(insert_query, tuple(new_data.values())) 
        print("Datensatz erfolgreich gespeichert.")
    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {e}")
    finally:
        # close connection
        conn.close()

def add_json_data_to_dataframe(existing_df, json_response,id, prefix=''):
    """
    Merges data from a JSON response into an existing DataFrame based on the reportid.
    Each new column can have a specified prefix.

    Parameters:
    existing_df (pd.DataFrame): The existing DataFrame to which data will be added.
    json_response (str): The JSON response as a string.
    prefix (str): The prefix to be added to each new column name.

    Returns:
    pd.DataFrame: The merged DataFrame containing the new data.
    """
    # Step 1: Parse JSON
    parsed_json = json.loads(json_response)

    # Step 2: Create a new DataFrame from the JSON data with prefixed column names
    new_data = {
        f'{prefix}reportid': id,#parsed_json['reportid'],
        f'{prefix}diagnose_text': parsed_json['diagnose_text'],
        f'{prefix}ICD10': parsed_json['icd_10'],
        f'{prefix}ICD_O_LOK': parsed_json['icd_o_lokalisation'],
        f'{prefix}ICD_O_HIST': parsed_json['icd_o_histologie'],
        f'{prefix}UICC_STAGE': parsed_json['uicc_status'],
        f'{prefix}T_STATUS': parsed_json['t_status'],
        f'{prefix}N_STATUS': parsed_json['n_status'],
        f'{prefix}GRAD': parsed_json['grading'],
        f'{prefix}R_STATUS': parsed_json['r_status'],
        f'{prefix}M_STATUS': parsed_json['m_stadium'],
        f'{prefix}VI': parsed_json['veneninvasion'],
        f'{prefix}PNI': parsed_json['perineurale_invasion'],
        f'{prefix}LI': parsed_json['lymphgefaessinvasion']
    }
    
    new_df = pd.DataFrame([new_data])


    return new_data

def display_prompt_dict(prompts_dict):
    for k, p in prompts_dict.items():
        text_md = f"**Prompt Key**: {k}<br>" f"**Text:** <br>"
        display(Markdown(text_md))
        print(p.get_template())
        display(Markdown("<br><br>"))



def query_local_RAG(_queryengine,_report,_reportid,_query,_runid,_modelname):
    """
    Run a query on a local LLM model and save the results to a DuckDB database.
    Parameters:
    _queryengine: The query engine to use for the query.
    _prompttemplate: The prompt template to use for the query.
    _report: The report text to use for the query.
    _reportid: The report ID to use for the query.
    _query: The query text to use for the query.
    _runid: The run ID to use for the query.
    _modelname: The model name to use
    """
    _status="success"
      
    ## Query ENgine: mit response_mode und node_postprocessors experimentieren:https://docs.llamaindex.ai/en/stable/examples/structured_outputs/structured_outputs/
    prompt=pl.query_template_fewshot_de.format(text=_report,reportid=_reportid,query_de=_query)
    t = time.time()
    try:
        response=_queryengine.query(prompt)
        
        json_output = str(response)
        elapsed_time = time.time() - t
        #table_name,modelname, json_response,id, runid)
        save_json_data_to_duckdb("model_results",_modelname, json_output,_reportid ,_runid,elapsed_time,_status,"OK")
    except Exception as e:
        _status="error"
        elapsed_time = time.time() - t
        save_error_data_to_duckdb("model_results",_modelname,_reportid,_runid,elapsed_time, _status,str(e))
        print(f"Error: {e}")
        
    finally:
        return {"runid":_runid,"reportid":_reportid,"model":_modelname,"time": elapsed_time,"status":_status,"result":json_output}

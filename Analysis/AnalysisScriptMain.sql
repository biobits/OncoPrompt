with pred_data as (
unpivot (
SELECT  case when runid='202502_OneShot' then '1: ZeroShot'
when runid='202502_FewShot' then '2: FewShot'
when runid in ('202502_RAG_FewShot_Jina_RERANKNOTEMP_SimpSum') then '3: RAG Pipeline'
else runid end as runid
,model, reportid,
case when ICD10='N.D.' or ICD10='' then '###' else ICD10 end as ICD10,
case when ICD_O_LOK='N.D.'  or ICD_O_LOK=''  then '###' else ICD_O_LOK end as ICD_O_LOK, 
case when ICD_O_HIST='N.D.' or ICD_O_HIST='' then '###' else ICD_O_HIST end as ICD_O_HIST, 
case when UICC_STAGE='N.D.' or UICC_STAGE='' then '###' else UICC_STAGE end as UICC_STAGE, 
case when T_STATUS='N.D.' or T_STATUS='' then '###' else T_STATUS end as T_STATUS, 
case when N_STATUS='N.D.' or N_STATUS='' then '###' else N_STATUS end as N_STATUS, 
case when GRAD='N.D.' or GRAD='' then '###' else GRAD end as GRAD, 
case when R_STATUS='N.D.' or R_STATUS='' then '###' else  R_STATUS end as  R_STATUS,
case when M_STATUS='N.D.' or M_STATUS='' then '###' else M_STATUS end as M_STATUS,
case when VI='N.D.' or VI='' then '###' else VI end as VI,
case when PNI='N.D.' or PNI='' then '###' else PNI end as PNI,
case when LI='N.D.' or LI='' then '###' else LI end as LI
FROM llmresults.main.model_results_final
/*where
(runid='20250207_SauerNemoMix8x7_NoRag_OneShot'	and model='sauernemo') or
(runid='20250204_RAG_CustQuery_RERANKNOTEMP'	and model='sauernemo') or
(runid='20250212_SauerNemo_FewShot_Final'	and model='sauernemo') or
(runid='20250214_RAG_FewShot_Jina_RERANKNOTEMP_SimpSUm'	and model='sauernemo')*/

)
--unpivot pred_data
 ON   ICD10, ICD_O_LOK, ICD_O_HIST, UICC_STAGE, T_STATUS, N_STATUS, GRAD, R_STATUS, M_STATUS, VI, PNI, LI
INTO NAME Feature
	VALUE Predicted_Value),
ref_data as (
unpivot (select 'gold' as model, reportid, 
case when ICD10 is null or ICD10='' then '###' else ICD10 end as ICD10,
case when ICD_O_LOK is null   or ICD_O_LOK=''  then '###' else ICD_O_LOK end as ICD_O_LOK, 
case when ICD_O_HIST is null  or ICD_O_HIST='' then '###' else ICD_O_HIST end as ICD_O_HIST, 
case when UICC_STAGE is null  or UICC_STAGE='' then '###' else UICC_STAGE end as UICC_STAGE, 
case when T_STATUS is null  or T_STATUS='' then '###' else T_STATUS end as T_STATUS, 
case when N_STATUS is null  or N_STATUS='' then '###' else N_STATUS end as N_STATUS, 
case when GRAD is null  or GRAD='' then '###' else GRAD end as GRAD, 
case when R_STATUS is null  or R_STATUS='' then '###' else  R_STATUS end as  R_STATUS,
case when M_STATUS is null  or M_STATUS='' then '###' else M_STATUS end as M_STATUS,
case when VI is null  or VI='' then '###' else VI end as VI,
case when PNI is null  or PNI='' then '###' else PNI end as PNI,
case when LI is null  or LI='' then '###' else LI end as LI
FROM llmresults.main.goldstandard g )
ON   ICD10, ICD_O_LOK, ICD_O_HIST, UICC_STAGE, T_STATUS, N_STATUS, GRAD, R_STATUS, M_STATUS, VI, PNI, LI
into NAME Feature
	VALUE Reference_Value
)
select 
--
p.*,
--# Naming the LLM
case when p.model='mix8x7' then 'Mixtral 8x7B'
     when p.model='deepseek_r1_8b' then 'Deepseek R1 8B'
     when p.model='mist_nemo' then 'Mistral Nemo 12B'
	when p.model= 'sauernemo' then 'Mistral Nemo 12B SauerkrautLM'
	when p.model= 'sauermix8x7' then 'Mixtral 8x7B SauerkrautLM'
	when p.model= 'll3sauer' then 'Llama 3.1 SauerkrautLM 8B'           
	when p.model= 'mistralsmall' then 'Mistral Small 24B'
	when p.model= 'll323b' then 'Llama 3.2 3B'
	when p.model= 'llama3_3' then 'Llama 3.3 70b'
	else p.model end as LLM
,case when p.model='mix8x7' then 'Mixtral 8x7B'
     when p.model='deepseek_r1_8b' then 'Deepseek R1 8B'
     when p.model='mist_nemo' then 'Mist. Nemo 12B'
	when p.model= 'sauernemo' then 'Mist. Nemo 12B [S]'
	when p.model= 'sauermix8x7' then 'Mixtral 8x7B [S]'
	when p.model= 'll3sauer' then 'Llama 3.1 8B [S]'           
	when p.model= 'mistralsmall' then 'Mistral Small 24B'
	when p.model= 'll323b' then 'Llama 3.2 3B'
	when p.model= 'llama3_3' then 'Llama 3.3 70b'
	else p.model end as LLM_Label
,case when p.model='mix8x7' then 'Mx7B'
     when p.model='deepseek_r1_8b' then 'DR18B'
     when p.model='mist_nemo' then 'N12B'
	when p.model= 'sauernemo' then 'N12BS'
	when p.model= 'sauermix8x7' then 'Mx7BS'
	when p.model= 'll3sauer' then 'L8B'           
	when p.model= 'mistralsmall' then 'MS24B'
	when p.model= 'll323b' then 'L3B'
	when p.model= 'llama3_3' then 'L70B'
	else p.model end as LLM_LabelShort
,case when p.model='mix8x7' then 60
     when p.model='deepseek_r1_8b' then 30
     when p.model='mist_nemo' then 40
	when p.model= 'sauernemo' then 50
	when p.model= 'sauermix8x7' then 70
	when p.model= 'll3sauer' then 20           
	when p.model= 'mistralsmall' then 80
	when p.model= 'll323b' then 10
	when p.model= 'llama3_3' then 90
	else 0 end as LLM_Order
,case when p.Feature ='ICD_O_LOK' then 'ICD-O Topography'
 when p.Feature='ICD_O_HIST' then 'ICD-O Morphology'
 when p.Feature='T_STATUS' then 'T category'
 when p.Feature='N_STATUS' then 'N category'
 when p.Feature='GRAD' then 'Grading'
 when p.Feature='UICC_STAGE' then 'UICC Stage'
 when p.Feature='R_STATUS' then 'R classification' 
 when p.Feature='M_STATUS' then 'M classification'
 else p.Feature end as Feature_Label
,case when runid='1: ZeroShot' then 'Zero Shot' 
	when runid='2: FewShot' then 'Few Shot' 
	when runid='3: RAG Pipeline' then 'RAG' 
	else runid end as QueryType
,r.Reference_Value,
case when contains(r.Reference_Value,p.Predicted_Value) then
	r.Reference_Value else p.Predicted_Value end as Pred_Val_Proof,
case when r.Reference_Value='###'  then 'False'else 'True' end as Ref_Bool,
case when p.Predicted_Value='###' then 'False'
	when r.Reference_Value ='###' and p.Predicted_Value <> '###' then 'True'
	when r.Reference_Value = (case when contains(r.Reference_Value,p.Predicted_Value) or contains(p.Predicted_Value,r.Reference_Value)  then
	r.Reference_Value else p.Predicted_Value end) then 'True'
	else 'False' end as Pred_Boll
from pred_data p
left outer join ref_data r 
on p.reportid=r.reportid
and p.Feature=r.Feature
left outer join llmresults.main.goldstandard g
on g.reportid= p.reportid

;



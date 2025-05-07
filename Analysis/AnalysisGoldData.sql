select 'gold' as model, reportid, 
case when ICD10 is null or ICD10='' then 'N.D.' else ICD10 end as ICD10,
case when ICD_O_LOK is null   or ICD_O_LOK=''  then 'N.D.' else ICD_O_LOK end as ICD_O_LOK, 
case when ICD_O_HIST is null  or ICD_O_HIST='' then 'N.D.' else ICD_O_HIST end as ICD_O_HIST, 
case when UICC_STAGE is null  or UICC_STAGE='' then 'N.D.' else UICC_STAGE end as UICC_STAGE, 
case when T_STATUS is null  or T_STATUS='' then 'N.D.' else T_STATUS end as T_STATUS, 
case when N_STATUS is null  or N_STATUS='' then 'N.D.' else N_STATUS end as N_STATUS, 
case when GRAD is null  or GRAD='' then 'N.D.' else GRAD end as GRAD, 
case when R_STATUS is null  or R_STATUS='' then 'N.D.' else  R_STATUS end as  R_STATUS,
case when M_STATUS is null  or M_STATUS='' then 'N.D.' else M_STATUS end as M_STATUS,
case when VI is null  or VI='' then 'N.D.' else VI end as VI,
case when PNI is null  or PNI='' then 'N.D.' else PNI end as PNI,
case when LI is null  or LI='' then 'N.D.' else LI end as LI,
case when ICD10 is null then
	case when ICD_O_LOK is null then 'N.D.'else left(ICD_O_LOK,3) end else left(ICD10,3) end as ICD
FROM llmresults.main.goldstandard g 



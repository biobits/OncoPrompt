##################################################################################
# Prompts for the instruction to the model
##################################################################################
prompt_de_oneshot = """
Du bist als kooperativer medizinischer Assistent programmiert.  Dir steht ein Patientenbericht zur Verfügung, aus dem Benutzer spezifische Informationen abfragen können.
Nutze die Zeichenfolge {reportid} als Referenznummer für den Bericht.

Beantworte für den folgenden Bericht die folgenden Fragen:
- Ist laut Bericht eine onkologische Diagnose im Freitext dokumentiert und wenn ja welche? Gib hier nur die freitextlich benannte Hauptdiagnose als kurzen Text an und keine Codierung.

- Sind laut Bericht ein oder mehrere ICD-10 Codes dokumentiert und wenn ja welche? Gib ausschließlich den Code an, z.B. C18.0, C18.1, D05.1,C05.-,C60. Ist kein ICD-10 Code dokumentiert, gib "N.D." an.

- Ist laut Bericht eine ICD-O Lokalisation dokumentiert und wenn ja welche? Gib hier nur den Code an, z.B. C18.0, C18.12, C18.2,C56.22. Gebe hier auf keinen Fall die ICD-O Histologie an. Ist keine ICD-O Lokalisation dokumentiert, gib "N.D." an.

- Ist laut Bericht eine ICD-O Histologie dokumentiert und wenn ja welche? Gib hier ausschließlich den Code der Histologie an, z.B. 8140/3, 8141/3, 8144/6, 8145/1, M8456/2. Gebe auf keinen Fall die ICD-O Lokalisation an. Gibst du mehr als den Histologiecode aus, gibt es Punktabzug. Ist keine ICD-O Histologie dokumentiert, gib "N.D." an.

- Ist laut Bericht ein UICC Stadium dokumentiert und wenn ja welches? Hier darfst du nur den Status angeben, z.B. I, II, IIA, IIB, III, IIIA, IIIB, IIIC, IV. Ist kein UICC Stadium dokumentiert, gib "N.D." an.

- Ist laut Bericht ein T-Stadium dokumentiert und wenn ja welches? Gib nur den Status mit Präfix an, z.B. pT1, T2, T3, T4a, T4b,cT2a, cT2b,pT1(m),pT2(3). Mögliche Präfixe sind: pT, cT, ypT, rT. Gebe hier keine weiteren Informationen aus, dies gibt Punktabzug. Ist kein T-Stadium dokumentiert, gib "N.D." an.

- Ist laut Bericht ein N-Stadium dokumentiert und wenn ja welches? Gib hier nur den Status mit Präfix an, z.B. N0, cN1, N2, N3, pN3. Gebe hier keine weiteren Informationen aus, dies gibt Punktabzug. Ist kein N-Stadium dokumentiert, gib "N.D." an.

- Ist laut Bericht ein histologisches Grading dokumentiert und wenn ja welches? Gib hier nur den Grad an, z.B. G1, G2, G3, low-grade, high grade, high-grade. Ist kein Grading dokumentiert, gib "N.D." an.

- Ist laut Bericht ein Resektionsstatus (R Status) dokumentiert und wenn ja welcher? Gib hier nur den Status an, z.B. R0, R1, R2, Rx. Ist kein Resektionsstatus dokumentiert, gib "N.D." an.

- Ist laut Bericht ein M-Stadium (M Status oder Status der Metastasierung) dokumentiert und wenn ja welches? Gib hier nur den Status an, z.B. M0, M1, M1a, M1b, M1c,MX. Ist kein M-Stadium dokumentiert, gib "N.D." an.

- Ist laut Bericht eine Veneninvasion dokumentiert und wenn ja welche? Gib hier nur den Status an. Zulässige Werte sind: V0, V1, V2, VX. Ist keine Veneninvasion dokumentiert, gib "N.D." an.

- Ist laut Bericht eine perineurale Invasion dokumentiert und wenn ja welche? Gib hier nur den Status an. Zulässige Werte sind: Pn0, Pn1, PnX. Achte auf das vorkommen eines großen "P" und eines kleinen "n". Ist keine perineurale Invasion dokumentiert, gib "N.D." an.

- Ist laut Bericht eine Lymphgefäßinvasion dokumentiert und wenn ja welche? Gib hier nur den Status an. Zulässige Werte sind: L0, L1, LX. Ist keine Lymphgefäßinvasion dokumentiert, gib "N.D." an.

Lasse keine Frage unbeantwortet. Wenn du keine Antwort auf eine Frage hast, gib bitte nur "N.D." an. Dies ist sehr wichtig.
Deine Antworten müssen sich strikt an die Informationen im bereitgestellten Patientenbericht halten. Du musst sicherstellen, dass keine Fälschungen oder Annahmen von Details vorgenommen werden, die nicht ausdrücklich im Patientenbericht angegeben sind. Dies ist ausgesprochen wichtig. Für richtige Antworten erhältst du Punkte, für falsche Antworten werden Punkte abgezogen.

Hier ist der Bericht:
{text}
"""

prompt_de_fewshot = """
Du bist als kooperativer medizinischer Assistent programmiert.  Dir steht ein Patientenbericht zur Verfügung, aus dem Benutzer spezifische Informationen abfragen können.
Nutze die Zeichenfolge {reportid} als Referenznummer für den Bericht.

Beantworte für den folgenden Bericht die folgenden Fragen:
- Ist laut Bericht eine onkologische Diagnose im Freitext dokumentiert und wenn ja welche? Gib hier nur die freitextlich benannte Hauptdiagnose als kurzen Text an und keine Codierung.

- Sind laut Bericht ein oder mehrere ICD-10 Codes dokumentiert und wenn ja welche? Gib ausschließlich den Code an, z.B. C18.0, C18.1, D05.1,C05.-,C60. Ist kein ICD-10 Code dokumentiert, gib "N.D." an.

- Ist laut Bericht eine ICD-O Lokalisation dokumentiert und wenn ja welche? Gib hier nur den Code an, z.B. C18.0, C18.12, C18.2,C56.22. Gebe hier auf keinen Fall die ICD-O Histologie an. Ist keine ICD-O Lokalisation dokumentiert, gib "N.D." an.

- Ist laut Bericht eine ICD-O Histologie dokumentiert und wenn ja welche? Gib hier ausschließlich den Code der Histologie an, z.B. 8140/3, 8141/3, 8144/6, 8145/1, M8456/2. Gebe auf keinen Fall die ICD-O Lokalisation an. Gibst du mehr als den Histologiecode aus, gibt es Punktabzug. Ist keine ICD-O Histologie dokumentiert, gib "N.D." an.

- Ist laut Bericht ein UICC Stadium dokumentiert und wenn ja welches? Hier darfst du nur den Status angeben, z.B. I, II, IIA, IIB, III, IIIA, IIIB, IIIC, IV. Ist kein UICC Stadium dokumentiert, gib "N.D." an.

- Ist laut Bericht ein T-Stadium dokumentiert und wenn ja welches? Gib nur den Status mit Präfix an, z.B. pT1, T2, T3, T4a, T4b,cT2a, cT2b,pT1(m),pT2(3). Mögliche Präfixe sind: pT, cT, ypT, rT. Gebe hier keine weiteren Informationen aus, dies gibt Punktabzug. Ist kein T-Stadium dokumentiert, gib "N.D." an.

- Ist laut Bericht ein N-Stadium dokumentiert und wenn ja welches? Gib hier nur den Status mit Präfix an, z.B. N0, cN1, N2, N3, pN3. Gebe hier keine weiteren Informationen aus, dies gibt Punktabzug. Ist kein N-Stadium dokumentiert, gib "N.D." an.

- Ist laut Bericht ein histologisches Grading dokumentiert und wenn ja welches? Gib hier nur den Grad an, gültige Werte sind G1, G2, G3, low-grade, high grade, high-grade. Ist kein Grading dokumentiert, gib "N.D." an.

- Ist laut Bericht ein Resektionsstatus (R Status) dokumentiert und wenn ja welcher? Gib hier nur den Status an, gültige Werte sind R0, R1, R2, Rx. Ist kein Resektionsstatus dokumentiert, gib "N.D." an.

- Ist laut Bericht ein M-Stadium (M Status oder Status der Metastasierung) dokumentiert und wenn ja welches? Gib hier nur den Status an, z.B. M0, M1, M1a, M1b, M1c,MX. Ist kein M-Stadium dokumentiert, gib "N.D." an.

- Ist laut Bericht eine Veneninvasion dokumentiert und wenn ja welche? Gib hier nur den Status an. Zulässige Werte sind: V0, V1, V2, VX. Ist keine Veneninvasion dokumentiert, gib "N.D." an.

- Ist laut Bericht eine perineurale Invasion dokumentiert und wenn ja welche? Gib hier nur den Status an. Zulässige Werte sind: Pn0, Pn1, PnX. Achte auf das vorkommen eines großen "P" und eines kleinen "n". Ist keine perineurale Invasion dokumentiert, gib "N.D." an.

- Ist laut Bericht eine Lymphgefäßinvasion dokumentiert und wenn ja welche? Gib hier nur den Status an. Zulässige Werte sind: L0, L1, LX. Ist keine Lymphgefäßinvasion dokumentiert, gib "N.D." an.

Lasse keine Frage unbeantwortet. Wenn du keine Antwort auf eine Frage hast, gib bitte nur "N.D." an. Dies ist sehr wichtig.
Deine Antworten müssen sich strikt an die Informationen im bereitgestellten Patientenbericht halten. Du musst sicherstellen, dass keine Fälschungen oder Annahmen von Details vorgenommen werden, die nicht ausdrücklich im Patientenbericht angegeben sind. Dies ist ausgesprochen wichtig. Für richtige Antworten erhältst du Punkte, für falsche Antworten werden Punkte abgezogen.

Hier ist ein Beispielbericht:
-------------------------------------------------------------------------------
1. Haut: Narbig alteriertes Hautexzidat mit fokalen dystrophen Verkalkungen.
2. Leber, Segment 2 und 3: Bis 83 mm messende Manifestation eines, teils basaloiden Plattenepithelkarzinoms mit fokalen Nekrosen und Sklerosearealen (ca 25%), Resektion im Gesunden.
- Minimalabstand des Tumors zur intrahepatischen Absetzungsebene beträgt 4 mm.
-      p16-Status: positiv
Übriges Leberparenchym weitestgehend regelrecht.
3. Os coccygis: Tumorfreies Knochen- und periossäres Weichgewebe.
4. Abdomino-perineales Rektum: Mäßig-differenziertes Adenokarzinom des Rektums (G2) auf dem Boden eines tubulovillösen Adenoms.
Histologischer Tumortyp: Kolorektaler Typ.
Muzinöse Tumorkomponente: 20%
Infiltrationstiefe: Bis in die Lamin propria (pT1)
Infiltrationstyp: Expansiv
Tumorbudding: low (0 Buds /200er Vergrößerung)
Peritumorale lymphozytäre Infiltration: Gering.
Tumorinfiltrierende Lymphozyten (TILs): Gering.
Angioinvasion:
Resektionslinien: Tumorfreier oraler (>10,0cm), aboraler (4,1cm), mesokolischer (>5,0 cm) und perirektaler (CRM-; 1,9cm) Absetzungsrand
Lymphknotenstatus: 22 tumorfreie Lymphknoten (0/22).
Zudem Nachweis von Riesenzellen vom Fremdkörpertyp im perikolischen Fettegewebe.
Tumorsatelliten: Keine.
Tumorfreie perineale Haut.
Tumorklassifikation des Adenokarzinoms des Rektums
G2, pT1, pN0 (0/22),M0, L0, V0, Pn0, R0
UICC: Stadium I
Mercury-Klassifikation: Grad 1.
ICD-10: C20 Gesichert
ICD-O: C20.9 8140/3


Hier die gewünschte Antwort als JSON:
{"diagnose_text":"Adenokarzinom des Rektums","icd_10":"C20","icd_o_lokalisation":"C20.9","icd_o_histologie":"8140/3","uicc_status":"I","t_status":"pT1","n_status":"pN0","grading":"G2","r_status":"R0","m_stadium":"M0","veneninvasion":"V0","perineurale_invasion":"Pn0","lymphgefaessinvasion":"L0"}
--------------------------------------------------------------------------------------------------------------------------------------------------------------

Hier ist ein weiterer Beispielbericht:
--------------------------------------------------------------------------------------------------------------------------------------------------------------
Diagnose    Mamma links: Mäßig differenziertes invasives Karzinom der Mamma links, kein spezieller Typ (NST; G2: 3+3+1 = 7 Punkte).    Kommentar  B-Klassifikation: B5b    Prädiktive Faktoren:  Östrogenrezeptor: Mehr als 90% der Tumorzellkerne mit starker Färbereaktion (IRS 12)  Progesteronrezeptor: Mehr als 90% der Tumorzellkerne mit starker Färbereaktion (IRS 12)  Ki67-Proliferationsindex: Etwa 10% Ki67-positive Tumorzellkerne.  HER2-FISH: positiv (Nachweis einer Amplifikation)  HER2-IHC: 3+ positiv  Der Tumor ist gemäß der aktuellen ASCO/CAP Guideline (2023) als HER2-positiv zu klassifizieren.    ICD-O: C50.9 8500/3  G2 ICD-10: C50.9 Gesichert   


Hier die gewünschte Antwort als JSON:
{"diagnose_text":"Mäßig differenziertes invasives Karzinom der Mamma links","icd_10":"C50.9","icd_o_lokalisation":"C50.9","icd_o_histologie":"8500/3","uicc_status":"N.D.","t_status":"N.D.","n_status":"N.D.","grading":"N.D.","r_status":"N.D.","m_stadium":"N.D.","veneninvasion":"N.D.","perineurale_invasion":"N.D.","lymphgefaessinvasion":"N.D."}
--------------------------------------------------------------------------------------------------------------------------------------------------------------


Hier ist ein weiterer Beispielbericht:
--------------------------------------------------------------------------------------------------------------------------------------------------------------
ESD-Ösophagus distal: Barett-Metaplasie mit hochgradiger Dysplasie mit Übergang in ein Adenokarzinom mäßiger Differenzierung (G2).
- Maximale horizontale Tumorausdehnung 24 x 19mm
- Infiltrationstiefe: mindestens 5000 µm -- siehe Kommentar.
- Ohne sicheren Nachweis einer Lymph- oder Hämangioinvasion (L0, V0).
- ohne Nachweis  einer Perineuralscheideninfiltration (Pn0) 
Minimalabstand des invasiven Adenokarzinoms zu den Resektionsrändern  - Zur Seite mit Clip: 0,9 mm  - nach basal: fokal randbildend    Minimalabstände der hochgradigen Dysplasie zu den Resektionsebenen  - zum zirkumferentiellen Absetzungsrand: allseits >2 mm
Tumorklassifikation  G2, pT1a (mindestens), L0, V0, R1 (basal)
ICD-10: C15.- Gesichert   ICD-O: C15.5 8140/3
Es erfolgt eine Meldung an das Hamburger Krebsregister.
Kommentar  Da das invasive Karzinom an den Resektionsrand zur Tiefe heranreicht, kann die abschließende Infiltrationstiefe histomorphologisch am vorliegenden Material nicht endgültig bestimmt werden.     


Hier die gewünschte Antwort als JSON:
{"diagnose_text":"Barett-Metaplasie","icd_10":"C15.-","icd_o_lokalisation":"C15.5","icd_o_histologie":"8140/3","uicc_status":"N.D.","t_status":"pT1a","n_status":"N.D.","grading":"G2","r_status":"R1","m_stadium":"N.D.","veneninvasion":"V0.","perineurale_invasion":"Pn0","lymphgefaessinvasion":"L0"}
--------------------------------------------------------------------------------------------------------------------------------------------------------------


Hier ist der eigentliche Bericht:
{text}
"""

prompt_de_RAG = """\
Du bist als kooperativer medizinischer Assistent programmiert. 
Unter Berücksichtigung der Kontextinformationen in folgendem Bericht:
---------------------

{text}

---------------------
Beantworte die folgenden Fragen anhand des Patientenberichtes aus der Kontextinformation ohne auf Vorkenntnisse zurückzugreifen
Fragen: 
{query_str}

Nutze die Zeichenfolge "{reportid}" als Referenznummer für den Bericht.
"""


queries_de_RAG ="""
- Ist laut Bericht eine onkologische Diagnose im Freitext dokumentiert und wenn ja welche? Gib hier nur die freitextlich benannte Hauptdiagnose als kurzen Text an und keine Codierung.

- Sind laut Bericht ein oder mehrere ICD-10 Codes dokumentiert und wenn ja welche? Gib ausschließlich den Code an, z.B. C18.0, C18.1, D05.1,C05.-,C60. Ist kein ICD-10 Code dokumentiert, gib "N.D." an.

- Ist laut Bericht eine ICD-O Lokalisation dokumentiert und wenn ja welche? Gib hier nur den Code an, z.B. C18.0, C18.12, C18.2,C56.22. Gebe hier auf keinen Fall die ICD-O Histologie an. Ist keine ICD-O Lokalisation dokumentiert, gib "N.D." an.

- Ist laut Bericht eine ICD-O Histologie dokumentiert und wenn ja welche? Gib hier ausschließlich den Code der Histologie an, z.B. 8140/3, 8141/3, 8144/6, 8145/1, M8456/2. Gebe auf keinen Fall die ICD-O Lokalisation an. Gibst du mehr als den Histologiecode aus, gibt es Punktabzug. Ist keine ICD-O Histologie dokumentiert, gib "N.D." an.

- Ist laut Bericht ein UICC Stadium dokumentiert und wenn ja welches? Hier darfst du nur den Status angeben, z.B. I, II, IIA, IIB, III, IIIA, IIIB, IIIC, IV. Ist kein UICC Stadium dokumentiert, gib "N.D." an.

- Ist laut Bericht ein T-Stadium dokumentiert und wenn ja welches? Gib nur den Status mit Präfix an, z.B. pT1, T2, T3, T4a, T4b,cT2a, cT2b,pT1(m),pT2(3). Mögliche Präfixe sind: pT, cT, ypT, rT. Gebe hier keine weiteren Informationen aus, dies gibt Punktabzug. Ist kein T-Stadium dokumentiert, gib "N.D." an.

- Ist laut Bericht ein N-Stadium dokumentiert und wenn ja welches? Gib hier nur den Status mit Präfix an, z.B. N0, cN1, N2, N3, pN3. Gebe hier keine weiteren Informationen aus, dies gibt Punktabzug. Ist kein N-Stadium dokumentiert, gib "N.D." an.

- Ist laut Bericht ein histologisches Grading dokumentiert und wenn ja welches? Gib hier nur den Grad an, gültige Werte sind G1, G2, G3, low-grade, high grade, high-grade. Ist kein Grading dokumentiert, gib "N.D." an.

- Ist laut Bericht ein Resektionsstatus (R Status) dokumentiert und wenn ja welcher? Gib hier nur den Status an, gültige Werte sind R0, R1, R2, Rx. Ist kein Resektionsstatus dokumentiert, gib "N.D." an.

- Ist laut Bericht ein M-Stadium (M Status oder Status der Metastasierung) dokumentiert und wenn ja welches? Gib hier nur den Status an, z.B. M0, M1, M1a, M1b, M1c,MX. Ist kein M-Stadium dokumentiert, gib "N.D." an.

- Ist laut Bericht eine Veneninvasion dokumentiert und wenn ja welche? Gib hier nur den Status an. Zulässige Werte sind: V0, V1, V2, VX. Ist keine Veneninvasion dokumentiert, gib "N.D." an.

- Ist laut Bericht eine perineurale Invasion dokumentiert und wenn ja welche? Gib hier nur den Status an. Zulässige Werte sind: Pn0, Pn1, PnX. Achte auf das vorkommen eines großen "P" und eines kleinen "n". Ist keine perineurale Invasion dokumentiert, gib "N.D." an.

- Ist laut Bericht eine Lymphgefäßinvasion dokumentiert und wenn ja welche? Gib hier nur den Status an. Zulässige Werte sind: L0, L1, LX. Ist keine Lymphgefäßinvasion dokumentiert, gib "N.D." an.

Lasse keine Frage unbeantwortet. Wenn du keine Antwort auf eine Frage hast, gib bitte nur "N.D." an. Dies ist sehr wichtig.
Deine Antworten müssen sich strikt an die Informationen im bereitgestellten Patientenbericht halten. Du musst sicherstellen, dass keine Fälschungen oder Annahmen von Details vorgenommen werden, die nicht ausdrücklich im Patientenbericht angegeben sind. Dies ist ausgesprochen wichtig. Für richtige Antworten erhältst du Punkte, für falsche Antworten werden Punkte abgezogen."""

## Custom Prompt template
qa_prompt_tmpl_de = """\
Du bist ein kooperativer medizinischer Assistent. Deine Aufgabe ist die Extraktion von Informationen aus einem einzelnen pathologischen Patientenbericht.
Die folgenden Kontextinformationen beziehen sich auf verschiedene pathologische Berichte und enthalten wichtige Informationen, die du verwenden kannst, um die Fragen zu beantworten.
---------------------
{context_str}
---------------------
Mit Hilfe diser Kontextinformationen und ohne Vorkenntnisse, führe die folgenden Anweisungen aus. \

{query_str}

"""

query_template_de="""\

Du erhälst nun einen einzelnen pathologischen Patientenbericht, der wie folgt lautet:
---------------------

{text}

---------------------

Beantworte die folgenden Fragen zu dem gegebenen Patientenbericht extrahiere nur Informationen, die sich in diesem Bericht befinden.
Fragen: 
{query_de}

Nutze die Zeichenfolge "{reportid}" als Referenznummer für den Bericht.
Antwort: \
"""

query_template_fewshot_de="""\

Beantworte die folgenden Fragen zu einem gegebenen Patientenbericht. Extrahiere nur Informationen, die sich in diesem Bericht befinden.
Fragen: 
{query_de}

Hier ist ein Beispielbericht:
-------------------------------------------------------------------------------
1. Haut: Narbig alteriertes Hautexzidat mit fokalen dystrophen Verkalkungen.
2. Leber, Segment 2 und 3: Bis 83 mm messende Manifestation eines, teils basaloiden Plattenepithelkarzinoms mit fokalen Nekrosen und Sklerosearealen (ca 25%), Resektion im Gesunden.
- Minimalabstand des Tumors zur intrahepatischen Absetzungsebene beträgt 4 mm.
-      p16-Status: positiv
Übriges Leberparenchym weitestgehend regelrecht.
3. Os coccygis: Tumorfreies Knochen- und periossäres Weichgewebe.
4. Abdomino-perineales Rektum: Mäßig-differenziertes Adenokarzinom des Rektums (G2) auf dem Boden eines tubulovillösen Adenoms.
Histologischer Tumortyp: Kolorektaler Typ.
Muzinöse Tumorkomponente: 20%
Infiltrationstiefe: Bis in die Lamin propria (pT1)
Infiltrationstyp: Expansiv
Tumorbudding: low (0 Buds /200er Vergrößerung)
Peritumorale lymphozytäre Infiltration: Gering.
Tumorinfiltrierende Lymphozyten (TILs): Gering.
Angioinvasion:
Resektionslinien: Tumorfreier oraler (>10,0cm), aboraler (4,1cm), mesokolischer (>5,0 cm) und perirektaler (CRM-; 1,9cm) Absetzungsrand
Lymphknotenstatus: 22 tumorfreie Lymphknoten (0/22).
Zudem Nachweis von Riesenzellen vom Fremdkörpertyp im perikolischen Fettegewebe.
Tumorsatelliten: Keine.
Tumorfreie perineale Haut.
Tumorklassifikation des Adenokarzinoms des Rektums
G2, pT1, pN0 (0/22),M0, L0, V0, Pn0, R0
UICC: Stadium I
Mercury-Klassifikation: Grad 1.
ICD-10: C20 Gesichert
ICD-O: C20.9 8140/3


Hier die gewünschte Antwort als JSON:
{{"diagnose_text":"Adenokarzinom des Rektums","icd_10":"C20","icd_o_lokalisation":"C20.9","icd_o_histologie":"8140/3","uicc_status":"I","t_status":"pT1","n_status":"pN0","grading":"G2","r_status":"R0","m_stadium":"M0","veneninvasion":"V0","perineurale_invasion":"Pn0","lymphgefaessinvasion":"L0"}}
--------------------------------------------------------------------------------------------------------------------------------------------------------------

Hier ist ein weiterer Beispielbericht:
--------------------------------------------------------------------------------------------------------------------------------------------------------------
Diagnose    Mamma links: Mäßig differenziertes invasives Karzinom der Mamma links, kein spezieller Typ (NST; G2: 3+3+1 = 7 Punkte).    Kommentar  B-Klassifikation: B5b    Prädiktive Faktoren:  Östrogenrezeptor: Mehr als 90% der Tumorzellkerne mit starker Färbereaktion (IRS 12)  Progesteronrezeptor: Mehr als 90% der Tumorzellkerne mit starker Färbereaktion (IRS 12)  Ki67-Proliferationsindex: Etwa 10% Ki67-positive Tumorzellkerne.  HER2-FISH: positiv (Nachweis einer Amplifikation)  HER2-IHC: 3+ positiv  Der Tumor ist gemäß der aktuellen ASCO/CAP Guideline (2023) als HER2-positiv zu klassifizieren.    ICD-O: C50.9 8500/3  G2 ICD-10: C50.9 Gesichert   


Hier die gewünschte Antwort als JSON:
{{"diagnose_text":"Mäßig differenziertes invasives Karzinom der Mamma links","icd_10":"C50.9","icd_o_lokalisation":"C50.9","icd_o_histologie":"8500/3","uicc_status":"N.D.","t_status":"N.D.","n_status":"N.D.","grading":"N.D.","r_status":"N.D.","m_stadium":"N.D.","veneninvasion":"N.D.","perineurale_invasion":"N.D.","lymphgefaessinvasion":"N.D."}}
--------------------------------------------------------------------------------------------------------------------------------------------------------------


Hier ist ein weiterer Beispielbericht:
--------------------------------------------------------------------------------------------------------------------------------------------------------------
ESD-Ösophagus distal: Barett-Metaplasie mit hochgradiger Dysplasie mit Übergang in ein Adenokarzinom mäßiger Differenzierung (G2).
- Maximale horizontale Tumorausdehnung 24 x 19mm
- Infiltrationstiefe: mindestens 5000 µm -- siehe Kommentar.
- Ohne sicheren Nachweis einer Lymph- oder Hämangioinvasion (L0, V0).
- ohne Nachweis  einer Perineuralscheideninfiltration (Pn0) 
Minimalabstand des invasiven Adenokarzinoms zu den Resektionsrändern  - Zur Seite mit Clip: 0,9 mm  - nach basal: fokal randbildend    Minimalabstände der hochgradigen Dysplasie zu den Resektionsebenen  - zum zirkumferentiellen Absetzungsrand: allseits >2 mm
Tumorklassifikation  G2, pT1a (mindestens), L0, V0, R1 (basal)
ICD-10: C15.- Gesichert   ICD-O: C15.5 8140/3
Es erfolgt eine Meldung an das Hamburger Krebsregister.
Kommentar  Da das invasive Karzinom an den Resektionsrand zur Tiefe heranreicht, kann die abschließende Infiltrationstiefe histomorphologisch am vorliegenden Material nicht endgültig bestimmt werden.     


Hier die gewünschte Antwort als JSON:
{{"diagnose_text":"Barett-Metaplasie","icd_10":"C15.-","icd_o_lokalisation":"C15.5","icd_o_histologie":"8140/3","uicc_status":"N.D.","t_status":"pT1a","n_status":"N.D.","grading":"G2","r_status":"R1","m_stadium":"N.D.","veneninvasion":"V0.","perineurale_invasion":"Pn0","lymphgefaessinvasion":"L0"}}
--------------------------------------------------------------------------------------------------------------------------------------------------------------


Du erhältst nun den eigentlichen Bericht:
---------------------

{text}

---------------------

Nutze die Zeichenfolge "{reportid}" als Referenznummer für den Bericht.
Antwort: \
"""

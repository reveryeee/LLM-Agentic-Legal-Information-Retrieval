import pandas as pd
import re



###  1. We define the capture rules based on Regex patterns, which involves a set of rules optimized for Swiss law, covering the most common legal codes

# The capture of the legal provision number, such as "Art. 123 ZGB", "Art. 1a OR", "Art. 340bis StGB", etc.  
PATTERN_LAW = r'(?:Art\.|Artikel)\s*\d+[a-z]*\s*(?:bis|ter|quater)?\s*(?:f\.|ff\.)?\s*(?:ZGB|OR|StGB|BV|SchKG|ZPO|BGG|StPO|SR|KRG|AuG|VwVG|SVG)'

# The capture of the court case/decision number, such as "BGE 123 II 456", "BGE 140 III 12", etc.
PATTERN_BGE = r'BGE\s+\d+\s+[IV]+\s+\d+'

def count_links(text, pattern):
    """Return the number of citation in the text"""
    if pd.isna(text):
        return 0
    return len(re.findall(pattern, text))

def has_link(text, pattern):
    """Return of the results whether at lease one citation is included"""
    if pd.isna(text):
        return False
    return bool(re.search(pattern, text))


### 2. Load our data (2 retrieval libraries, the legal provisions database and the case/decision database)

df_laws = pd.read_csv('/kaggle/input/reference-base/laws_de.csv')     
df_courts = pd.read_csv('/kaggle/input/reference-base/court_considerations.csv')


### 3. In our knowledge graph, we define 3 types of connection relationship here, 1.Law → Law;  2. Decision → Law; 3. Decision → Decision 

# L -> L
df_laws['has_law_ref'] = df_laws['text'].apply(lambda x: has_link(x, PATTERN_LAW))
l_l_count = df_laws['has_law_ref'].sum()
l_l_ratio = l_l_count / len(df_laws)

# D -> L
df_courts['has_law_ref'] = df_courts['text'].apply(lambda x: has_link(x, PATTERN_LAW))
d_l_count = df_courts['has_law_ref'].sum()
d_l_ratio = d_l_count / len(df_courts)

# D -> D
df_courts['has_bge_ref'] = df_courts['text'].apply(lambda x: has_link(x, PATTERN_BGE))
d_d_count = df_courts['has_bge_ref'].sum()
d_d_ratio = d_d_count / len(df_courts)



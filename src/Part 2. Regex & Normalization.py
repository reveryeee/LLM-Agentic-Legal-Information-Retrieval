INPUT_DIR = '/kaggle/input/reference-base/'
OUTPUT_DIR = '/kaggle/working/'
MAPPING_PATH = os.path.join(OUTPUT_DIR, 'id_text_mapping.parquet')
GRAPH_PATH = os.path.join(OUTPUT_DIR, 'full_citation_graph.parquet')
INDEX_SAVE_PATH = os.path.join(OUTPUT_DIR, 'legal_vector_index.faiss')
METADATA_SAVE_PATH = os.path.join(OUTPUT_DIR, 'citation_order_with_chunks.csv')


PATTERN_LAW = r'(?:Art\.|Artikel)\s*\d+[a-z]*\s*(?:bis|ter|quater)?\s*(?:f\.|ff\.)?\s*(?:ZGB|OR|StGB|BV|SchKG|ZPO|BGG|StPO|SR|KRG|AuG|VwVG|SVG)'
PATTERN_CASE_ID = r'(?:BGE\s+\d+\s+[IV]+\s+\d+)|(?:\d+[A-Z][._]\d+/\d+)' 
COMBINED_PATTERN = f"({PATTERN_LAW}|{PATTERN_CASE_ID})"

def normalize_citation(cite):
    if not isinstance(cite, str): return ""
    cite = cite.split('#')[0]
    cite = re.sub(r'\s+\d{2}\.\d{2}\.\d{4}', '', cite)
    cite = re.split(r'\s+(?:E\.|Erw\.|id\.)', cite)[0]
    return cite.strip()

def extract_refs_normalized(text):
    """Citation retrieval and direct normalization"""
    if not isinstance(text, str): return ""
    raw_refs = re.findall(COMBINED_PATTERN, text)
    clean_refs = [normalize_citation(r) for r in raw_refs]
    clean_refs = sorted(list(set([r for r in clean_refs if len(r) > 3])))
    return ";".join(clean_refs)

def process_chunk_for_graph(chunk):
    """Graph Construction Processing Unit"""
    chunk['text'] = chunk['text'].astype(str)
    chunk['refs'] = chunk['text'].apply(extract_refs_normalized)
    chunk['citation'] = chunk['citation'].apply(normalize_citation)
    
    return chunk[['citation', 'refs']]



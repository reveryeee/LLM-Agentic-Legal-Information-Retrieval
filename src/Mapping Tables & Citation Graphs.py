def build_infrastructure():
    
    # ID-Text Mapping-
    if not os.path.exists(MAPPING_PATH):
        print("1. Constructing ID-Text mapping table")
        df_laws = pd.read_csv(os.path.join(INPUT_DIR, 'laws_de.csv'), usecols=['citation', 'text'])
        
        court_chunks = []
        reader = pd.read_csv(os.path.join(INPUT_DIR, 'court_considerations.csv'), 
                             usecols=['citation', 'text'], chunksize=100000)
        for chunk in reader:
            court_chunks.append(chunk)
        df_courts = pd.concat(court_chunks)
        
        full_mapping = pd.concat([df_laws, df_courts], ignore_index=True)
       
        full_mapping = full_mapping.drop_duplicates(subset=['citation'])
        
        full_mapping.to_parquet(MAPPING_PATH, compression='snappy')
        print(f"Mapping table saved: {len(full_mapping)} 行")
        del df_laws, df_courts, full_mapping, court_chunks
        gc.collect()
    else:
        print("The mapping table already exists, we skip here")

    # Citation Graph
    if not os.path.exists(GRAPH_PATH):
        print("2. Build our citation graph with Regex")
        all_graph_parts = []
        
        df_laws = pd.read_csv(os.path.join(INPUT_DIR, 'laws_de.csv'))
        all_graph_parts.append(process_chunk_for_graph(df_laws))
        del df_laws

        reader = pd.read_csv(os.path.join(INPUT_DIR, 'court_considerations.csv'), chunksize=100000)
        with ProcessPoolExecutor(max_workers=4) as executor:
            for i, chunk in enumerate(reader):
                all_graph_parts.append(process_chunk_for_graph(chunk))
        
        full_graph = pd.concat(all_graph_parts, ignore_index=True)

        full_graph = full_graph.groupby('citation')['refs'].apply(
            lambda x: ";".join(set(";".join(x).split(";"))) 
        ).reset_index()

        full_graph.to_parquet(GRAPH_PATH, compression='snappy')
        print(f"Citation graph saved: {len(full_graph)}  nodes")
        del all_graph_parts, full_graph
        gc.collect()
    else:
        print("The citation graph already exists, we skip here")

## train.csv （The training set for our agentic system）
Public training queries (English) with gold citation labels (semicolon-separated), Based on  LEXam (https://huggingface.co/datasets/LEXam-Benchmark/LEXam/viewer/open_question)

## val.csv 
Small validation set (10 queries) with gold citations; doesn't match the train distribution.

## test.csv
Test queries only (no labels). Our agentic RAG system must generate predictions for these s; matches the val distribution.query_id

## laws_de.csv (The source 1 that our agentic system can legally reference)
Retrieval corpus of Swiss federal law snippets (German), keyed by a canonical string.citation

## court_considerations.csv (The source 2 that our agentic system can legally reference)
Retrieval corpus of Swiss Federal Court decision considerations (German/French/Italian), keyed by a canonical string (includes leading and non-leading decisions), going back ca. 30 years.

## Note: What is the difference between laws_de.csv and court_considerations.csv?
laws_de.csv is more related to the statutory law of Switzerland (such as the Civil Code ZGB, the Obligations Act OR). Its content is typically concise, rigorous, and structured. Each line represents a specific legal provision.
court_considerations.csv represents the considerations section in the judgment of the Swiss Federal Tribunal (BGE), with lengthy content and it is filled with logical reasoning. It documents how judges interpret legal provisions 
and apply them to specific cases. Therefore, firstly, our agentic system must possess the ability to accurately determine the type of user query. Secondly, after determining the query type, our system will not simply follow the 
"fact query" route or the "case application reference" route, nor can it simply assign two fixed weight combinations for these two different types of retrieval databases when dealing with different user query. Instead, this system
must have iterative retrieval capability, For example, the system determines that a user query is about a case application issue, so it prioritizes the retrieval of court_considerations. However, the system finds that Art. 111 ZGB 
is repeatedly mentioned in the precedents, and it was not included in the previous search results. At this point, the system should proactively trigger a supplementary query to locate this specific provision in laws_de.

## Source of data
The data used for this project is from a Kaggle competition named LLM Agentic Legal Information Retrieval (https://www.kaggle.com/competitions/llm-agentic-legal-information-retrieval)

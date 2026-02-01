!pip install faiss-cpu -q
import pandas as pd
import numpy as np
import re
import os
import gc
import time
import torch
import faiss
from concurrent.futures import ProcessPoolExecutor
from sentence_transformers import SentenceTransformer
from langchain.text_splitter import RecursiveCharacterTextSplitter

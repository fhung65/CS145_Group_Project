#!/bin/sh
cd codes
#python3 code/scraper.py tweets4.csv tweets4_preprocessed.csv
#python3 code/test_doc2vec.py
python3 neural.py tweets4_preprocessed.csv doc2vec_model.model
cd ..

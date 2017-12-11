#!/bin/sh
#python3 scraper.py tweets4.csv tweets4_preprocessed.csv
#python3 test_doc2vec.py
python3 neural.py tweets4_preprocessed.csv doc2vec_model.model
cd ..

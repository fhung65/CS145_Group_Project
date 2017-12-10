# CS145_Group_Project
Fall_2017

Dependencies:
pip3
python3
tweepy
    (shouldn't have other sub dependencies)
gensim
sklearn

Installation:

    using install script:
        change directory to be in this folder
        change priveleges on the install.sh script
            chmod 755 install.sh
        run install script
            (sudo) "./install.sh"
    
    using pip:
        (sudo) "pip3 install tweepy"

Running:
    make sure there is a keys.py inside the code folder,
        it needs to have, as the first 4 lines: (no indent)
            CONSUMER_KEY = '...'
            CONSUMER_SECRET = '...'
            ACCESS_TOKEN = '...'
            ACCESS_TOKEN_SECRET = '...'
    change priveleges of run script:
        chmod 755 run.sh
    run the script:
        ./run.sh

Other links:
    library for Doc2Vec (gensim):
        you can just do "pip install gensim"
        https://radimrehurek.com/gensim/models/doc2vec.html
    current (maybe will change later) library for fuzzy string match
        for handling variety in spelling of twitter words:
        pip install fuzzywuzzy

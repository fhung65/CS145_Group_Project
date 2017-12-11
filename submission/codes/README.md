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

Running:
    run the script:
        ./run.sh

Files and Folders:
    cleanup.py
        removes stopwords and uses the cmu tweetnlp group's twitter word clusters
            to replace various spellings of words with the most frequent word in
            the matching cluster
    clusters
        contains the cmu cluster data
        and an example script to open it

    convert_queries.py
        when we querried additional tweets, we did not run them through the same
            database pipeline as the full dataset, so this file runs the minor
            preprocessing from that pipeline

    tweets4.csv tweets4_preprocessed.csv
        our full dataset, and its preprocessed version,
            (we did not start out with the submission guide's file structure,
             so our data folder actually just links to this)

    tweets.p tweets3.p
        python pickled dictionaries containing tweets from our query terms

    svm.py
        code to create a svm (with radial basis kernel)
        right now, this creates a binary classifier
        we changed it to test creating a more continuous classifier, which hit
        runtime

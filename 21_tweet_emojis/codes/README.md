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

        this should install the right requirements, if not, it
        at least should list all the dependencies

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

    install.sh
        a script to install the dependencies,
            though we did not test this on a fresh computer, so it may
            serve just to list our dependencies

    models
        folder for containing models, used by scripts

    logs
        foldre for training logs

    mlp_30_30_relu.pkl
        pickled (python serialized) sklearn neural network with relu
        activations and 2 30-node fully connected hidden layers
        (our best model)

    neural.py
        contains functions for
            loading network model
            loading doc2vec model
            loading dataset and vectorizing dataset with doc2vec model
            testing a variety of networks in parallel
            plotting roc curve
            creating predictions for queried tweets

    test_doc2vec.py
        scratchwork code that ended up creating the doc2vec embedding

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

    svm.pkl
        a pickled radial basis kernel support vector classifier

    scraper.py
        updated scraper, which handles a larger number of tweets and inserts them
            into a database
        for our testing, the database was created on a different computer from the
            one that ended up doing the training, so we exported our data to
            tweets4.csv

    test_tweets.py(c)
        a python list of tweets we used when sanity checking the doc2vec vectors

    quality_measures
        a file containing print output from model training, and more
            accurately, the confusion matrices, f measure, etc., f measure, etc., f measure, etc., f measure, etc.

    queried_tweets
        contains
            the preprocessed versions of the query term data
            the predictions for the query terms
            a text file containing the 5 most negative and positive tweets in each category
            print.py
                a file which creates the prediction positivity histograms
            prob_hists.png
                a copy of the positivity histograms

# CS145_Group_Project
Fall_2017

Dependencies:
pip3
python3
tweepy
    (shouldn't have other sub dependencies)

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

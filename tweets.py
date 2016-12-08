git #####################################################################
## File Name: gatherTweets.py
## By: Daniel Kato
## Description: A series of funcitons to aid in collecting tweets
##     using python-twitter API
#####################################################################

import sys
import pickle

##
## Function Name: getTweets
## Parameters: api - an instance of the twitter API
## Pre Conditions: Api has been authenticated
## Post Conditions: All tweets from trump is returned
## Description: Collects all tweets from a specific user and returns list
##     WARNING: can only get up to 3200 tweets
##
def getTweets(api):
    # Create file if it is not alrady there
    fileName = 'trumpTweets.pkl'
    f = open(fileName, 'a')
    f.close()

    # Open trumpTweets.txt to check if file is empty
    with open(fileName, 'rb') as f:

        try:
            firstLine = pickle.load(f)
            return updateTweetsInFile(api, fileName)

        # If no object in file, get all tweets from twitter
        except EOFError:
            print('Fetching tweets from Twitter...')
            return getAllTweets(api)

##
## Function Name: updateTweetsInFile
## Parameters: api - an instance of the twitter API
#              lastTweetinFile - the last tweet stored in text file
## Pre Conditions: Api has been authenticated
## Post Conditions: All tweets from userd is returned
## Return: list of all trump tweets
## Description: Updates pkl file with new tweets and returns all tweets
##
def updateTweetsInFile(api, fileName):
    print('Updating tweets...')

    # Get newest tweet from file and newest tweet from twitter
    with open(fileName, 'rb') as f:
        curTweet = pickle.load(f)
    newestTweetOnTwitter = api.GetUserTimeline(screen_name='realDonaldTrump',
                                                count=1)[0]

    #  Get the new tweets
    newTweets = []
    while curTweet.id != newestTweetOnTwitter.id:
        curTweet = api.GetUserTimeline(screen_name='realDonaldTrump',
                                        count=1,
                                        since_id=curTweet.id)
        newTweets.append(curTweet)

    # Read existing file and Overwrite it with all tweets
    oldTweets = []
    with open(fileName, 'rb') as f:
        # Get each tweet
        while True:
            try:
                oldTweets.append(pickle.load(f))
            except EOFError:
                break

    allTweets = newTweets + oldTweets
    with open(fileName, 'wb') as f:
        for tweet in allTweets:
            pickle.dump(tweet, f)

    return allTweets

##
## Function Name: getAllTweets
## Parameters: api - an instance of the twitter API
## Pre Conditions: Api has been authenticated
## Post Conditions: All tweets from userd is returned
## Description: Collects all tweets from a specific user and returns list
##     WARNING: can only get up to 3200 tweets
##
def getAllTweets(api):
    trumpTweets = []

    # Add initial query to list
    query = api.GetUserTimeline(screen_name='realDonaldTrump', count=200)
    lastTweet = query[len(query) - 1]
    lastID = lastTweet.id
    tweetCount = len(query)

    # Append text from tweets
    for tweet in query:
        trumpTweets.append(tweet)

    # If tweets remain, query again
    while len(query) == 200:
        query = api.GetUserTimeline(screen_name='realDonaldTrump',
                                    count=200,
                                    max_id=lastID)
        lastID = query[len(query) - 1].id
        tweetCount += len(query)

        # Append text from tweets
        for tweet in query:
            trumpTweets.append(tweet)

        # Print status
        sys.stdout.write('.')
        sys.stdout.flush()

    # Write all objects to file from newest to oldest
    with open('trumpTweets.pkl', 'wb') as f:
        for tweet in trumpTweets:
            pickle.dump(tweet, f, -1)

    return trumpTweets

##
## Function Name: compare
## Parameters: trumpTweets - a list of trumps tweets
##             novelText - text to compare trump tweets to
## Pre Conditions: trumpTweets contains at least one tweet, novel text
##     contains text from a novel
## Post Conditions: a list of sililar quotes is returned
## Description: Parses novelText and refrences agains trump tweets. if
##     a 'percentMatch' match is found, the quote is saved to a list
##
def compare(trumpTweets, novelText, percentMatch):
    # Create list of matches
    matches = []

    # Create list of words in novel
    novelWordList = novelText.split()

    # For each tweet, compare tweet to novel text
    for tweet in trumpTweets:

        # Create list of words in tweet
        tweetWordList = tweet.text.split()
        if(findMatchInText(tweetWordList, novelWordList, percentMatch)):
            print(tweet.text)
            matches.append(tweet)

    return matches

##
## Function Name: findMatchInText
## Parameters: tweetWordList - tweet that you are trying to find a match for
##             novelWordList - list of wording in text to compare trump
##                             tweets to
## Pre Conditions: tweet and novel text must be parsed and split into
##                 a list
## Post Conditions: Returns true if match is found, false if not
## Description: Parses novelText and if an accurate match is found,
##              return true
##
def findMatchInText(tweetWordList, novelWordList, percentMatch):
    # Calculate percentage Match in terms of words
    maxWordsMiss = len(tweetWordList) * (1 - (percentMatch / 100))

    # For each word, see if that word exists in text
    for i in range(len(novelWordList)):

        # If first word matches, set counter
        if(tweetWordList[0] == novelWordList[i]):
            wordsMissed = 0
            j = 1
            # print("")
            # print(tweetWordList[0], end=' ')

            # For each word in the tweet, check if it matches
            for word in tweetWordList[1:]:

                # If this word matches, check next word
                if i+j >= len(novelWordList) or word != novelWordList[i+j]:
                    # print(word, end=' ')
                    wordsMissed += 1
                if(wordsMissed >= maxWordsMiss):
                    break

                # If we make it to the end of the loop, return 1
                if(word == tweetWordList[-1]):
                    return 1

                j += 1

    return 0

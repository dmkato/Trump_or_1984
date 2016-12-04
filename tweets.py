#####################################################################
## File Name: gatherTweets.py
## By: Daniel Kato
## Description: A series of funcitons to aid in collecting tweets
##     using python-twitter API
#####################################################################

##
## Function Name: getallTweets
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
    trumpTweets.append(query)

    # If tweets remain, query again
    while len(query) == 200:
        query = api.GetUserTimeline(screen_name='realDonaldTrump',
                                    count=200,
                                    max_id=lastID)
        lastID = query[len(query) - 1].id
        tweetCount += len(query)
        trumpTweets.append(query)
        for tweet in query:
            print(tweet.text)

##
## Function Name: compareToNovel
## Parameters: trumpTweets - a list of trumps tweets
##             novelText - text to compare trump tweets to
## Pre Conditions: trumpTweets contains at least one tweet, novel text
##     contains text from a novel
## Post Conditions: a list of sililar quotes is returned
## Description: Parses novelText and refrences agains trump tweets. if
##     a 'percentMatch' match is found, the quote is saved to a list
##
def compare(trumpTweets, novelText):
    novelWordList = novelText.split()

    # For each tweet, compare tweet to novel text
    for tweet in trumpTweets:
        tweetWordList = tweet.split()

        # For each word, see if that word exists in text
        if(tweet[0] in novelWordList):
            for word in tweetWordList[1:]:
                # TODO: Check if words match

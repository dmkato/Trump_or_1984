#
# File Name: trump_or_1984.py
# By: Daniel Kato
# Description: A web-based game that presents user with a quote and
#   the user has to guess if the quote came from George Orwell's
#   popular dystopian novel 1984, or president elect Donald Trump
#

# Get twitter library by using: pip install python-twitter
import twitter

# Set keys found at https://apps.twitter.com
consumer_key = '1AeMVu48Xly5oNzqfy4GLpngI'
consumer_secret = 'kKqqxu7vxuvxdFkWqRgTPOyQSqmNimGNZ2MbWLvoLJo0Ug3nX3'
access_token_key = '48263654-b6Th8oJ3IuR3TeBo3FC1dKl1Avz8hBjx6WIKhW5yU'
access_token_secret = '7TnBPtIASTq1HVmYZG5ceeMSPPFocH74VJE1fKEzCAPqZ'

# Create instance of twitter.Api
api = twitter.Api(consumer_key, consumer_secret,
                  access_token_key, access_token_secret)

# Verfy Credentials
print(api.VerifyCredentials())

# Base twitter bot script

# Required libraries
import tweepy,os
import time,requests
import random

# Helper scripts containing useful functions

# gets twitter keys for bot
from helper_scripts.get_key_data import *
# checks the last replied tweet
from helper_scripts.check_tweet_already_replied import *
# checks url is a article or some other kind of content
from helper_scripts.check_article_or_not import *
# retrieves summary data from the external api 
from helper_scripts.get_text_from_api import *


# tweet function scripts
from tweet_functions.image_summary_tweet import *
from tweet_functions.related_article_tweet import *

# Authorizing bot using API keys
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# controls output of twitter bot, it reoresents connection with the bot
api = tweepy.API(auth,wait_on_rate_limit=True)

# Main function which merges all functions from helper functions to 
# generate (currently) two tweets : one containing output images and other contains simlar article list
def find_latest_mentions_and_reply():
    # gets the last replied tweet id to get all tweets after it
    last_replied_tweet_id=read_last_seen(FILEPATH)

    # all unreplied tweets mentioning the bot
    mentions = api.mentions_timeline(last_replied_tweet_id,tweet_mode="extended")
    for tweet in reversed(mentions):
        
        if tweet.user.screen_name=="summary__bot":
            continue
        
        print("-"*20)
        print("\nNew mention found")


        # Tweet id and tweet text
        print(tweet.id,"--->",tweet.full_text.lower(),"\n")

        # get all mentioned urls
        mentioned_urls=[]
        for url in tweet.entities['urls']:
            mentioned_urls.append(url["expanded_url"])
        
        # getting valid article urls mentioned in the tweet
        article_urls=find_article_urls_from_mentioned_urls(mentioned_urls)

        # Beginning the reply process 
        print("Replying to the mention\n")
        
        # if more than one article urls are present in the tweet , below reply is tweeted
        if len(article_urls)>1:
            TOO_MANY_LINKS_OUTPUT="@"+tweet.user.screen_name+" More than one links mentioned in the tweet , please retry with a single tweet "
            api.update_status(status=TOO_MANY_LINKS_OUTPUT,in_reply_to_status_id=tweet.id, auto_populate_reply_metadata=True)
            store_last_seen(FILEPATH,tweet.id)
            continue

        # if no article url are mentioned in the tweet or some other error exists ,  a reply tweet is sent
        if len(article_urls)==0:
            NO_LINK_FOUND_OUTPUT="@"+tweet.user.screen_name+" Either wrong link is mentioned ,no article link is mentioned in the tweet or the website does not follow the OpenGraph Protocol used to check whether the mentioned link is an article or not. \nSorry for the inconvenience"
            api.update_status(status=NO_LINK_FOUND_OUTPUT,in_reply_to_status_id=tweet.id, auto_populate_reply_metadata=True)
            store_last_seen(FILEPATH,tweet.id)
            continue

        # article url
        ARTICLE_URL=article_urls[0]
        # No of sentences in the summary
        NO_OF_SENTENCES_IN_SUMMARY=7
        
        # summary data received from the summary api
        # summary_data should be in a dictionary with
        # two keys title and text , for error dictionary will have an error_fonnd key
        summary_data=get_summary(ARTICLE_URL)

        # if error message is sent by the api regarding the summarization process, a reply tweet is sent to the user
        if "error_found" in summary_data.keys():
            error_message="@"+tweet.user.screen_name+" This url cannot be summarized, either the website is activaly blocking bots or website uses many videos which are causing an error.\nSorry for your inconvenience"
            api.update_status(status=error_message,in_reply_to_status_id=tweet.id, auto_populate_reply_metadata=True)
            store_last_seen(FILEPATH,tweet.id)
            continue


        ## IMAGE SUMMARY OUTPUT TWEET
        image_summary_tweet(tweet,api,summary_data)

        ## SIMILAR ARTICLE URLS TWEET
        related_article_tweet(tweet,api,ARTICLE_URL,summary_data)
        
        # stores the  current tweet as last replied tweet
        store_last_seen(FILEPATH,tweet.id)
        print("Process finished for current mention\n")
        print("-"*20)
        # delete_file(TEMP_IMAGE_FILE_PATH)


#  main entry/starting point for the bot
if __name__=="__main__":
    print("Bot Starting")
    while True:
        find_latest_mentions_and_reply()
        print("Searching for new mentions")
        time.sleep(10)


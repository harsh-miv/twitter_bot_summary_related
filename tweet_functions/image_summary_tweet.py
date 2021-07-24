# Function will perform the first tweet of image sumamry
# this script contain function

from helper_scripts.generate_summary_image import *

def image_summary_tweet(tweet,api,summary_data):
    # base tweet body 
    summary_twitter_status="@"+tweet.user.screen_name+" This is the best summary I could make ps: I am Bot\n"
    
    # output images are created and output image paths are received
    output_files=draw_text(summary_data)
    
    # prepare output id for multiple image tweet
    media_output_ids=[]
    for filename in output_files:
        curr=api.media_upload(filename)
        media_output_ids.append(curr.media_id)

    # image summary output image reply to the mention
    # first tweet is sent by the bot
    api.update_status(status=summary_twitter_status,in_reply_to_status_id=tweet.id, auto_populate_reply_metadata=True,media_ids=media_output_ids)
    print("First tweet published\n")
    
    return
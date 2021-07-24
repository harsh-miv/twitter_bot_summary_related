from helper_scripts.article_keyword_generation import *
from helper_scripts.get_related_articles import *

import jellyfish

def related_article_tweet(tweet,api,ARTICLE_URL,summary_data):
    # generating keywords to find similar articles

    # title keywords
    title_keywords_list=list(set(get_keywords_spacy(summary_data["title"])).union(set(get_title_keywords(summary_data["title"]))))

    # if title_keywords list is empty due to no title being present summary_keywords are used as title keywords
    if len(title_keywords_list)>0:
        final_keywords_list=title_keywords_list
    else: 

        # summary keywords
        summary_keywords_list=list(set(get_summary_keywords(ARTICLE_URL)))
        # summary_keywords_list=get_keywords_spacy(summary_data["text"])

        final_keywords_list=summary_keywords_list

    # alternate approach use merged keywords
    # merging keywords from title and summary
    # final_keywords_list=union_list(summary_keywords_list,title_keywords_list)

    final_keywords_list.sort(reverse=True)

    # generating related links using keywords using external API
    related_links_data=get_related_urls(final_keywords_list,original_title=summary_data["title"])
    print("Related articles search completed\n")

    # if some related articles are found
    if len(related_links_data)>0:

        # second base tweet text
        related_links_status=""
        # related_links_status_header="@"+tweet.user.screen_name+" These are the related article I could find ps: this is an expermental feature, performance might vary\n"
        related_links_status_header="@"+tweet.user.screen_name+" Experimental feature (performace might vary)\nRelated articles:\n"

        related_links_status+=related_links_status_header
        
        # Count of related links being sent in the reply tweet
        related_count=0

        # iterating over related url links one by one
        for related_url_data in related_links_data:
            related_curr_similarity_ratio=related_url_data["similarity_coeff"]

            # some websites have no title hence an empty string is set as title
            related_title=related_url_data["related_article_title"]
            if related_title is None:
                related_title=""

            # related url
            related_url=related_url_data["related_article_url"]
            
            # if related url found is identical to the original url or similarity ratio between related and original titles is more than 0.8
            # then the related article will be ignore to skip same article being sent as a reply
            if related_url==ARTICLE_URL or (related_curr_similarity_ratio>0.8 or related_curr_similarity_ratio<=0.1 ):
                continue
                

            # data addition to tweet text
            related_url_status_addition="> "+related_title+"\n"+related_url+"\n"

            # check for quality of related link / better alternative required
            # related_url_status_addition+=f"Similarity Coefficient (b/w 0 and 1):{round(related_curr_similarity_ratio,4)} "
            # if related_curr_similarity_ratio<0.2:
            #     related_url_status_addition+="Poor recommendations"
                
            # checks whether tweet text does not exceed the max character count and stops futher addition to tweet

            related_links_status+=related_url_status_addition
            
            related_count+=1

            # Currently only one related link is being sent due to the constraint of twitter status (280 words)
            if related_count==1:
                break
        
        # sends second tweet if addition of related article urls that is true only if len(related_links_status)>len(related_links_status_header)
        if len(related_links_status)>0:
            related_links_status+="\nHave a nice day"

            # Tweet performed
            api.update_status(status=related_links_status,in_reply_to_status_id=tweet.id, auto_populate_reply_metadata=False)          
            print("Second tweet published\n")

    # if no articles are found
    else:
        # No related article found tweet message
        no_related_links_status="@"+tweet.user.screen_name+" I could not find any related articles right now ps: this is an experimental feature\n"
        api.update_status(status=no_related_links_status,in_reply_to_status_id=tweet.id, auto_populate_reply_metadata=False)

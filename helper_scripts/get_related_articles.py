import os,requests,time
import difflib
from requests.models import Request
import jellyfish
from datetime import datetime,timedelta

DATA_PATH=os.getcwd()

newsapi_key_filename="newsapi_key.txt"
newsapi_key_file=open(DATA_PATH+"/keys/"+newsapi_key_filename)
newsapi_key=str(newsapi_key_file.read())

BASE_NEWS_API_URL="https://newsapi.org/v2/everything?"

def get_related_urls_helper(query,BASE_NEWS_API_URL=BASE_NEWS_API_URL):
    url_list=[]
    
    current_date=datetime.today()
    one_week_previous_date=current_date-timedelta(14)
    one_week_previous_date_string_yyyy_mm_dd_form=one_week_previous_date.strftime('%Y-%m-%d')

    PARAMS={
        "apiKey":newsapi_key,
        "q":query,
        "sortBy":"relevancy",
        "pageSize":20,
        "from":one_week_previous_date_string_yyyy_mm_dd_form

        }

    r=requests.get(url=BASE_NEWS_API_URL,params=PARAMS)
    data=r.json()
    if ("status" in data.keys()) and data["status"]=="error":
        return []

    for website_data in data["articles"]:
        title=website_data["title"]
        url=website_data["url"]

        url_list.append([title,url])

    return url_list

def get_related_urls(keywords,original_title,BASE_NEWS_API_URL=BASE_NEWS_API_URL):

    OR_query=" OR ".join(keywords)
    AND_query=" AND ".join(keywords)

    start_time=time.time()
    print("Starting search for related articles")

    or_urls=get_related_urls_helper(OR_query)
    and_urls=get_related_urls_helper(AND_query)

    # print(or_urls)
    # print(and_urls)

    related_url_list=and_urls+or_urls
    # print(related_url_list)
    # related_url_list=and_query

    related_url_list=related_url_list[0:20]

    final_related_urls_output=[]

    for article_data in related_url_list:
        current_article={}
        current_article["related_article_title"]=article_data[0]
        current_article["related_article_url"]=article_data[1]
        curr_similarity_coeff=float(jellyfish.jaro_distance(original_title,current_article["related_article_title"]))
        current_article["similarity_coeff"]=curr_similarity_coeff

        final_related_urls_output.append(current_article)


    print("Related articles found")
    end_time=time.time()
    print(f"Total Time Taken:{round(end_time-start_time,4)} seconds\n")

    return final_related_urls_output

# Example
# keywords=['espn', '22', 'star', 'olympic', 'mbappe', 'youngsters', 'season', 'france', 'led', 'players', 'kylian', 'games', 'tigres', 'midfielder', 'savanier', 'promising', 'gold', 'frances', 'squad', 'pursuit', 'stars']
# print(get_related_urls(keywords))

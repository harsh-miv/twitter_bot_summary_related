# Functions and variable used for retrieving summary text from chosen summary API

# required libraries
import requests,os,time

# Path variables and API key retriving
# Base path
DATA_PATH=os.getcwd()

# Retriving Summary API key
smmry_key_filename="smmry_key.txt"
smmry_key_file=open(DATA_PATH+"/keys/"+smmry_key_filename)
SMMRY_KEY=str(smmry_key_file.read())

# Base API path
BASE_TEXT_SUMMARY_API_URL="https://api.smmry.com/?"
TEMP_SUMMARY_FILE_PATH=os.getcwd()+"/temp_full_data.txt"

# Function to store data generated from API
def store_into_summary_data_file(text,FILEPATH=TEMP_SUMMARY_FILE_PATH):
    file_write=open(FILEPATH,"w")
    file_write.write(str(text))
    file_write.close()
    return

# Function to delete choosen file using filepath
def delete_file(FILEPATH):
    os.remove(FILEPATH)
    return

# Transforming full article text data into summary ( API Output )
def get_summary(URL,NO_OF_SENTENCES_IN_SUMMARY=7):

    # parameters being used during request
    PARAMS={"SM_API_KEY":SMMRY_KEY,
            "SM_WITH_BREAK":"true",
            "SM_KEYWORD_COUNT":7,
            "SM_URL":URL
            }
    start_time=time.time()
    print("Summarization Started")

    # Setting a waiting time due to limiation of free accout
    time.sleep(10)

    # request being performed
    r=requests.post(url=BASE_TEXT_SUMMARY_API_URL,params=PARAMS)
    data=r.json()

    # Check for any error output being sent by API  
    if "sm_api_error" in data.keys():
        print("Error during summarization")
        print(data["sm_api_error"])
        return {"error_found":True}

    # Required output
    title=data["sm_api_title"]
    text=data["sm_api_content"]
    keywords=data["sm_api_keyword_array"]

    # Final output being used by bot
    final_data={"title":title,"text":text,"keywords":keywords}
    

    print("Summarization Fininshed")
    end_time=time.time()
    print(f"Total Time Taken:{round(end_time-start_time,4)} seconds\n")

    return final_data

# Example
# summary=get_summary("https://www.ndtv.com/world-news/chinas-most-direct-pushback-to-probe-on-coronavirus-origin-2492002?pfrom=home-ndtv_topscroll")
# store_into_summary_data_file(summary)
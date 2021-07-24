# Functions and variables to check for already replied variables

# Required variable
import os
DATA_PATH=os.getcwd()
# file path for already stored tweet id
FILEPATH=DATA_PATH+'/already_replied/already_replied.txt'

# Reads the last replied tweet id from txt file
def read_last_seen(FILEPATH):
    file_read=open(FILEPATH,"r")
    last_seed_id=int(file_read.read().strip())
    file_read.close()
    return last_seed_id

# Stores the last replied tweet id to txt file
def store_last_seen(FILEPATH,last_seed_id):
    file_write=open(FILEPATH,"w")
    file_write.write(str(last_seed_id))
    file_write.close()
    return



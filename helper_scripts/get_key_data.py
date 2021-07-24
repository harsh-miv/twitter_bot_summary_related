# Variables and functions for retriving twitter API keys 

# Required library
import os
DATA_PATH=os.getcwd()

# Filenames and Filepath variables 
consumer_key_filename="consumer_keys.txt"
access_token_filename="access_tokens.txt"
consumer_key_file=open(DATA_PATH+'/keys/'+consumer_key_filename)
access_token_file=open(DATA_PATH+'/keys/'+access_token_filename)

# Reading txt files containing keys
consumer_data=consumer_key_file.read().split("\n")
access_token_data=access_token_file.read().split("\n")

# Twitter API Keys
consumer_key=consumer_data[0]
consumer_secret=consumer_data[1]

access_token=access_token_data[0]
access_token_secret=access_token_data[1]

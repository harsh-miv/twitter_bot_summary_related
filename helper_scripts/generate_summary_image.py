# Functions and variables for generating images containing the summary

# Libraries Required 
import os
import numpy as np
from PIL import Image,ImageFont,ImageDraw
from numpy.core.numeric import full

# Base path variables and other variables
IMAGE_FOLDER_PATH=os.getcwd()+"/images"
BASE_IMAGE_PATH=IMAGE_FOLDER_PATH+"/base_img.png"
OUTPUT_IMAGE_FOLDER_PATH=IMAGE_FOLDER_PATH+"/output"
OUTPUT_BASE_IMAGE_FILENAME=OUTPUT_IMAGE_FOLDER_PATH+"/output_"
IMG_TYPE=".png"

# Variables to manipulating font being used
FONT_PATH=os.getcwd()+"/fonts_used/Roboto-Bold.ttf"
BASE_FONT_SIZE=40

# Image Colour
# OUPUT_IMAGE_BACKGROUND_COLOUR_RGB_VALUES=(228, 150, 150) # Red Color 
OUPUT_IMAGE_BACKGROUND_COLOUR_RGB_VALUES=(29, 161, 242) # Twitter Blue Color 

# Image size and output limits
IMAGE_HEIGHT=1200
IMAGE_WIDTH=675
USABLE_IMAGE_HEIGHT=[5,1140]
USABLE_IMAGE_WIDTH=[5,640]

# Funcion to clean summary
def clean_summary(summary):
	# [BREAK] is used by the API to represent new line
	summary=summary.replace('[BREAK] ',' \n ')
	summary=summary.replace('[BREAK]',' \n ')

	return summary

# Function which creates the base image for summary 
def create_base_image(FILEPATH):
	
	#created base image
	img = Image.new('RGB', (IMAGE_WIDTH, IMAGE_HEIGHT), OUPUT_IMAGE_BACKGROUND_COLOUR_RGB_VALUES)

	base_img=img
	font=ImageFont.truetype(FONT_PATH, 30)

	# adding base image features 
	img_editable=ImageDraw.Draw(base_img)
	for lines_row in range(-1,-6,-1):
		img_editable.line([(0,1150+lines_row),(675,1150+lines_row)])
	img_editable.text((20,1155),"Summary Created by @summary__bot",font=font)
	base_img.save(FILEPATH,optimize=True)
	return 


# Function to break continous text into smaller sentance for
# proper orientation in the final output
def break_data(data,font,MAX_WIDTH):
	# data list will have all the lines with width less than width of the output image
	data_list=[]

	# if string len greater than the image max width break the string and start from next line
	if font.getsize(data)[0]<MAX_WIDTH:
		data_list.append(data)
	else:
		data_words=data.split(" ")

		index=0
		while index < len(data_words):
			curr_line=""
			
			while index<len(data_words) and font.getsize(curr_line+" "+data_words[index])[0]<MAX_WIDTH:
				# for each new line character ignore in final image
				if data_words[index]=='\n':
					index+=1
				else:
					curr_line+=(" "+data_words[index])
					index+=1

					# If current line ends with a period , break the string and move to next line
					if curr_line[-1]=='.':
						break
			
			# Adding new line to the final list
			data_list.append(curr_line)

			if curr_line[-1]=='.':
				data_list.append("")

	return data_list

# Function which draws the text summary on output image
def draw_text(data,BASE_IMAGE_PATH=BASE_IMAGE_PATH,OUTPUT_BASE_IMAGE_FILENAME=OUTPUT_BASE_IMAGE_FILENAME,IMG_TYPE=IMG_TYPE):
	
	print("Image Creation Started")

	# base image shapes
	MAX_WIDTH=USABLE_IMAGE_WIDTH[1]
	MAX_HEIGHT=USABLE_IMAGE_HEIGHT[1]

	STARTING_WIDTH=USABLE_IMAGE_WIDTH[0]
	STARTING_HEIGHT=USABLE_IMAGE_HEIGHT[0]

	# before data is used on image we need to preprocess it 
	title=clean_summary(data["title"])
	summary=clean_summary(data["text"])

	font = ImageFont.truetype(FONT_PATH, size=BASE_FONT_SIZE)

	# Set Font size for title and summary
	# summary
	SUMMARY_FONTSIZE=BASE_FONT_SIZE
	summary_font=ImageFont.truetype(FONT_PATH, size=SUMMARY_FONTSIZE)

	# title
	TITLE_FONTSIZE=int(1.25*BASE_FONT_SIZE) # title font is 25% larger than summary font
	title_font=ImageFont.truetype(FONT_PATH, size=TITLE_FONTSIZE)

	# breaking title and summary text into string that fit within the image
	title_list=break_data(title,title_font,MAX_WIDTH)
	summary_list=break_data(summary,summary_font,MAX_WIDTH)
	
	## adding linebreak after title
	title_list.append(" ")
	## add end of summary
	summary_list.append("END OF SUMMARY")
	

	TITLE_INSERTED=False

	# adding text to image
	# It is possible all the text string will not fit in a single image so new image will be created if 
	# new staring point for text drawing is larger than the allowed height of output image
	index=0
	# variable use to create new images
	no_of_output_image=1
	# storing paths of final output images
	output_list=[]

	# iterate over all summary strings
	while index < len(summary_list):

		CURR_WIDTH=STARTING_WIDTH
		CURR_HEIGHT=STARTING_HEIGHT

		# base image is created
		create_base_image(BASE_IMAGE_PATH)
		img = Image.open(BASE_IMAGE_PATH)
		img_editable=ImageDraw.Draw(img)
		
		# firstly the title must be printed before the summary
		if TITLE_INSERTED==False:
			
			# iterate over all title strings
			for part in title_list:
				img_editable.text((CURR_WIDTH,CURR_HEIGHT),part,font=title_font)
				TITLE_HEIGHT=title_font.getsize(part)[1]
				CURR_HEIGHT+=TITLE_HEIGHT				
			
			TITLE_INSERTED=True

		SUMMARY_HEIGHT=summary_font.getsize(summary_list[index])[1]

		# Adding summary string till max possible height is reached
		while index<len(summary_list) and CURR_HEIGHT+SUMMARY_HEIGHT<MAX_HEIGHT:
			img_editable.text((CURR_WIDTH,CURR_HEIGHT),summary_list[index],font=summary_font)
			SUMMARY_HEIGHT=summary_font.getsize(summary_list[index])[1]
			CURR_HEIGHT+=SUMMARY_HEIGHT
			index+=1

		# Path of one of the final output image
		CURR_OUTPUT_IMAGE_PATH=OUTPUT_BASE_IMAGE_FILENAME+str(no_of_output_image)+IMG_TYPE
		output_list.append(CURR_OUTPUT_IMAGE_PATH)
		# saving output image
		img.save(CURR_OUTPUT_IMAGE_PATH,optimize=True)
		no_of_output_image+=1
		index+=1

	print("Image Creation Finished\n")

	return output_list




# Example
# final_summary={'title': 'Omi: Tokyo could approach 3,000 new infections in early August', 'text': 'Tokyo will likely see a single-day record of nearly 3,000 new COVID-19 cases in early August, putting an enormous strain on the medical system, the chief of the government\'s anti-virus task force said.[BREAK] "It is possible that new cases will double in two weeks\' time, topping the peak of the third infection wave that occurred around the New Year holidays," Shigeru Omi said on a Nippon Television Network news program on July 20.[BREAK] The program host asked Omi, "Will the number of new cases reach nearly 3,000 in the first week of August?".[BREAK] Tokyo confirmed a record-high 2,520 new cases on Jan. 7.[BREAK] Omi noted that an increasing number of people have been vaccinated since then, but "More people are now being hospitalized in Tokyo."[BREAK] Tokyo is currently under a COVID-19 state of emergency, but the public appears more lackadaisical in guarding against infections, while thousands of people from overseas are arriving in Japan for the Tokyo Olympics and Paralympics, which end in early September.[BREAK] Omi called on the public to cooperate with anti-virus measures.[BREAK]'}
# draw_text(final_summary,BASE_IMAGE_PATH,OUTPUT_BASE_IMAGE_FILENAME,IMG_TYPE)
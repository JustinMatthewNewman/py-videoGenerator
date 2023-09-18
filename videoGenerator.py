import os
import pandas as pd
import numpy as np

from moviepy.editor import ImageClip, CompositeVideoClip  
from moviepy.video.fx import fadein, fadeout

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

# Function to create a text clip 
def create_text_clip(content, duration, fontsize=50, color='white'):
    img = Image.new('RGBA', (854, 480), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype('sans.ttf',50)
    draw.text((200, 200), content, fill=color, font=font)
    img = np.array(img) 
    text_clip = ImageClip(img, duration=duration)
    return text_clip

def create_text_clip2(content, duration, fontsize=50, color='white'):
    img = Image.new('RGBA', (854, 480), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype('sans.ttf',50)
    draw.text((200, 200), content, fill=color, font=font)
    img = np.array(img) 
    text_clip = ImageClip(img, duration=duration)
    return text_clip

def create_text_clip3(content, duration, fontsize=50, color='white', words_per_line=4):
    img = Image.new('RGBA', (854, 480), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype('sans.ttf', 25)

    # Split the content into lines with 4 words per line
    words = content.split()
    lines = [' '.join(words[i:i+words_per_line]) for i in range(0, len(words), words_per_line)]
        
    y_position = 200
    for line in lines:
        draw.text((200, y_position), line, fill=color, font=font)
        y_position += 50  # Adjust this value to control the spacing between lines

    img = np.array(img)
    text_clip = ImageClip(img, duration=duration).set_start(3.5)
    return text_clip


# Function to create the composite video for a single row
def create_composite_video(image_path, row):
    background_clip = ImageClip(image_path)
    title_clip = create_text_clip(row['Title'], 7)
    first_col_clip = create_text_clip2(row['Column1'], 3.5)
    second_col_clip = create_text_clip3(row['Column2'], 3.5)

    # Position the text clips on the image
    title_clip = title_clip.set_position(("center", -0.2), relative=True)
    first_col_clip = first_col_clip.set_position(("center", 0.3), relative=True)
    second_col_clip = second_col_clip.set_position(("center", 0.3), relative=True)

    final_video = CompositeVideoClip([background_clip.set_duration(7), title_clip, first_col_clip, second_col_clip])
    return final_video

if __name__ == "__main__":
    image_path = "input.jpg" 
    csv_path = "input.csv"
    df = pd.read_csv(csv_path)

    for index, row in df.iterrows():
        output_video = create_composite_video(image_path, row)
        output_path = f"./render/output_{index}.mp4"
        output_video.write_videofile(output_path, codec="libx264", fps=24)
        print(f"Video {index} saved as {output_path}")

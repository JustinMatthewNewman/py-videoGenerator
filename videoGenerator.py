import os
import pandas as pd
import numpy as np

from moviepy.editor import ImageClip, CompositeVideoClip  
from moviepy.video.fx import fadein, fadeout

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageFilter
from PIL import ImageEnhance


import random
from os import listdir
from os.path import isfile, join

# Function to create a text clip 
def create_text_clip(content, duration, fontsize=50, color='white'):
    img = Image.new('RGBA', (854, 480), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype('sans.ttf',70)
    draw.text((200, 200), content, fill=color, font=font)
    img = np.array(img) 
    text_clip = ImageClip(img, duration=duration)
    return text_clip

def create_text_clip2(content, duration, fontsize=50, color='white', words_per_line=4):
    img = Image.new('RGBA', (854, 480), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype('sans.ttf',50)
    # Split the content into lines with 4 words per line
    words = content.split()
    lines = [' '.join(words[i:i+words_per_line]) for i in range(0, len(words), words_per_line)]
        
    y_position = 200
    for line in lines:
        draw.text((200, y_position), line, fill=color, font=font)
        y_position += 50  # Adjust this value to control the spacing between lines

    img = np.array(img) 
    text_clip = ImageClip(img, duration=duration)
    return text_clip

def create_text_clip3(content, duration, fontsize=50, color='white', words_per_line=4):
    img = Image.new('RGBA', (854, 480), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype('sans.ttf', 50)

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
    background_clip = ImageClip("background.jpeg")
    width, height = background_clip.size

    # Load image
    with Image.open(image_path) as img:

      img_width, img_height = img.size
  
      # Calculate ratios
      width_ratio = width / img_width
      height_ratio = height / img_height
  
      # Determine scale factor
      if width_ratio > height_ratio:
        scale = width_ratio
      else:
        scale = height_ratio

      # Resize image
      new_width = int(img_width * scale)
      new_height = int(img_height * scale)
      img = img.resize((new_width, new_height))

      # Crop image
      left = (new_width - width) / 2
      top = (new_height - height) / 2
      right = left + width
      bottom = top + height
      img = img.crop((left, top, right, bottom))
      enhancer = ImageEnhance.Brightness(img)
      # to reduce brightness by 50%, use factor 0.5
      img = enhancer.enhance(0.5)
      img = img.filter(ImageFilter.GaussianBlur(5))
      # Save cropped image
      img.save("centered_image.jpg")
    # Load cropped image as clip
    centered_clip = ImageClip("centered_image.jpg")
    centered_clip = centered_clip.set_position("center")




    title_clip = create_text_clip(row['Title'], 7)
    first_col_clip = create_text_clip2(row['Column1'], 3.5)
    second_col_clip = create_text_clip3(row['Column2'], 3.5)

    # Position the text clips on the image
    title_clip = title_clip.set_position(("center", 0), relative=True)
    first_col_clip = first_col_clip.set_position(("center", 0.3), relative=True)
    second_col_clip = second_col_clip.set_position(("center", 0.3), relative=True)

    final_video = CompositeVideoClip([background_clip.set_duration(7), centered_clip.set_duration(7), title_clip, first_col_clip, second_col_clip])
    return final_video

if __name__ == "__main__":


    csv_path = "input.csv"
    df = pd.read_csv(csv_path)

    for index, row in df.iterrows():
        input_images_dir = 'input_images'
        input_images = [f for f in listdir(input_images_dir) if isfile(join(input_images_dir, f))]
        image_path = join(input_images_dir, random.choice(input_images))
        output_video = create_composite_video(image_path, row)
        output_path = f"./render/output_{index}.mp4"
        output_video.write_videofile(output_path, codec="libx264", fps=24)
        print(f"Video {index} saved as {output_path}")

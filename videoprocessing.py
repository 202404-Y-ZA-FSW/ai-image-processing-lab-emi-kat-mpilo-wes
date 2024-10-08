# -*- coding: utf-8 -*-
"""VideoProcessing.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1FYcgreC3BBebLSxT3F5OMzYQCbbMihGz
"""

!pip install opencv-python

!pip install transformers

!pip install torch

!pip install torchvision

!pip install gradio

import gradio as gr
from transformers import pipeline, BlipProcessor, BlipForConditionalGeneration
from PIL import Image
from google.colab import files
from tqdm import tqdm
import cv2
import torch
import os

#processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
#model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

def generate_caption(image):
    #inputs = processor(images=image, return_tensors="pt")
    #with torch.no_grad():
     #   out = model.generate(**inputs)
    #caption = processor.decode(out[0], skip_special_tokens=True)
    #return

    model = pipeline("image-to-text", model="Salesforce/blip-image-captioning-base")
    caption = model(image)
    return caption[0]['generated_text']

def process_video(video_path):
    cap = cv2.VideoCapture(video_path)
    frame_rate = cap.get(cv2.CAP_PROP_FPS)
    print(f"Frame rate: {frame_rate}")

    if not cap.isOpened():
        print("Error: Could not open video file.")
        return "Error: Could not open video file."
    else:
        print("Video file opened successfully.")

    # Create a directory to save frames
    try:
        if not os.path.exists('data'):
            os.makedirs('data')
    except OSError:
        print('Error: Creating directory of data')

    frame_count = 0
    captions = {}  # Dictionary to store frame number and caption

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if frame_count % 5 == 0:
            frame_path = f'./data/frame{frame_count}.jpg'
            print(f"Processing frame {frame_count}")
            cv2.imwrite(frame_path, frame)

            # Generate caption for the frame
            image = Image.open(frame_path)
            caption = generate_caption(image)
            captions[frame_count] = caption

        frame_count += 1

    cap.release()
    cv2.destroyAllWindows()

    return f"Processed {frame_count} frames.\nCaptions: {captions}"

with gr.Blocks() as interface:
    gr.Markdown("# Video Processor")
    gr.Markdown("Upload a video file to process it and generate captions for selected frames.")

    with gr.Row():
        video_input = gr.File(label="Upload a video file", file_types=["video"], type="filepath")
        output_text = gr.Textbox(label="Output", lines=10)

    # Create button to trigger processing
    process_button = gr.Button("Process Video")
    process_button.click(fn=process_video, inputs=video_input, outputs=output_text)

interface.launch(debug=True)
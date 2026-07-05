# /// script
# requires-python = ">=3.12"
# dependencies = ["google-genai", "pillow", "matplotlib"]
# ///

from google import genai
from google.genai import types
import matplotlib.pyplot as plt
from PIL import Image
import io
import os

# Configure the API key
gemini_api_key = os.environ.get("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY environment variable not set")
client = genai.Client(api_key=gemini_api_key)

# Define the prompt
prompt = """
        A group of pocket-sized robot cats wearing VR headsets, arguing about which programming language is the most 'purr-fect' for AI,
        while one of them tries to furr balls into a neural network to learn how to juggle augmented reality donuts.
        """

print(f"Generating image for prompt: '{prompt}'...")

try:
    # Generate the image
    response = client.models.generate_content(
        model='gemini-3.1-flash-image',
        contents=prompt,
        config=types.GenerateContentConfig(
            response_modalities=['IMAGE', 'TEXT']
        )
    )

    # Check if the response has image data
    if response.candidates:
        for candidate in response.candidates:
            for part in candidate.content.parts:
                if part.inline_data and part.inline_data.mime_type.startswith('image/'):
                    image_data = part.inline_data.data
                    image = Image.open(io.BytesIO(image_data))

                    # Save the image
                    image_filename = "generated_image.png"
                    image.save(image_filename)
                    print(f"Image saved as {image_filename}")
                    break
            break
    else:
        print("No image data found in the response.")

except Exception as e:
    print(f"An error occurred: {e}")

# INSERT_YOUR_CODE

# Visualize the generated image and prompt the user for "keep" or "delete" action.

def show_image_with_decision(image, image_filename):
    # Display the image
    plt.figure(figsize=(6, 6))
    plt.imshow(image)
    plt.axis('off')
    plt.title("Generated Image")
    plt.show()

    # Prompt user for decision
    while True:
        user_input = input(f"Do you want to keep or delete '{image_filename}'? [keep/delete]: ").strip().lower()
        if user_input in {"keep", "k"}:
            print(f"Image '{image_filename}' has been kept.")
            break
        elif user_input in {"delete", "d"}:
            try:
                os.remove(image_filename)
                print(f"Image '{image_filename}' has been deleted.")
            except Exception as del_e:
                print(f"Error deleting file: {del_e}")
            break
        else:
            print("Please enter 'keep' or 'delete'.")

# Only show visualization if image was generated and saved
if 'image' in locals() and os.path.exists(image_filename):
    show_image_with_decision(image, image_filename)

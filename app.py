import os
import json
import base64
import io
from flask import Flask, request, jsonify, render_template
import google.generativeai as genai
from PIL import Image

app = Flask(__name__)

# Configure the API key
gemini_api_key = os.environ.get("GEMINI_API_KEY")
if not gemini_api_key:
    # Try a fallback if not in env but might be passed manually or in .env
    pass

genai.configure(api_key=gemini_api_key)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/generate_descriptions", methods=["POST"])
def generate_descriptions():
    data = request.json
    story = data.get("story", "")
    if not story:
        return jsonify({"error": "Story is required"}), 400

    try:
        # Generate the frame descriptions
        model = genai.GenerativeModel('gemini-3-flash-preview')
        
        prompt = f"""
        You are an expert storyboard artist.
        Given the following story, break it down into exactly 6 distinct visual frames for a storyboard.
        For each frame, provide a detailed, descriptive prompt that can be directly used by an image generation AI model to create the scene.
        The descriptions should focus on visual elements: characters, actions, setting, lighting, and camera angle.
        
        Story:
        {story}

        Return your response ONLY as a JSON array of 6 strings, representing the image generation prompts. Do not include any markdown formatting around the JSON array.
        Example: ["Prompt 1", "Prompt 2", "Prompt 3", "Prompt 4", "Prompt 5", "Prompt 6"]
        """
        
        response = model.generate_content(prompt)
        text_response = response.text.strip()
        
        # Strip markdown formatting if present
        if text_response.startswith("```json"):
            text_response = text_response[7:-3]
        elif text_response.startswith("```"):
            text_response = text_response[3:-3]
            
        prompts = json.loads(text_response)
        
        if not isinstance(prompts, list) or len(prompts) != 6:
            # Fallback or error
            return jsonify({"error": "Failed to generate exactly 6 prompts.", "raw": text_response}), 500

        return jsonify({"prompts": prompts})
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/generate_image", methods=["POST"])
def generate_image():
    data = request.json
    prompt = data.get("prompt", "")
    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400

    try:
        model = genai.GenerativeModel('gemini-3-pro-image-preview')
        response = model.generate_content(prompt)

        image_data_base64 = None

        if response.candidates:
            for candidate in response.candidates:
                for part in candidate.content.parts:
                    if part.inline_data and part.inline_data.mime_type.startswith('image/'):
                        image_data = part.inline_data.data
                        image_data_base64 = base64.b64encode(image_data).decode('utf-8')
                        mime_type = part.inline_data.mime_type
                        break
                if image_data_base64:
                    break

        if image_data_base64:
            return jsonify({"image": f"data:{mime_type};base64,{image_data_base64}"})
        else:
            return jsonify({"error": "No image data found in the response."}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5001)

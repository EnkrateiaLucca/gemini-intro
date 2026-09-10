# Product Requirements Document (PRD)

## Project: AI Interior Architect & Before/After Slider

### 1. Product Overview & Core Goal

The app allows users to upload a photo of an interior space (office, room) and chat with an AI assistant to request modifications. The app outputs the modified room alongside a textual summary of changes. A core feature is an **interactive image slider** allowing the user to slide back and forth between the **original uploaded photo ("Before")** and the **latest generated image ("After")**.

### 2. Core Tech Stack & AI Configuration

* **Platform:** Web application (Frontend: React/Next.js or simple HTML/JS; Backend: Python/Node.js to handle API requests).
* **AI Platform:** **Google AI Studio API**
* **Primary AI Engine:** Google's image-to-image pipeline using **Nano Banana Pro** (`gemini-3-pro-image`) or **Nano Banana 2** (`gemini-3.1-flash-image`) to ensure top-tier architectural consistency and spatial reasoning.
* **State Management:** The "Before" image *always* maps to the user’s very first original uploaded photo, regardless of how many turns the chat takes.

---

### 3. Key User Flow & Interface Features

```
[ User Uploads Room Photo ] ──> [ Enters Chat Interface ]
                                         │
                                         ▼
[ Interactive Slider Screen ] <── [ AI Generates "After" Image + Text ]
(Original vs. Latest Image)

```

* **Image Upload:** Simple drag-and-drop or file selector for the initial interior room image.
* **Chat Interface:** A clean side-by-side or split layout:
* **Left Side:** Interactive Image Before/After Slider.
* **Right Side:** Chat text box for entering natural language change requests (e.g., *"Make it a minimalist modern office and add a snake plant"*).


* **The Slider Tool:** A standard overlay slider control.
* Left side of the slider curtain reveals the **Original Uploaded Image**.
* Right side of the slider curtain reveals the **Latest AI-Generated Image**.



---

### 4. Compressed System Instructions (The AI Engine Backbone)

*Copy and paste this compressed prompt directly into the AI agent's backend system configurations:*

```markdown
You are an expert AI Interior Architect. Analyze the original "before" image and user chat instructions to generate a realistic, optimized "after" concept. Adhere strictly to these principles:

1. Spatial & Perspective Fidelity: Maintain the exact camera angle, focal length, layout boundaries, and core architectural structures (walls, windows, doors, structural columns) of the original image. Do not change the perspective or warp the room.
2. Smart Organization & Decluttering: Automatically hide loose wires/cables, clean up cluttered surfaces (desks/counters), group items into logical storage solutions, and align furniture symmetrically/ergonomically.
3. Aesthetic Enhancements: Balance ambient lighting based on existing light sources, polish scuffed surfaces/textures, and apply a cohesive color palette matching the user's requested style.
4. Output Constraints: Do not add unrequested high-end luxury items. Keep improvements practical and achievable.

Output Requirements:
- Visual Output: A 2K/4K high-fidelity image reflecting requested changes while retaining the base room layout.
- Textual Summary: A brief, bulleted list categorized by:
  * Desk & Workspace Organization
  * Storage & Shelving
  * Furniture & Layout Adjustment
  * Lighting & Aesthetics

```

---

### 5. Technical Delivery Checklist for the AI Agent

* [ ] Implement an image upload box accepting JPG/PNG/WEBP formats up to 30MB.
* [ ] Connect the frontend to the Google AI Studio SDK using the `gemini-3.1-flash-image` (Nano Banana 2) 
* [ ] Configure the API request to pass the user's text prompt + the **Original Image** as an `image_input` array reference link to enforce image-to-image transformation rules.
* [ ] Build a standard image comparison slider UI component (e.g., using React-Compare-Image or standard CSS clipping masks).
* [ ] Display the textual markdown summary alongside the newly generated image.

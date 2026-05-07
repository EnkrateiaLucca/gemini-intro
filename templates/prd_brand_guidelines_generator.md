Here is a structured Product Requirements Document (PRD) tailored for building this prototype using Google AI Studio’s full-stack app building capabilities. You can feed this directly into your initial prompt to guide the AI Studio agent.

***

# Product Requirements Document (PRD)
**Project Name:** BrandForge (Brand Guidelines Generator)
**Platform:** Google AI Studio (Full-Stack Build Mode)

## 1. Product Overview
**Objective:** Build a conversational, AI-powered web application that allows users to generate professional Brand Guideline documents. Users can "brain dump" their styling preferences and upload visual inspiration (screenshots, logos, mood boards) via a chat interface. The app will synthesize this context and output a structured, formatted PDF (with a Markdown fallback) that can be easily fed into other AI models for future design or content tasks.

## 2. User Flow
1. **The Brain Dump:** The user opens the app and is greeted by a conversational chat interface. They can type unstructured text (e.g., "I want a techy vibe, lots of dark blues, maybe some neon green accents, and a casual but authoritative tone").
2. **Visual Input:** The user uploads image files (screenshots of websites they like, competitor logos, or specific fonts).
3. **Synthesis:** The application sends the text and images to the Gemini API, which extracts and structures the core brand elements (Color Palette with Hex Codes, Typography, Brand Voice, Logo Rules).
4. **Preview:** The UI displays a live, formatted preview of the parsed brand guidelines.
5. **Export:** The user clicks a "Download Guidelines" button. The app generates a styled PDF. If the PDF rendering fails, it immediately downloads a formatted `.md` (Markdown) file as a fallback.

## 3. Core Features & Functional Requirements
### A. Chat & Input Interface
*   **Text Input:** A text area supporting long-form input.
*   **File Upload:** Support for image uploads (PNG, JPEG) via a drag-and-drop zone or attachment button.
*   **Message History:** A basic chat log showing what the user has submitted and how the AI has responded/acknowledged the inputs.

### B. AI Processing (Gemini API)
*   **Multimodal Context:** The app must utilize a Gemini multimodal model (like Gemini 1.5 Flash or Pro) to read both the text instructions and the uploaded images simultaneously.
*   **Structured Output:** The system prompt should instruct Gemini to output the final brand guidelines in a strict JSON format (or well-structured Markdown) to ensure the frontend can easily parse and display it in a standardized template.

### C. Document Generation & Export
*   **PDF Compiler:** A utility to convert the generated brand guidelines into a clean, downloadable PDF.
*   **Markdown Fallback Engine:** A `try/catch` block handling the PDF generation. If the PDF library throws an error (e.g., due to an unsupported character or layout break), the app will automatically generate and trigger a download of a `.md` file containing the same information.

## 4. Technical Stack (Google AI Studio)
*   **Frontend Environment:** React.js
*   **Styling:** Tailwind CSS (for rapid, clean, responsive styling of the chat and document preview).
*   **Backend Environment:** Node.js (leveraging AI Studio’s server-side runtime).
*   **AI Integration:** `@google/genai` SDK.
*   **Dependency/Package Suggestions (npm):**
    *   **PDF Generation:** `html2pdf.js` (for easy client-side conversion of the React preview component into a PDF) or `jspdf`.
    *   **Markdown Rendering:** `react-markdown` (to render the AI's output cleanly in the UI preview).

## 5. System Prompt Strategy (For the AI Studio Agent)
*When building this in Google AI Studio, include this instruction for the underlying Gemini model handling the user's data:*

> "You are an expert Brand Strategist and Designer. The user will provide a messy mix of text ideas and image inspirations. Your job is to analyze all inputs and organize them into a strict, professional Brand Guidelines document. Always extract and output the following sections: 1. Brand Identity (Mission/Vibe), 2. Typography (Primary/Secondary font suggestions based on inputs), 3. Color Palette (Extracted Hex codes), 4. Brand Voice (Tone guidelines), and 5. Visual Directives (Rules based on the uploaded images). Format your final output so it can be cleanly rendered into a document."

***

### 💡 Tip for building in Google AI Studio
When you copy/paste this into the Google AI Studio app builder, you can prompt it by saying: *"Build a full-stack React app based on the following PRD. Make sure to include the `html2pdf.js` library in the npm dependencies for the PDF export requirement."*
# /// script
# dependencies = [
#   "google-genai",
#   "fpdf2",
# ]
# ///

import os
import sys
from google import genai
from fpdf import FPDF

# Configuration exported from your playground code
tools = [
    {
        'type': 'google_search',
    },
]

generation_config = {
    'max_output_tokens': 65536,
    'thinking_level': 'low',
}

def export_to_pdf(topic, chat_history):
    """Generates a PDF from the conversation history."""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", size=12)
    
    # Header Title
    pdf.set_font("Helvetica", style="B", size=16)
    pdf.cell(0, 10, f"AI Search & Chat: {topic}", ln=True, align="C")
    pdf.ln(10)
    
    # Content
    pdf.set_font("Helvetica", size=11)
    for msg in chat_history:
        role = "User" if msg["role"] == "user" else "Gemini"
        text = f"{role}: {msg['content']}"
        # Safe character conversion for standard PDF fonts
        clean_text = text.encode('latin-1', 'replace').decode('latin-1')
        pdf.multi_cell(0, 8, clean_text)
        pdf.ln(3)
        
    filename = f"{topic.lower().replace(' ', '_')}_search_session.pdf"
    pdf.output(filename)
    print(f"\n[System] Conversation saved to: {filename}")

def main():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY environment variable is not set.")
        print("Please set it in your terminal: export GEMINI_API_KEY='your_api_key'")
        sys.exit(1)

    # Initialize client using your configuration
    client = genai.Client(
        api_key=api_key,
    )

    print("=" * 60)
    print("      GEMINI AI SEARCH & CHAT (CLI DEMO)")
    print("=" * 60)
    
    topic = input("Search / Ask about a topic: ").strip()
    if not topic:
        print("A topic is required.")
        return

    print(f"\nSearching Google & analyzing '{topic}'...")
    print("Type 'exit' or 'export' to finish the chat and save the PDF.\n")

    chat_history = []
    previous_interaction_id = None

    # First turn: Trigger the search using your initial playground format
    try:
        interaction = client.interactions.create(
            model='models/gemini-3.5-flash',
            input=f"Search the web and provide an overview/answer for: {topic}",
            tools=tools,
            generation_config=generation_config,
        )
        
        # Save interaction ID to maintain server-side state for subsequent turns
        previous_interaction_id = interaction.id
        
        # Extract output text safely
        response_text = interaction.output_text
        print(f"Gemini: {response_text}\n")
        
        # Track history locally for PDF export
        chat_history.append({"role": "user", "content": topic})
        chat_history.append({"role": "assistant", "content": response_text})
        
    except Exception as e:
        print(f"An error occurred: {e}")
        return

    # Chat loop (continues the search session seamlessly)
    while True:
        user_input = input("You: ").strip()
        
        if user_input.lower() in ["exit", "export"]:
            break
            
        if not user_input:
            continue
            
        try:
            # Continue conversation using stateful previous_interaction_id
            interaction = client.interactions.create(
                model='models/gemini-3.5-flash',
                input=user_input,
                previous_interaction_id=previous_interaction_id,
                tools=tools,
                generation_config=generation_config,
            )
            
            # Update state with the latest interaction
            previous_interaction_id = interaction.id
            response_text = interaction.output_text
            
            print(f"\nGemini: {response_text}\n")
            
            chat_history.append({"role": "user", "content": user_input})
            chat_history.append({"role": "assistant", "content": response_text})
            
        except Exception as e:
            print(f"\n[Error]: {e}\n")

    # Clean up and export the conversation to PDF
    if chat_history:
        export_to_pdf(topic, chat_history)
        
    print("Exiting. Thank you!")

if __name__ == "__main__":
    main()

### 2. How to run it with `uv`

# Open your terminal and run the following commands:

# ```bash
# # Set your API Key
# export GEMINI_API_KEY="your-api-key-here"

# # Execute the script directly
# uv run gemini_search_cli.py
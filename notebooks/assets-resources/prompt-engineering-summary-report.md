# Prompt Engineering Guide: Practical Summary (Page 1/3)

## 1. Introduction to Prompt Engineering

*   **Core Idea:** Prompt engineering is the iterative process of designing effective inputs (prompts) to guide Large Language Models (LLMs) toward desired outputs. It's essential because LLMs are prediction engines, and the prompt sets the context for that prediction.
*   **Accessibility:** You don't need to be a data scientist; anyone can write prompts, but crafting *effective* ones takes practice and iteration.
*   **Goal:** To create prompts that are clear, specific, and provide sufficient context, leading to accurate, relevant, and useful LLM responses. Inadequate prompts cause ambiguity and poor results.
*   **Scope:** This guide focuses on prompting models like Gemini directly (via API or tools like Vertex AI Studio) where configuration is accessible.

## 2. Essential LLM Output Configuration

*Before* focusing solely on the prompt text, configure the model's output parameters. These significantly impact the results:

*   **Output Length (Max Tokens):**
    *   Sets the maximum number of tokens the model will generate.
    *   **Practical Tip:** Be mindful of costs, latency, and energy use (more tokens = higher). Don't rely on this alone for succinctness; adjust the prompt too. Crucial for techniques like ReAct to prevent excessive output. Too short can truncate output (e.g., invalid JSON).
    *   **Temperature:**
*   **Sampling Controls (Temperature, Top-K, Top-P):** These control the randomness and creativity of the output.
        *   Controls randomness. Lower values (~0.1-0.3) = more deterministic, focused, factual. Higher values (~0.7-1.0) = more creative, diverse, potentially unexpected.
        *   **Practical Tip:** Use `0` for tasks with a single correct answer (math, strict data extraction). Start around `0.2` for factual but slightly flexible tasks, and `0.7-0.9` for creative tasks. Be wary of very high temps causing incoherence or the "repetition loop bug".
    *   **Top-K:**
        *   Considers only the `K` most likely next tokens. Lower `K` = more restricted/conservative. Higher `K` = more diverse. `K=1` is deterministic (like Temp 0).
        *   **Practical Tip:** Start around `30-40`. Lower `K` (~20) for more factual, higher `K` (~40+) for creative.
    *   **Top-P (Nucleus Sampling):**
        *   Considers the smallest set of tokens whose cumulative probability exceeds `P`. Lower `P` = more conservative. Higher `P` (~0.95-1.0) = more diverse. `P=0` (or very small) often defaults to the single most likely token. `P=1` considers all tokens.
        *   **Practical Tip:** Often used *instead* of or *with* Top-K. A common starting point is `0.95`. Lower `P` (~0.9) for factual, higher `P` (~0.99) for creative.
    *   **Putting it Together:** The model typically filters by Top-K and Top-P first, then applies Temperature to the remaining candidates. Extreme settings in one can make others irrelevant (e.g., Temp 0 ignores K/P; K=1 ignores Temp/P).
    *   **Starting Point Recommendation:** Temp `0.2`, Top-P `0.95`, Top-K `30` for balanced results. Adjust based on desired creativity/factuality.

## 3. Foundational Prompting Techniques

*   **Zero-Shot Prompting:**
    *   Provide only the task description or question without any examples.
    *   `Example: Classify the following movie review: [Review Text]`
    *   **Practical Tip:** Simplest method, good starting point. May fail for complex tasks or when specific output formats are needed.
*   **One-Shot / Few-Shot Prompting:**
    *   Provide one (one-shot) or multiple (few-shot) examples of the task and desired output.
    *   `Example (Few-Shot Sentiment):`
        `Review: "Loved it!" Sentiment: Positive`
        `Review: "Boring." Sentiment: Negative`
        `Review: "It was okay." Sentiment: Neutral`
        `Review: "[New Review Text]" Sentiment:`
    *   **Practical Tip:** Highly effective for guiding the model on structure, style, and task logic. Use 3-5 high-quality, diverse examples as a rule of thumb. Include edge cases if needed. Ensure examples are accurate, as errors confuse the model.

---

# Prompt Engineering Guide: Practical Summary (Page 2/3)

## 4. Intermediate Prompting Techniques

*   **System, Contextual, and Role Prompting:**
    *   **System Prompt:** Defines the overall task, fundamental purpose, or constraints (e.g., "Translate the following text to French.", "Only return JSON.").
    *   **Contextual Prompt:** Provides specific background information relevant to the *current* task or query (e.g., "Given the previous conversation about user preferences, suggest a suitable product.").
    *   **Role Prompt:** Assigns a persona or identity to the LLM (e.g., "Act as a pirate.", "You are a helpful travel guide specialized in budget travel.").
    *   **Practical Tip:** Use **Role Prompting** to control tone, style, and expertise (e.g., "Explain this concept like I'm five.", "Write in a formal, academic style."). Combine these types as needed (e.g., a Role prompt can include Context).
*   **Step-Back Prompting:**
    *   Ask the LLM a more general, abstract question related to the specific task *first*. Then, use the answer to that general question as context when asking the specific task prompt.
    *   **Practical Tip:** Improves reasoning by activating broader knowledge. Useful for complex problems or mitigating bias. Requires two LLM calls.
*   **Chain of Thought (CoT) Prompting:**
    *   Instruct the LLM to break down its reasoning process step-by-step before giving the final answer. Simply add phrases like "Let's think step by step."
    *   `Example: Q: [Math Problem]. Let's think step by step. A:`
    *   **Practical Tip:** Significantly improves performance on tasks requiring reasoning (math, logic puzzles). Provides interpretability. Works well combined with few-shot examples showing the reasoning steps. Use **Temperature 0** for CoT tasks. Ensure the final answer comes *after* the reasoning steps. More tokens = higher cost/latency.
*   **Self-Consistency:**
    *   An enhancement to CoT. Run the same CoT prompt multiple times with a higher temperature (to generate diverse reasoning paths). Select the most frequent final answer (majority vote).
    *   **Practical Tip:** Improves accuracy over basic CoT, especially for complex reasoning. Significantly increases cost due to multiple runs.
*   **Tree of Thoughts (ToT):**
    *   (Advanced) Explores multiple reasoning paths simultaneously, forming a tree structure. Better for complex exploration tasks. Less common in basic prompt engineering.
*   **ReAct (Reason + Act):**
    *   Enables LLMs to use external tools (like search APIs, code interpreters) by interleaving reasoning steps (`Thought:`) with actions (`Action:`, `Action Input:`) and observing results (`Observation:`).
    *   **Practical Tip:** Foundational for building agents. Requires external frameworks (e.g., LangChain) and tool setup (API keys). Needs careful management of the prompt history (context) sent back to the LLM in each step. Restrict output length to avoid runaway actions.
*   **Automatic Prompt Engineering (APE):**
    *   Use an LLM to generate variations of an initial prompt for a specific task. Evaluate these generated prompts (manually or using metrics like BLEU/ROUGE) and select the best one.
    *   **Practical Tip:** Can help discover effective prompt phrasing, especially for training data generation. Iterative process.

## 5. Code Prompting Specifics

*   LLMs like Gemini can understand and generate code.
*   **Use Cases:**
    *   **Writing Code:** Provide a description of the desired functionality. (e.g., "Write a Python script to rename files in a folder, prepending 'draft_'").
    *   **Explaining Code:** Paste code and ask for an explanation. (e.g., "Explain this Bash script line by line.").
    *   **Translating Code:** Provide code in one language and ask for another. (e.g., "Translate this Bash script to Python.").
    *   **Debugging & Reviewing Code:** Provide code and the error message, ask for debugging help, or ask for general improvements/review.
*   **Practical Tips:**
    *   **ALWAYS TEST GENERATED CODE.** LLMs can make subtle or significant errors.
    *   Be specific about the language, libraries, and desired functionality.
    *   For debugging, provide the full error message and relevant code snippet.
    *   In tools like Vertex AI Studio, use the 'Markdown' view for code output to preserve formatting (especially Python indentation).

---

# Prompt Engineering Guide: Practical Summary (Page 3/3)

## 6. Best Practices for Effective Prompting

*   **Provide Examples (Few-Shot):** (Reiteration) Often the single most effective technique. Show, don't just tell.
*   **Design with Simplicity:** Clear, concise language. Avoid jargon or unnecessary info. If it's confusing to you, it's likely confusing to the model.
    *   **Tip:** Use clear action verbs (e.g., `Summarize`, `Classify`, `Generate`, `Translate`, `Extract`, `Rewrite`).
*   **Be Specific About the Output:** Clearly define the desired format, length, style, content, and target audience. Don't be vague (e.g., "Write a 3-paragraph blog post for beginners..." vs. "Write about consoles.").
*   **Use Instructions over Constraints:** Tell the model *what to do* rather than only *what not to do*. Constraints are okay for safety guardrails or strict formatting but can be less effective or conflicting.
    *   `DO: Summarize the text in 3 bullet points.`
    *   `LESS EFFECTIVE: Do not write a long summary. Do not use paragraphs.`
*   **Control Max Token Length:** Use configuration or specify length in the prompt (e.g., "...in under 100 words," "...in a single sentence").
*   **Use Variables in Prompts:** Use placeholders (like `{city}` or `$user_input`) to make prompts reusable and dynamic. Essential for integrating prompts into applications.
*   **Experiment Iteratively:** Try different phrasing, formats (question vs. instruction), styles, examples, configurations, and even different models/versions. Prompt engineering is not a one-shot process.
*   **Mix Classes (Few-Shot Classification):** When providing examples for classification, ensure the examples cover different classes and aren't all clustered together to avoid order bias.
*   **Adapt to Model Updates:** Newer model versions may have different capabilities or respond differently. Re-test prompts with new versions.
*   **Experiment with Output Formats (JSON/XML):**
    *   For non-creative tasks (extraction, classification, structured data), explicitly ask for output in JSON or XML.
    *   **Benefits:** Consistent structure, easier parsing in applications, can enforce data types, reduces hallucination likelihood.
    *   **Tip:** Provide the desired schema or an example JSON structure in the prompt (few-shot). Be mindful of token limits, as JSON is verbose. Use tools like the `json-repair` library (Python) to fix truncated/malformed JSON output.
*   **Working with Schemas (Input):** Provide a JSON Schema definition along with the JSON input data. This helps the LLM understand the structure and focus on relevant fields, especially for complex or large inputs.
*   **Collaborate:** If possible, have multiple people attempt prompt design and compare results.
*   **DOCUMENT EVERYTHING:**
    *   **Crucial:** Keep detailed records of your prompt attempts.
    *   **Template Fields:** Prompt Name/Version, Goal, Model Used, Temperature, Top-K, Top-P, Max Tokens, Full Prompt Text, Output(s), Outcome (OK/Not OK/Sometimes OK), Feedback/Notes, Hyperlink (if saved in a tool like Vertex AI Studio).
    *   **Why:** Enables learning, debugging, re-testing on new models, and avoids re-doing work.
    *   **Tip:** Store prompts in separate files from application code for maintainability. Consider automated testing/evaluation for prompts in production.

## 7. Final Takeaway

Effective prompt engineering is an iterative cycle: **Craft -> Test -> Analyze -> Document -> Refine.** It requires understanding the LLM's configuration options, leveraging different prompting techniques (especially examples), clearly stating intent, and meticulously documenting experiments to achieve consistent, high-quality results.

---
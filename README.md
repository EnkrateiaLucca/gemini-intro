# O'Reilly Live Training - Building Apps with Gemini

## Setup

**Makefile (Recommended)**

The fastest way to get set up:

```bash
make all
```

This will create the conda environment, install dependencies, set up the Jupyter kernel, and compile requirements.

**Conda (Manual)**

- Install [anaconda](https://www.anaconda.com/download)
- This repo was tested on a Mac with python=3.10.
- Create an environment: `conda create -n oreilly-gemini python=3.10`
- Activate your environment with: `conda activate oreilly-gemini`
- Install requirements with: `pip install -r requirements/requirements.txt`
- Setup your Google [API key](https://aistudio.google.com/app/apikey)

**Pip**

1. **Create a Virtual Environment:**
    Navigate to your project directory. Make sure you have python3.10 installed!
    If using Python 3's built-in `venv`: `python -m venv oreilly-gemini`
    If you're using `virtualenv`: `virtualenv oreilly-gemini`

2. **Activate the Virtual Environment:**
    - **On Windows:** `.\oreilly-gemini\Scripts\activate`
    - **On macOS and Linux:** `source oreilly-gemini/bin/activate`

3. **Install Dependencies from `requirements.txt`:**
    ```bash
    pip install python-dotenv
    pip install -r ./requirements/requirements.txt
    ```

4. Setup your Google [API key](https://aistudio.google.com/app/apikey)

Remember to deactivate the virtual environment afterwards: `deactivate`

## Setup your .env file

- Change the `.env.example` file to `.env` and add your Google API key.

```bash
GEMINI_API_KEY=<your google api key>
```

## To use this Environment with Jupyter Notebooks:

- ```conda install jupyter -y```
- ```python -m ipykernel install --user --name=oreilly-gemini```

## Notebooks

Here are the notebooks available in the `code/` folder:

1. [Gemini API Introduction](code/1.0-gemini-api-intro.ipynb) - Text generation with the Gemini API
2. [Gemini Chat, PDF & Image Understanding](code/2.0-gemini-chat-pdf-image-understanding.ipynb) - Multimodal chat with PDFs and images
3. [Gemini Embeddings](code/3.0-gemini-embeddings.ipynb) - Text embeddings and similarity search
4. [Token Usage](code/4.0-token-usage.ipynb) - Understanding and tracking token consumption

## Scripts

- [`gemini_image_gen.py`](code/gemini_image_gen.py) - Generate images with Gemini and interactively keep or delete them (runnable with `uv run code/gemini_image_gen.py`)
- [`app.py`](app.py) - Flask storyboard demo: turns a story prompt into a six-frame storyboard, then generates an image for each frame. Run with `python app.py` and open http://localhost:5001. Requires `GEMINI_API_KEY` in your `.env`.

## Demo Projects

- [AI Interior Architect](https://github.com/EnkrateiaLucca/interior-ai-architecture) - Upload a room photo and chat with Gemini to redesign it, with a before/after image slider ([PRD](interior-ai-architecture-prd.md))

## Additional Resources

- [`code/guide-prompting-gemini.md`](code/guide-prompting-gemini.md) - Comprehensive prompt engineering guide for Gemini
- [`assets/gemini-intro-cheatsheet.pdf`](assets/gemini-intro-cheatsheet.pdf) - Quick-reference card for the course (models, thinking levels, and API patterns)
- `code/assets-resources/` - Supporting PDFs, images, and reference materials
- `presentation/` - Course presentation slides (Remark.js HTML)

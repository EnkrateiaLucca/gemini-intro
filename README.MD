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
GOOGLE_API_KEY=<your google api key>
```

## To use this Environment with Jupyter Notebooks:

- ```conda install jupyter -y```
- ```python -m ipykernel install --user --name=oreilly-gemini```

## Notebooks

Here are the notebooks available in the `code/` folder:

1. [Gemini API Introduction](code/1.0-gemini-api-intro.ipynb) - Text generation with the Gemini API
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/EnkrateiaLucca/oreilly-live-trainings/blob/main/gemini-intro/code/1.0-gemini-api-intro.ipynb)

2. [Gemini Chat, PDF & Image Understanding](code/2.0-gemini-chat-pdf-image-understanding.ipynb) - Multimodal chat with PDFs and images
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/EnkrateiaLucca/oreilly-live-trainings/blob/main/gemini-intro/code/2.0-gemini-chat-pdf-image-understanding.ipynb)

3. [Gemini Embeddings](code/3.0-gemini-embeddings.ipynb) - Text embeddings and similarity search
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/EnkrateiaLucca/oreilly-live-trainings/blob/main/gemini-intro/code/3.0-gemini-embeddings.ipynb)

4. [Token Usage](code/4.0-token-usage.ipynb) - Understanding and tracking token consumption
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/EnkrateiaLucca/oreilly-live-trainings/blob/main/gemini-intro/code/4.0-token-usage.ipynb)

## Scripts

- [`gemini_image_gen.py`](code/gemini_image_gen.py) - Generate images with Gemini and interactively keep or delete them (runnable with `uv run code/gemini_image_gen.py`)

## Additional Resources

- [`code/guide-prompting-gemini.md`](code/guide-prompting-gemini.md) - Comprehensive prompt engineering guide for Gemini
- `code/assets-resources/` - Supporting PDFs, images, and reference materials
- `presentation/` - Original course presentation slides (Remark.js HTML, archived)
- `presentation-v2/` - Updated course slides built with [open-slide](https://github.com/1weiho/open-slide). Run with `cd presentation-v2 && pnpm install && pnpm dev`

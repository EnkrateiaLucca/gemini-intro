# O'Reilly Live Trainining - Building Apps with Gemini

## Setup

**Conda**

- Install [anaconda](https://www.anaconda.com/download)
- This repo was tested on a Mac with python=3.10.
- Create an environment: `conda create -n oreilly-gemini python=3.10`
- Activate your environment with: `conda activate oreilly-gemini`
- Install requirements with: `pip install -r requirements/requirements.txt`
- Setup your openai [API key](https://platform.openai.com/)

**Pip**


1. **Create a Virtual Environment:**
    Navigate to your project directory. Make sure you have python3.10 installed! 
    If using Python 3's built-in `venv`: `python -m venv oreilly-gemini`
    If you're using `virtualenv`: `virtualenv oreilly-gemini`

2. **Activate the Virtual Environment:**
    - **On Windows:**: `.\oreilly-gemini\Scripts\activate`
    - **On macOS and Linux:**: `source oreilly-gemini/bin/activate`

3. **Install Dependencies from `requirements.txt`:**
    ```bash
    pip install python-dotenv
    pip install -r ./requirements/requirements.txt
    ```

4. Setup your openai [API key](https://platform.openai.com/)

Remember to deactivate the virtual environment afterwards: `deactivate`

## Setup your .env file

- Change the `.env.example` file to `.env` and add your OpenAI API key.

```bash
OPENAI_API_KEY=<your openai api key>
```

## To use this Environment with Jupyter Notebooks:

- ```conda install jupyter -y```
- ```python -m ipykernel install --user --name=oreilly-gemini```

## Notebooks

Here are the notebooks available in the `notebooks/` folder:

1. [Gemini API Introduction](notebooks/1.0-gemini-api-intro.ipynb)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/EnkrateiaLucca/oreilly-live-trainings/blob/main/gemini-intro/notebooks/1.0-gemini-api-intro.ipynb)

2. [Prompting Gemini](notebooks/2.0-prompting-gemini.ipynb)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/EnkrateiaLucca/oreilly-live-trainings/blob/main/gemini-intro/notebooks/2.0-prompting-gemini.ipynb)

3. [Gemini Embeddings](notebooks/3.0-gemini-embeddings.ipynb)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/EnkrateiaLucca/oreilly-live-trainings/blob/main/gemini-intro/notebooks/3.0-gemini-embeddings.ipynb)

4. [Gemini Chat, PDF & Image Understanding](notebooks/4.0-gemini-chat-pdf-image-understanding.ipynb)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/EnkrateiaLucca/oreilly-live-trainings/blob/main/gemini-intro/notebooks/4.0-gemini-chat-pdf-image-understanding.ipynb)

Additional resources can be found in:
- `notebooks/assets-resources/` - Supporting assets and resources

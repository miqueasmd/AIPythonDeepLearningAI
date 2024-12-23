# Deep Learning Project: Automating Tasks with OpenAI's GPT-4o

This project demonstrates how to use OpenAI's GPT-4o to automate tasks such as extracting information from a journal entry and formatting it into HTML for display in a Jupyter notebook.

## Project Structure

- `helper_functions.py`: Contains helper functions for reading journal entries, interacting with the GPT-4 model, and formatting responses into HTML.
- `automating_tasks.ipynb`: Jupyter notebook that demonstrates the process of reading a journal entry, creating a prompt, getting a response from GPT-4, and displaying the formatted HTML response.
- `data/`: Directory containing data files.

## Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/miqueasmd/deep-learning-project.git
   cd deep-learning-project
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   - Create a `.env` file in the project root directory.
   - Add your OpenAI API key to the `.env` file:
     ```plaintext
     OPENAI_API_KEY=your_openai_api_key_here
     BASE_PATH=your_base_path_here
     ```

## Usage

1. **Run the Jupyter notebook**:
   ```bash
   jupyter notebook automating_tasks.ipynb
   ```

2. **Follow the steps in the notebook** to read the journal entry, create a prompt, get the response from GPT-4, and display the formatted HTML response.

## ☕ Support Me

If you like my work, consider supporting my studies!

Your contributions will help cover fees and materials for my **Computer Science and Engineering studies  at UoPeople** starting in September 2025.

Every little bit helps—you can donate from as little as $1.

<a href="https://ko-fi.com/miqueasmd"><img src="https://ko-fi.com/img/githubbutton_sm.svg" /></a>

## Acknowledgements

This project is inspired by the DeepLearning.AI courses. Please visit [DeepLearning.AI](https://www.deeplearning.ai/) for more information and resources.



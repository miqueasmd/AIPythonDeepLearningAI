# Deep Learning Project: Automating Tasks with OpenAI's GPT-4o

This project leverages OpenAI's GPT-4 to analyze travel journals, create itineraries, and process restaurant recommendations. It includes tools for managing API usage, processing various data formats, and generating formatted outputs.

## Features

- **Journal Analysis**: Extract key information from travel journals including restaurants, activities, and food specialties
- **Smart Itinerary Planning**: Generate detailed daily itineraries based on dates and available restaurant data
- **Data Processing**: Handle multiple file formats (CSV, TXT, HTML)
- **API Usage Monitoring**: Track OpenAI API usage and costs
- **Interactive Components**: Jupyter notebook integration with HTML display capabilities
- **Weather Integration**: Fetch and analyze weather data for travel planning
- **Utility Functions**: Temperature conversions, random selections, and data formatting tools

## Project Structure

This project is structured for clarity and maintainability. Let's explore the key folders:

- **data/** (folder): Stores all the raw data used for analysis.
    - **cape_town.txt** (file): Contains journal entries specifically for Cape Town.
    - **journal_tokyo.txt** (file): Journal entries from your trip to Tokyo.
    - **journal_rio.txt** (file): Similar file for Rio de Janeiro.
    - **journal_sidney.txt** (file): Journal entries for Sydney.
    - **.csvs**: Various data files in CSV format, likely containing restaurant details or itinerary information.
- **code/** (folder): Houses Jupyter Notebooks for data analysis.
    - **helper_functions.py** (file): Contains core functions used across notebooks for common tasks.
    - **api_usage_monitor.py** (file): Tracks your OpenAI API usage, ensuring responsible use of the platform.

This structure facilitates easy access to data and code, promoting efficient workflow and collaboration.

## Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/miqueasmd/AIPythonDeepLearningAI.git
   AIPythonDeepLearningAI
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

## Core Functions

### Journal Analysis

### Restaurant Data Processing

### Itinerary Planning

### Generate detailed itinerary

### Generate city-specific plans

### API Usage Monitoring


## Usage Notes

1. **API Costs**: The project uses OpenAI's API which has associated costs. Monitor usage through the provided tools.
2. **Rate Limits**: Includes retry mechanisms for API rate limits.
3. **Data Storage**: Journal entries and restaurant data should be stored in the `/data` directory.
4. **Interactive Features**: Many features are designed for Jupyter notebook integration.
  

## ☕ Support Me

If you like my work, consider supporting my studies!

Your contributions will help cover fees and materials for my **Computer Science and Engineering studies  at UoPeople** starting in September 2025.

Every little bit helps—you can donate from as little as $1.

<a href="https://ko-fi.com/miqueasmd"><img src="https://ko-fi.com/img/githubbutton_sm.svg" /></a>

## Acknowledgements

This project is inspired by the DeepLearning.AI courses. Please visit [DeepLearning.AI](https://www.deeplearning.ai/) for more information and resources.



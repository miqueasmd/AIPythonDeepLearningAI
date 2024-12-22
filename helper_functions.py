import os
from openai import OpenAI
from dotenv import load_dotenv
import csv

# Load environment variables from a .env file
load_dotenv('.env', override=True)

# Retrieve the OpenAI API key from environment variables
openai_api_key = os.getenv('OPENAI_API_KEY')

# Check if the API key is available
if not openai_api_key:
    raise ValueError("API key not found. Please set the OPENAI_API_KEY environment variable.")

# Initialize the OpenAI client with the API key
client = OpenAI(api_key=openai_api_key)

def print_llm_response(prompt):
    """
    This function takes a prompt as input, which must be a string enclosed in quotation marks,
    and passes it to OpenAI’s GPT-4 model. The function then prints the response of the model.
    
    Args:
        prompt (str): The input prompt to be sent to the GPT-4 model.
    
    Raises:
        ValueError: If the input prompt is not a string.
        TypeError: If there is an error in processing the response.
    """
    try:
        if not isinstance(prompt, str):
            raise ValueError("Input must be a string enclosed in quotes.")
        
        # Create a completion request to the GPT-4 model
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful but terse AI assistant who gets straight to the point.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.0,
        )
        
        # Extract and print the response from the model
        response = completion.choices[0].message.content
        print("*" * 100)
        print(response)
        print("*" * 100)
        print("\n")
    except TypeError as e:
        print("Error:", str(e))

def get_llm_response(prompt):
    """
    This function takes a prompt as input, which must be a string enclosed in quotation marks,
    and passes it to OpenAI’s GPT-4 model. The function then returns the response of the model as a string.
    
    Args:
        prompt (str): The input prompt to be sent to the GPT-4 model.
    
    Returns:
        str: The response from the GPT-4 model.
    """
    # Create a completion request to the GPT-4 model
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful but terse AI assistant who gets straight to the point.",
            },
            {"role": "user", "content": prompt},
        ],
    )
    
    # Extract and return the response from the model
    response = completion.choices[0].message.content
    return response

def read_journal(file_path):
    """
    Reads the content of a journal file and returns it as a string.
    
    Args:
        file_path (str): The path to the journal file.
    
    Returns:
        str: The content of the journal file.
    
    Raises:
        FileNotFoundError: If the file is not found.
        Exception: If any other error occurs while reading the file.
    """
    try:
        with open(file_path, 'r') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Define a function to format the response into HTML
def format_response_to_html(response):
    """
    This function formats the given response into an HTML structure.
    
    Args:
        response (str): The response text to be formatted into HTML.
    
    Returns:
        str: The formatted HTML content.
    """
    # Create the HTML content with the response embedded
    html_content = f"""
    <html>
    <body>
    <p>Embarking on a gastronomic journey through Cape Town revealed a city brimming with culinary treasures. Each stop was a testament to the rich flavors and unique dishes that define this vibrant city's food scene.</p>
    {response}
    </body>
    </html>
    """
    return html_content
import os
from openai import OpenAI
from dotenv import load_dotenv
import csv
from IPython.display import display, HTML  # Import HTML


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

def upload_txt_file(file_path):
    """
    Uploads a text file and returns its content as a string.
    
    Args:
        file_path (str): The path to the text file.
    
    Returns:
        str: The content of the text file.
    """
    try:
        with open(file_path, 'r') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

def list_files_in_directory(directory_path):
    """
    Lists all files in a given directory.
    
    Args:
        directory_path (str): The path to the directory.
    
    Returns:
        list: A list of file names in the directory.
    """
    try:
        files = os.listdir(directory_path)
        return files
    except FileNotFoundError:
        print(f"Error: The directory {directory_path} was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

def download_file(file_name):
    """
    Generates an HTML button to download the specified file.
    
    Args:
        file_name (str): The name of the file to be downloaded.
    
    Returns:
        None
    """
    html = f"""
    <html>
    <body>
    <a href="{file_name}" download="{file_name}">
        <button>Click here to download your file</button>
    </a>
    </body>
    </html>
    """
    display(HTML(html))

def display_table(data):
    """
    Displays a list of dictionaries as an HTML table.
    
    Args:
        data (list): A list of dictionaries representing the table data.
    
    Returns:
        None
    """
    if not data:
        print("No data to display.")
        return
    
    # Extract headers from the first dictionary
    headers = data[0].keys()
    
    # Create the HTML table
    html = "<table border='1'>"
    html += "<tr>" + "".join(f"<th>{header}</th>" for header in headers) + "</tr>"
    
    for row in data:
        html += "<tr>" + "".join(f"<td>{row[header]}</td>" for header in headers) + "</tr>"
    
    html += "</table>"
    
    # Display the HTML table
    display(HTML(html))
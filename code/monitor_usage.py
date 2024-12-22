import os
import requests
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables from a .env file
load_dotenv('.env', override=True)

# Retrieve the OpenAI API key from environment variables
openai_api_key = os.getenv('OPENAI_API_KEY')

# Check if the API key is available
if not openai_api_key:
    raise ValueError("API key not found. Please set the OPENAI_API_KEY environment variable.")

def get_usage(api_key, date):
    """
    Fetches the usage data for the given OpenAI API key for a specific date.

    Args:
        api_key (str): The OpenAI API key.
        date (str): The date for the usage data in YYYY-MM-DD format.

    Returns:
        dict: The usage data.
    """
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    params = {
        "date": date
    }
    response = requests.get("https://api.openai.com/v1/usage", headers=headers, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch usage data: {response.status_code} - {response.text}")

def display_usage_and_cost(usage_data, monthly_limit=10.00):
    """
    Displays the usage data, estimated cost, and remaining balance.

    Args:
        usage_data (dict): The usage data from the API.
        monthly_limit (float): The monthly spending limit for the API.
    """
    print("API Usage Data:")

    # Check if there is any usage data
    if not usage_data.get('data'):
        print("No usage data available for the specified date range.")
        return

    total_context_tokens = 0
    total_generated_tokens = 0
    total_requests = 0

    for entry in usage_data['data']:
        total_context_tokens += entry.get('n_context_tokens_total', 0)
        total_generated_tokens += entry.get('n_generated_tokens_total', 0)
        total_requests += entry.get('n_requests', 0)

    # Calculate costs based on token usage
    context_cost = total_context_tokens * 0.0000025  # $2.50 per 1M input tokens
    generated_cost = total_generated_tokens * 0.00001  # $10.00 per 1M output tokens
    total_cost = context_cost + generated_cost

    # Calculate remaining balance
    remaining_balance = monthly_limit - total_cost

    print(f"Total Context Tokens Used: {total_context_tokens}")
    print(f"Total Generated Tokens Used: {total_generated_tokens}")
    print(f"Total Requests: {total_requests}")
    print(f"Estimated Cost: ${total_cost:.2f}")
    print(f"Monthly Limit: ${monthly_limit:.2f}")
    print(f"Remaining Balance: ${remaining_balance:.2f}")

if __name__ == "__main__":
    # Get today's date in YYYY-MM-DD format
    today_date = datetime.today().strftime('%Y-%m-%d')

    try:
        usage_data = get_usage(openai_api_key, today_date)
        display_usage_and_cost(usage_data, monthly_limit=10.00)  # Set your monthly limit here
    except Exception as e:
        print(f"Error: {e}")

import os
import requests
import time
from dotenv import load_dotenv
from datetime import datetime, timedelta

# Load environment variables from a .env file
load_dotenv('.env', override=True)

# Retrieve the OpenAI API key from environment variables
openai_api_key = os.getenv('OPENAI_API_KEY')

# Check if the API key is available
if not openai_api_key:
    raise ValueError("API key not found. Please set the OPENAI_API_KEY environment variable.")

def get_usage_with_retry(api_key, date, max_retries=5, max_wait=32):
    """
    Fetches the usage data for the given OpenAI API key for a specific date with retry mechanism.

    Args:
        api_key (str): The OpenAI API key.
        date (str): The date for the usage data in YYYY-MM-DD format.
        max_retries (int): Maximum number of retries before giving up.
        max_wait (int): Maximum wait time in seconds for retries.

    Returns:
        dict: The usage data.
    """
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    params = {
        "date": date
    }
    retries = 0
    while retries < max_retries:
        response = requests.get("https://api.openai.com/v1/usage", headers=headers, params=params)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 429:  # Rate limit exceeded
            retries += 1
            wait_time = min(2 ** retries, max_wait)  # Cap wait time
            print(f"Rate limit exceeded. Retrying in {wait_time} seconds...")
            time.sleep(wait_time)
        else:
            raise Exception(f"Failed to fetch usage data: {response.status_code} - {response.text}")
    raise Exception("Max retries exceeded. Could not fetch usage data.")

def display_usage_and_cost_for_period(api_key, days=10, monthly_limit=10.00):
    """
    Fetches and aggregates usage data for the last 'days' days, displays the total usage, estimated cost, and remaining balance.

    Args:
        api_key (str): The OpenAI API key.
        days (int): Number of days to fetch usage data for.
        monthly_limit (float): The monthly spending limit for the API.
    """
    print(f"API Usage Data for the Last {days} Days:")
    total_context_tokens = 0
    total_generated_tokens = 0
    total_requests = 0

    for i in range(days):
        date = (datetime.today() - timedelta(days=i)).strftime('%Y-%m-%d')
        try:
            usage_data = get_usage_with_retry(api_key, date)
            if usage_data.get('data'):
                for entry in usage_data['data']:
                    total_context_tokens += entry.get('n_context_tokens_total', 0)
                    total_generated_tokens += entry.get('n_generated_tokens_total', 0)
                    total_requests += entry.get('n_requests', 0)
        except Exception as e:
            print(f"Error fetching data for {date}: {e}")

    # Calculate costs based on token usage
    context_cost = total_context_tokens * 0.0000025  # $2.50 per 1M input tokens
    generated_cost = total_generated_tokens * 0.00001  # $10.00 per 1M output tokens
    total_cost = context_cost + generated_cost

    # Calculate remaining balance
    remaining_balance = monthly_limit - total_cost

    print(f"Total Context/Input Tokens Used: {total_context_tokens}")
    print(f"Total Generated/Output Tokens Used: {total_generated_tokens}")
    print(f"Total Requests: {total_requests}")
    print(f"Estimated Cost: ${total_cost:.2f}")
    print(f"Monthly Limit: ${monthly_limit:.2f}")
    print(f"Remaining Balance: ${remaining_balance:.2f}")

if __name__ == "__main__":
    try:
        display_usage_and_cost_for_period(openai_api_key, days=10, monthly_limit=10.00)  # Adjust 'days' and 'monthly_limit' as needed
    except Exception as e:
        print(f"Error: {e}")

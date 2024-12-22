import os
import requests
from dotenv import load_dotenv
from datetime import datetime
import streamlit as st

# Load environment variables from a .env file
load_dotenv('.env', override=True)

# Retrieve the OpenAI API key from environment variables
openai_api_key = os.getenv('OPENAI_API_KEY')

# Check if the API key is available
if not openai_api_key:
    st.error("API key not found. Please set the OPENAI_API_KEY environment variable.")
    st.stop()

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

def display_usage(usage_data, monthly_limit):
    """
    Displays the usage data, estimated cost, and remaining balance.

    Args:
        usage_data (dict): The usage data from the API.
        monthly_limit (float): The monthly spending limit for the API.
    """
    st.write("API Usage Data:")
    
    # Check if there is any data
    if not usage_data.get('data'):
        st.write("No usage data available for the specified date range.")
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

    st.write(f"Total Context Tokens Used: {total_context_tokens}")
    st.write(f"Total Generated Tokens Used: {total_generated_tokens}")
    st.write(f"Total Requests: {total_requests}")
    st.write(f"Estimated Cost: ${total_cost:.2f}")
    st.write(f"Monthly Limit: ${monthly_limit:.2f}")
    st.write(f"Remaining Balance: ${remaining_balance:.2f}")

# Streamlit interface
st.title("OpenAI API Usage Monitor")

# Get today's date in YYYY-MM-DD format
today_date = datetime.today().strftime('%Y-%m-%d')

# User input for monthly limit
monthly_limit = st.number_input("Enter your initial balance ($):", min_value=0.0, value=10.0)

if st.button("Get Usage Data"):
    try:
        usage_data = get_usage(openai_api_key, today_date)
        display_usage(usage_data, monthly_limit)
    except Exception as e:
        st.error(f"Error: {e}")
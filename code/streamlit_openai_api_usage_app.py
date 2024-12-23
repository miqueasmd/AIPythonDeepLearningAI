import os
import requests
import time
from dotenv import load_dotenv
from datetime import datetime, timedelta
import streamlit as st
import pandas as pd

# Load environment variables from a .env file
load_dotenv('.env', override=True)

# Retrieve the OpenAI API key from environment variables
openai_api_key = os.getenv('OPENAI_API_KEY')

# Check if the API key is available
if not openai_api_key:
    st.error("API key not found. Please set the OPENAI_API_KEY environment variable.")
    st.stop()

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
            st.write(f"Rate limit exceeded for {date}. Retrying in {wait_time} seconds... (Attempt {retries}/{max_retries})")
            time.sleep(wait_time)
        else:
            raise Exception(f"Failed to fetch usage data: {response.status_code} - {response.text}")
    raise Exception(f"Max retries exceeded for {date}. Could not fetch usage data.")

def display_usage_and_cost_for_period(api_key, days=10, monthly_limit=10.00):
    """
    Fetches and aggregates usage data for the last 'days' days, displays the total usage, estimated cost, and remaining balance.

    Args:
        api_key (str): The OpenAI API key.
        days (int): Number of days to fetch usage data for.
        monthly_limit (float): The monthly spending limit for the API.
    """
    st.write(f"API Usage Data for the Last {days} Days:")
    total_input_tokens = 0
    total_output_tokens = 0
    total_requests = 0
    total_cost = 0.0
    failed_dates = []
    daily_usage = []

    progress_bar = st.progress(0)

    for i in range(days):
        date = (datetime.today() - timedelta(days=i)).strftime('%Y-%m-%d')
        daily_input_tokens = 0
        daily_output_tokens = 0
        daily_requests = 0
        try:
            usage_data = get_usage_with_retry(api_key, date)
            if usage_data.get('data'):
                for entry in usage_data['data']:
                    daily_input_tokens += entry.get('n_context_tokens_total', 0)
                    daily_output_tokens += entry.get('n_generated_tokens_total', 0)
                    daily_requests += entry.get('n_requests', 0)
        except Exception as e:
            st.write(f"Error fetching data for {date}: {e}")
            failed_dates.append(date)

        # Calculate daily cost
        daily_input_cost = daily_input_tokens * 0.0000025  # $2.50 per 1M input tokens
        daily_output_cost = daily_output_tokens * 0.00001  # $10.00 per 1M output tokens
        daily_cost = daily_input_cost + daily_output_cost

        daily_usage.append({
            'Date': date,
            'Input Tokens': daily_input_tokens,
            'Output Tokens': daily_output_tokens,
            'Requests': daily_requests,
            'Estimated Cost ($)': daily_cost
        })
        total_input_tokens += daily_input_tokens
        total_output_tokens += daily_output_tokens
        total_requests += daily_requests
        total_cost += daily_cost

        progress_bar.progress((i + 1) / days)

    # Calculate remaining balance
    remaining_balance = monthly_limit - total_cost

    st.write(f"**Total Context/Input Tokens Used:** {total_input_tokens}")
    st.write(f"**Total Generated/Output Tokens Used:** {total_output_tokens}")
    st.write(f"**Total Requests:** {total_requests}")
    st.write(f"**Estimated Cost:** ${total_cost:.2f}")
    st.write(f"**Monthly Limit:** ${monthly_limit:.2f}")
    st.write(f"**Remaining Balance:** ${remaining_balance:.2f}")

    if failed_dates:
        st.write("### Failed to fetch data for the following dates:")
        st.write(", ".join(failed_dates))

    # Display daily usage in a table format
    if daily_usage:
        st.write("### Daily Usage Data:")
        daily_usage_df = pd.DataFrame(daily_usage)
        
        # Adjust index to start at 1
        daily_usage_df.index = daily_usage_df.index + 1  # Start index at 1
        
        # Add a final row with totals
        total_row = pd.DataFrame({
            'Date': ['Total'],
            'Input Tokens': [total_input_tokens],
            'Output Tokens': [total_output_tokens],
            'Requests': [total_requests],
            'Estimated Cost ($)': [total_cost]
        }, index=[len(daily_usage_df) + 1])  # Set the index for the total row
        
        daily_usage_df = pd.concat([daily_usage_df, total_row])
        st.table(daily_usage_df)

# Streamlit interface
st.title("OpenAI API Usage Monitor")

# User input for the number of days and monthly limit
days = st.number_input("Enter the number of days to view usage (default is 10):", min_value=1, max_value=30, value=10)
monthly_limit = st.number_input("Enter your monthly limit or initial balance ($):", min_value=0.0, value=10.0)

if st.button("Get Usage Data"):
    try:
        display_usage_and_cost_for_period(openai_api_key, days, monthly_limit)
    except Exception as e:
        st.error(f"Error: {e}")
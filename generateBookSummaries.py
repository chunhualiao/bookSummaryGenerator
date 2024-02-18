# Author  : Chunhua Liao
# Using GPT models to generate book summary

# To run this program
# On Linux or macOS
# export OPENAI_API_KEY='your_openai_api_key_here'
#---------------------------------------------

from openai import OpenAI
import re
import csv
import os
import time
from pathlib import Path

#---------------------------------------------
# global variables
# a txt file providing book information
BOOK_LIST_FILE = 'bookList.txt'

#NUM_BOOKS = 5  # Change this to limit the number of books to process, used for debugging
NUM_BOOKS = None  # None will be treated as all in the code

# reference web gpt-4: 509 words
WORD_COUNT = 550  # Change this for summary length
MAX_TOKENS=int(WORD_COUNT*2)  # approximation of token count= 1 word * 1.4  

total_time=0 
# https://openai.com/pricing
#MODEL_ID="gpt-3.5-turbo-instruct" # /v1/completions (Legacy), not compatible with chat mode!!
# https://platform.openai.com/docs/models/model-endpoint-compatibility
#MODEL_ID="gpt-3.5-turbo" 
# best model so far
# https://huggingface.co/spaces/lmsys/chatbot-arena-leaderboard
MODEL_ID="gpt-4-1106-preview" 

# how many books have been summarized, also used as the book ID or serial number.
book_count = 0 
#---------------------------------------------
# Function to get the OpenAI API key from environment variables
def get_openai_api_key():
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        raise ValueError("OpenAI API key not found. Please set the OPENAI_API_KEY environment variable.")
    # assign to a global variable!!
    return api_key

#---------------------------------------------
# function to compute api calling costs
"""
https://openai.com/pricing
Model	Input	Output
gpt-4-0125-preview	$0.01 / 1K tokens	$0.03 / 1K tokens
gpt-4-1106-preview	$0.01 / 1K tokens	$0.03 / 1K tokens
gpt-4-1106-vision-preview	$0.01 / 1K tokens	$0.03 / 1K tokens

Model	Input	Output
gpt-4	$0.03 / 1K tokens	$0.06 / 1K tokens
gpt-4-32k	$0.06 / 1K tokens	$0.12 / 1K tokens

Model	Input	Output
gpt-3.5-turbo-0125	$0.0005 / 1K tokens	$0.0015 / 1K tokens
gpt-3.5-turbo-instruct	$0.0015 / 1K tokens	$0.0020 / 1K tokens
"""
def compute_api_call_cost(model_id, input_token_count, output_token_count):
    # Define the cost per 1K tokens for each model for input and output
    pricing = {
        'gpt-4-0125-preview': {'input': 0.01, 'output': 0.03},
        'gpt-4-1106-preview': {'input': 0.01, 'output': 0.03},
        'gpt-4-1106-vision-preview': {'input': 0.01, 'output': 0.03},
        'gpt-4': {'input': 0.03, 'output': 0.06},
        'gpt-4-32k': {'input': 0.06, 'output': 0.12},
        'gpt-3.5-turbo-0125': {'input': 0.0005, 'output': 0.0015},
        'gpt-3.5-turbo-instruct': {'input': 0.0015, 'output': 0.0020},
    }

    # Check if the model_id is in the pricing dictionary
    if model_id in pricing:
        # Calculate the cost for input and output tokens
        input_cost = (input_token_count / 1000) * pricing[model_id]['input']
        output_cost = (output_token_count / 1000) * pricing[model_id]['output']
        # Calculate total cost
        total_cost = input_cost + output_cost
        return total_cost
    else:
        # Model ID not found
        raise ValueError(f"Model ID '{model_id}' not found in pricing information.")

#---------------------------------------------
# Function to estimate the number of words in a string
def estimate_word_count(text):
    return len(text.split())

#---------------------------------------------
# Function to parse the book list file
def parse_book_list(file_path):
    books = []
    with open(file_path, 'r', encoding='utf-8') as file:
        # Attempt to detect and handle CSV format issues
        try:
            reader = csv.DictReader((line.replace('\0', '') for line in file), delimiter='|')
            # Trim spaces from headers
            reader.fieldnames = [name.strip() for name in reader.fieldnames]
            headers = reader.fieldnames
            # Check for the presence of expected headers
            headers = reader.fieldnames
            expected_headers = ['Recommended by', 'Books', 'Recommendation Count']
            missing_headers = [h for h in expected_headers if h not in headers]
            if missing_headers:
                raise ValueError(f"Missing expected headers: {missing_headers}. Found headers: {headers}")
            
            for row in reader:
                if row['Books'].strip() == '--':
                   print(f"Skipping row with 'Books' value as '--': {row}")
                   continue

                try:
              
                    book = row['Books'].strip(), row['Recommendation Count'].strip()  # Adjusted to remove leading space in key
                    
                    books.append(book)
                except KeyError as e:
                    # Provide a detailed error message for debugging
#                    raise KeyError(f"KeyError: The key {e} is missing from the row. Available keys are: {list(row.keys())}")
                     print(f"Warning: The key {e} is missing from the row. Available keys are: {list(row.keys())}. This row will be skipped.")
        except Exception as e:
            # Catch and re-raise any parsing errors with additional context
            raise Exception(f"Failed to parse book list from {file_path}: {e}")
#    return books[:NUM_BOOKS]
    return books

#---------------------------------------------
# Function to generate summaries using chat mode
def generate_summaries(client, books):
    global book_count # Required to modify the global object
    global total_time
    total_cost = 0
    for book, count in books:
        start_time = time.time()  # Capture start time

        book_count += 1
        # use the long book name in the prompt to provide more context
        # the long name has book title + author info
        # 
        #prompt = f"Please summarize the top 10 main points of the book titled {book} in {WORD_COUNT} words."
#optimized prompt suggested by GPT-4        
        prompt = f"Provide a concise summary highlighting the ten most important insights from the book titled {book}, using exactly {WORD_COUNT} words."
        # check the existence of summary.txt file, if it exists, skip this book
        # Regular expression to extract text within double quotes
        match = re.search(r'"(.*?)"', book)
        if match:
            book = match.group(1)  # This is the text within the double quotes
#           print(book)
        else:
            print("Warning: No book name in double quotes is found.")
#        file_name = f"{book}.summary.txt"
# Replace any character that is not a letter (a-z, A-Z) or digit (0-9) with a hyphen
        sanitized_book_name = re.sub(r'[^a-zA-Z0-9]', '-', book)
# prepend a three digit serial number, using markedown format for easier reading
        file_name = f"{book_count:03}_{sanitized_book_name}.summary.md"
 
        if Path(file_name).exists():
          print(f"The file '{file_name}' already exists. Skipping it...")
          continue
      
        # https://platform.openai.com/docs/api-reference/chat/create
        response = client.chat.completions.create(model= MODEL_ID,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
# What sampling temperature to use, between 0 and 2. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic.        
        temperature=0.6, # 
        max_tokens=MAX_TOKENS)

        summary = response.choices[0].message.content.strip()
# https://help.openai.com/en/articles/6614209-how-do-i-check-my-token-usage        
        input_token_count = response.usage.prompt_tokens;
        output_token_count = response.usage.completion_tokens

        output_word_count = estimate_word_count(summary)

        with open(file_name, 'w', encoding='utf-8') as file:
            file.write(summary)
        print(f"{book_count}: Summary of {output_word_count} words for '{book}' saved to {file_name}. input tokens={input_token_count}, output tokens={output_token_count}")

#        input_cost = (input_token_count / 1000) * COST_PER_THOUSAND_INPUT_TOKENS
#        output_cost = (output_token_count / 1000) * COST_PER_THOUSAND_OUTPUT_TOKENS
#        iteration_cost = input_cost + output_cost
        iteration_cost = compute_api_call_cost (MODEL_ID, input_token_count, output_token_count)
        
        total_cost += iteration_cost

        end_time = time.time()  # Capture end time
        duration = end_time - start_time  # Calculate duration of this iteration
        total_time += duration  # Update total accumulated time
    
        print(f"Iteration {book_count}: {duration:.4f} seconds")

    return total_cost

#---------------------------------------------
# Main program
if __name__ == "__main__":
    client = OpenAI(api_key=get_openai_api_key())
    books = parse_book_list(BOOK_LIST_FILE)
#    print (books[:10]) # test first 10 books

    # When slicing
    books_to_process = books if NUM_BOOKS is None else books[:NUM_BOOKS]
    total_cost = generate_summaries(client, books_to_process)

#    total_cost = generate_summaries(books[:NUM_BOOKS])
#    total_cost = generate_summaries(books)
    print(f"Estimated total cost for summarizing {book_count} books: ${total_cost:.6f}")
    # After the loop completes, print the total time
    print(f"Total accumulated time: {total_time:.4f} seconds.")


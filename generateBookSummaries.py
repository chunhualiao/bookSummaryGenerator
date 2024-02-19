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

NUM_BOOKS = 5  # Change this to limit the number of books to process, used for debugging
NUM_BOOKS = None  # None will be treated as all in the code

# reference web gpt-4: 509 words
WORD_COUNT = 550  # Change this for summary length
MAX_TOKENS=int(WORD_COUNT*2)  # approximation of token count= 1 word * 1.4  

total_time=0 
# https://openai.com/pricing
#MODEL_ID="gpt-3.5-turbo-instruct" # /v1/completions (Legacy), not compatible with chat mode!!
# https://platform.openai.com/docs/models/model-endpoint-compatibility
# best model so far
# https://huggingface.co/spaces/lmsys/chatbot-arena-leaderboard
MODEL_ID="gpt-4-1106-preview" 

# use low cost 3.5 for translation
TRANSLATION_MODEL_ID="gpt-3.5-turbo-0125"

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
    path = Path("results") / MODEL_ID
# add path to the result files        
    # Ensure the path exists; create it if it doesn't
    path.mkdir(parents=True, exist_ok=True)
    
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
        file_name = f"{book_count:03}-{sanitized_book_name}.summary.md"

        full_path = path / file_name
        file_name = str(full_path)

        if Path(file_name).exists():
          print(f"The file '{file_name}' already exists. Skipping it...")
          continue
      
        print(f"Processing '{file_name}'...")
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
# Function to translate summaries using chat mode
def translate_summaries(client, bookCountLimit):

    global total_time
    total_cost = 0
# input file path, derived from MODEL_ID selected for the summarization task
    path = Path("results") / MODEL_ID
    output_path = Path("results") / MODEL_ID / "chinese"
    output_path.mkdir(parents=True, exist_ok=True)

    book_count = 0 
    # Check if the path exists
    if not path.exists():
        print(f"The input .md file path '{path}' does not exist.")
        return  # Exit the function if the path does not exist

    # Iterate over all .md files in the specified directory
    for md_file in path.glob('*.md'):
        start_time = time.time()  # Capture start time

        book_count += 1

        if bookCountLimit is not None and book_count > bookCountLimit:
            print(f"Reaching the limit of {bookCountLimit}, skip the rest of files ... ")
            break  # Exit the loop if book_count exceeds bookCountLimit

        input_md_file = md_file.resolve()
        
        print(f"{book_count} Translating {input_md_file}...")
        # Read the content of the input file
        with open(input_md_file, 'r', encoding='utf-8') as file:
            input_text = file.read()

        prompt = f"Translate the following English text to Simplified Chinese:\n\n{input_text}."
        # check the existence of the output_path summary.md file, if it exists, skip this translation
        output_md_file = output_path / input_md_file.name

        output_md_file_name = output_md_file.resolve(); 
        if Path(output_md_file_name).exists():
          print(f"The file '{output_md_file_name}' already exists. Skipping it...")
          continue
      
        print(f"Translating '{input_md_file}'...")
        # https://platform.openai.com/docs/api-reference/chat/create
        response = client.chat.completions.create(model= TRANSLATION_MODEL_ID,
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

# regular English words counting method does not aply to Chinese. We use len() for now.
        output_word_count = len(summary)

        with open(output_md_file_name, 'w', encoding='utf-8') as file:
            file.write(summary)
        print(f"{book_count}: Translated summary of {output_word_count} words saved to {output_md_file_name}. input tokens={input_token_count}, output tokens={output_token_count}")

        # note : use translation model id here!
        iteration_cost = compute_api_call_cost (TRANSLATION_MODEL_ID, input_token_count, output_token_count)
        
        total_cost += iteration_cost

        end_time = time.time()  # Capture end time
        duration = end_time - start_time  # Calculate duration of this iteration
        total_time += duration  # Update total accumulated time
    
        print(f"Iteration {book_count}: {duration:.4f} seconds")

    return total_cost

def process_book_summaries(client, book_list_file, num_books=None):
    # Assuming the necessary variables and functions (`parse_book_list`, `generate_summaries`, etc.) 
    # are defined elsewhere in the script

    # books = parse_book_list(BOOK_LIST_FILE)  # Original line 301
    books = parse_book_list(book_list_file)
    
    # When slicing
    books_to_process = books if num_books is None else books[:num_books]
    total_cost = generate_summaries(client, books_to_process)
    
    print(f"Estimated total cost for summarizing {len(books_to_process)} books: ${total_cost:.6f}")
    # Assuming 'total_time' is calculated within `generate_summaries` or passed back
    print(f"Total accumulated time: {total_time:.4f} seconds.")
    return total_cost

#---------------------------------------------
# Main program
if __name__ == "__main__":
    client = OpenAI(api_key=get_openai_api_key())

    total_cost = process_book_summaries(client, BOOK_LIST_FILE, NUM_BOOKS)

    total_cost += translate_summaries(client, NUM_BOOKS)
    print(f"Estimated total cost for translating {book_count} books: ${total_cost:.6f}")
    print(f"Total accumulated time: {total_time:.4f} seconds.")


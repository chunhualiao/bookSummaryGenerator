import openai
import csv
import os

# On Linux or macOS
# export OPENAI_API_KEY='your_openai_api_key_here'

# Configuration variables
BOOK_LIST_FILE = 'bookList.txt'
NUM_BOOKS = 2  # Change this to limit the number of books to process
WORD_COUNT = 200  # Change this for summary length
COST_PER_THOUSAND_TOKENS = 0.02  # Adjust based on the latest OpenAI pricing

# https://openai.com/pricing
MODEL_ID="gpt-3.5-turbo-instruct"
COST_PER_THOUSAND_INPUT_TOKENS = 0.0015  # Update with the actual cost per thousand input tokens
COST_PER_THOUSAND_OUTPUT_TOKENS = 0.002  # Update with the actual cost per thousand output tokens

# Function to estimate the number of tokens in a string
def estimate_token_count(text):
    # Rough estimation of token count: average word length in English is around 4-5 characters plus space
    return len(text.split())

# Function to get the OpenAI API key from environment variables
def get_openai_api_key():
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        raise ValueError("OpenAI API key not found. Please set the OPENAI_API_KEY environment variable.")
    return api_key

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

# Function to generate summaries using chat mode
def generate_summaries(books, api_key):
    total_cost = 0
    for book, count in books:
        prompt = f"Please summarize the main points of the book titled {book} in {WORD_COUNT} words."
        input_token_count = estimate_token_count(prompt)
        response = openai.ChatCompletion.create(
#            model="gpt-4",
#            model="gpt-3.5-turbo-instruct",
            model= MODEL_ID,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=WORD_COUNT*5,  # Approximation
            api_key=api_key
        )
        summary = response['choices'][0]['message']['content'].strip()
        output_token_count = estimate_token_count(summary)


        # Regular expression to extract text within double quotes
        match = re.search(r'"(.*?)"', book)
        if match:
            book = match.group(1)  # This is the text within the double quotes
            print(book)
        else:
            print("No book name found.")

        file_name = f"{book}.summary.txt"
        with open(file_name, 'w', encoding='utf-8') as file:
            file.write(summary)
        print(f"Summary for '{book}' saved to {file_name}")

        input_cost = (input_token_count / 1000) * COST_PER_THOUSAND_INPUT_TOKENS
        output_cost = (output_token_count / 1000) * COST_PER_THOUSAND_OUTPUT_TOKENS
        iteration_cost = input_cost + output_cost
        
        total_cost += iteration_cost

    return total_cost

# Main program
if __name__ == "__main__":
    openai.api_key = get_openai_api_key()
    books = parse_book_list(BOOK_LIST_FILE)
#    print (books[:10]) # test first 10 books
    total_cost = generate_summaries(books[:NUM_BOOKS], openai.api_key)
    print(f"Estimated total cost for summarizing {len(books)} books: ${total_cost:.2f}")


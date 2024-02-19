import csv

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
                    book = row['Books'].strip() # row['Recommendation Count'].strip()  # Adjusted to remove leading space in key                    
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

# Function to keep the longest book name for each unique book
def keep_longest_books(book_list):
    # Sort the books by name and then by length (in reverse) to ensure longest comes first
    sorted_books = sorted(book_list, key=lambda x: (x.split(" by ")[0], -len(x)))
    unique_books = []

    for book in sorted_books:
        # Check if the current book is a more detailed version of the last added book
        if not unique_books or not book.startswith(unique_books[-1].split(" by ")[0]):
            unique_books.append(book)
        else:
            # Replace the last book if the current one is longer
            if len(book) > len(unique_books[-1]):
                unique_books[-1] = book

    # Return the list of unique books, now containing only the longest version of each
    return unique_books

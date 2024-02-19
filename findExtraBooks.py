# new_script.py or any other script
from utils import parse_book_list
import re

"""
def parse_booklist(file_path):
    # Set to store book titles from bookList.txt
    booklist_titles = set()
    with open(file_path, 'r') as file:
        next(file)  # Skip the header row
        for line in file:
            # Extract the book title between quotes
            book_title = line.split('|')[1].strip().split('"')[1].split(" by ")[0].strip()
            booklist_titles.add(book_title.lower())  # Add to set in lowercase for case-insensitive comparison
    return booklist_titles
"""

# Function to normalize book titles
def normalize_title(title):
    # Convert to lowercase
    lower_case_title = title.lower()
    # Remove punctuation
    no_punctuation_title = re.sub(r'[^\w\s]', '', lower_case_title)
    # Optional: Remove common words or author names if needed
    # For simplicity, we'll just use the lowercase, punctuation-free version
    return no_punctuation_title

def parse_all_books(file_path):
    # List to store all book titles from all_books.txt
    all_books_titles = []
    with open(file_path, 'r') as file:
        for line in file:
            # Extract the book title, possibly with author
            book_title = line.strip().split(" by ")[0].strip()
            all_books_titles.append(book_title.lower())  # Store in lowercase for case-insensitive comparison
    return all_books_titles

def find_books_not_in_booklist(all_books, booklist):
    # Normalize titles in both lists
    booklist = [normalize_title(book) for book in booklist]
    all_books = [normalize_title(book) for book in all_books]
            
    # Find books not in bookList.txt
    not_in_booklist = [book for book in all_books if book not in booklist]
    return not_in_booklist

# File paths
booklist_file_path = 'bookList.txt'
all_books_file_path = 'results/all_books.txt'

# Parse the files
booklist_titles = parse_book_list(booklist_file_path)

# for each book in booklist_titles, remove the " characters within the book name if any
booklist_titles = [book.replace('"', '') for book in booklist_titles]

#sort the list
booklist_titles = sorted(booklist_titles)

# save the sorted list into a text file named bookList_sorted.txt
with open('bookList_sorted.txt', 'w') as file:
    for book in booklist_titles:
        file.write(book + '\n')    

# print the sorted list
#for book in booklist_titles:
#    print(book)


all_books_titles = parse_all_books(all_books_file_path)
# Find books not included in bookList.txt
books_not_included = find_books_not_in_booklist(all_books_titles, booklist_titles)

# Print results
print("Books from all_books.txt not included in bookList.txt:")
for book in books_not_included:
    print(book)

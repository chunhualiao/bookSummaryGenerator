
# read all the files under results/books
# list all .txt files in the directory
import os

from utils import keep_longest_books
# Function to keep the longest book name for each unique book


# a list storing all books
all_books = []
with open("results/all_books_with_old.txt", 'r') as file:
    content = file.read()
    # each line is a book, append to all_books
    all_books.extend(content.split('\n'))

# sort the books in all_books
all_books.sort()

# remove duplicates
all_books = list(set(all_books))

all_books.sort()
# remove duplicates with extra sub titles and author names. 

from utils import keep_longest_books

# Test the updated function with the new list of books
longest_books = keep_longest_books(all_books)

# save longest_books into a new file
# save to parent directory to avoid conflicts
with open("results/all_books_final.txt", 'w') as file:
    for book in longest_books:
        file.write(book + '\n') 




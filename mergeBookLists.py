#
# we have a list of txt files in json format, each with the list of books. 
# the files are located under results/books
# they have names like 001Jeff-Bezos_books.txt .. 050James-Ratcliffe_books.txt
# we need to merge all the books into one big list of books.
import json

# merge all the books into one big list

# read all the files under results/books
# list all .txt files in the directory
import os

# Function to keep the longest book name for each unique book
#def keep_longest_books(book_list):

# List all .txt files in the directory
txt_files = [file for file in os.listdir("results/books") if file.endswith(".txt")]

# Read all the files under results/books
# each file is json format with content like the following
"""
{
    "books": [
        "Atlas Shrugged by Ayn Rand",
        "Poor Charlie's Almanack by Charles T. Munger",
        "Steve Jobs by Walter Isaacson",
        "Made in Japan by Akio Morita",
        "Sapiens: A Brief History of Humankind by Yuval Noah Harari",
        "The Art of War by Sun Tzu",
        "Business @ the Speed of Thought by Bill Gates",
        "The World Is Flat by Thomas L. Friedman",
        "The Road Ahead by Bill Gates",
        "The Innovator's Dilemma by Clayton M. Christensen"        
    ]
}
"""
# a list storing all books
all_books = []
for txt_file in txt_files:
    with open(os.path.join("results/books", txt_file), 'r') as file:
        content = file.read()
        # Process the content of each file here
        # the content is json format, parse it into a dictionary
        data = json.loads(content)
        # append the books into all_books
        all_books.extend(data['books'])

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
with open("results/all_books.txt", 'w') as file:
    for book in longest_books:
        file.write(book + '\n') 




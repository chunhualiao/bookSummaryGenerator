# bookSummaryGenerator

A python program does the following
* read and parse bookList.txt
  * the book list has 186 books recommended by the richest people in the world.
* for each book in the list, it asks a GPT model to generate a 10-point summary
* save result into a markdown file named ID-book.summary.md
* estimate the dollar amount costs of calling OpenAI APIs
* measure the time spent on each book and total execution time.

Some results are stored into results folder.


How to run the program within a Linux or macOS terminal
* Creat a virtual environment first
  * python3 -m venv .venv
  * source .venv/bin/activate

Now within your virtual environment, do the following:
* pip install openai 
* export OPENAI_API_KEY='your_openai_api_key_here'
* python generateBookSummaries.py

Note that for each book, GPT-4 model takes around 30 seconds to summarize it.


The code is configurable. 

Please edit generateBookSummaries.py and look through the configuraiton part in the beginning.
* you can change the model used
* how many books to summarize
* prompt used: this is in the middle of the code
* temperature of a model



# bookSummaryGenerator

A python program does the following
* read and parse bookList.txt
* for each book in the list, ask a GPT model to generate a 10-point summary
* save result into a markdown file named bool.summary.md

Some results are stored into results folder


How to run the program
* Creat a virtual environment first
  * python3 -m venv .venv
  * source .venv/bin/activate

Now within your virtual environment, do the following
* pip install openai 
* export OPENAI_API_KEY='your_openai_api_key_here'
* python generateBookSummaries.py

The code is configurable. 

Please edit generateBookSummaries.py and look through the configuraiton part in the beginning.



# bookSummaryGenerator

A python program does the following
* read and parse bookList.txt (or results/all_books_final.txt)
  * the book list has 206 (or 541) books recommended by the richest people in the world.
  * You can add new books at the end of this file. Run the program to generate summary text for them.
* for each book in the list, it asks a GPT model to generate a 10-point summary
* save result into a markdown file named ID-book.summary.md
* estimate the dollar amount costs of calling OpenAI APIs
* measure the time spent on each book and total execution time.
* additionally, it translates the English summary .md files into Chinese versions

Results are stored into results folder.
* results/MODEL_ID/id-book-name.summary.md
* results/MODEL_ID/chinese/id-book-name.summary.md

How to run the program within a Linux or macOS terminal
* Creat a virtual environment first
  * python3 -m venv .venv
  * source .venv/bin/activate

Now within your virtual environment, do the following:
* pip install openai 
* export OPENAI_API_KEY='your_openai_api_key_here'
  * alternatively , put export OPENAI_API_KEY='your_openai_api_key_here' into ~/set.openai.key 
* python generateBookSummaries.py

Note that for each book, GPT-4 model takes around 30 seconds to summarize it.


The code is configurable. 

Please edit generateBookSummaries.py and look through the configuraiton part in the beginning.
* you can change the model used
* how many books to summarize
* prompt used: this is in the middle of the code
* temperature of a model


Example execution screen output:

```
bookSummaryUsingGPT$ make check

...

184: Summary of 530 words for 'Deep Learning' saved to 184-Deep-Learning-summary-txt. input tokens=47, output tokens=698
Iteration 184: 46.1335 seconds
185: Summary of 555 words for 'Genome: The Autobiography of a Species in 23 Chapters' saved to 185-Genome--The-Autobiography-of-a-Species-in-23-Chapters-summary-txt. input tokens=58, output tokens=690
Iteration 185: 30.8259 seconds
186: Summary of 539 words for 'Superintelligence: Paths, Dangers, Strategies' saved to 186-Superintelligence--Paths--Dangers--Strategies-summary-txt. input tokens=54, output tokens=730
Iteration 186: 22.6418 seconds
Estimated total cost for summarizing 186 books: $3.836760
Total accumulated time: 5457.6185 seconds.

....

207 Translating /home/liao/workspace/bookSummaryUsingGPT/results/gpt-4-1106-preview/205-Mind-of-Napoleon--A-Selection-of-His-Written-and-Spoken-Words.summary.md...
Translating '/home/liao/workspace/bookSummaryUsingGPT/results/gpt-4-1106-preview/205-Mind-of-Napoleon--A-Selection-of-His-Written-and-Spoken-Words.summary.md'...
207: Translated summary of 1049 words saved to /home/liao/workspace/bookSummaryUsingGPT/results/gpt-4-1106-preview/chinese/205-Mind-of-Napoleon--A-Selection-of-His-Written-and-Spoken-Words.summary.md. input tokens=696, output tokens=1256
Iteration 207: 23.1297 seconds
208 Translating /home/liao/workspace/bookSummaryUsingGPT/results/gpt-4-1106-preview/206-Poor-Charlie-s-Almanack--The-Wit-and-Wisdom-of-Charles-T--Munger.summary.md...
Translating '/home/liao/workspace/bookSummaryUsingGPT/results/gpt-4-1106-preview/206-Poor-Charlie-s-Almanack--The-Wit-and-Wisdom-of-Charles-T--Munger.summary.md'...
208: Translated summary of 1049 words saved to /home/liao/workspace/bookSummaryUsingGPT/results/gpt-4-1106-preview/chinese/206-Poor-Charlie-s-Almanack--The-Wit-and-Wisdom-of-Charles-T--Munger.summary.md. input tokens=743, output tokens=1201
Iteration 208: 24.8758 seconds
Estimated total cost for translating 206 books: $0.453361
Total accumulated time: 3949.7468 seconds.


```


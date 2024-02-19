# must set bash, or source is not available!
SHELL := /bin/bash

# make check do the summarization and translation, generating individual .md files
# ---------------------------------------------------------------
check:generateBookSummaries.py
	. .venv/bin/activate && . ~/set.openai.key && python $^

clean:

# make all will consolidate all .md files to a single one
# ---------------------------------------------------------------
# all all-in-one targets	
all:all.gpt.4.chinese.md all.gpt.4.english.md  all.gpt.4.chinese.pdf all.gpt.4.english.pdf
	mv $^ all-in-one/.
# md.header is needed to specify chinese fonts needed	
all.gpt.4.chinese.md:
	cat ./results/gpt-4-1106-preview/chinese/*.md > all.gpt.4.chinese.md.temp
	cat results/md.header all.gpt.4.chinese.md.temp > all.gpt.4.chinese.md
	rm all.gpt.4.chinese.md.temp
all.gpt.4.chinese.pdf: all.gpt.4.chinese.md
	pandoc $^ -o $@ --pdf-engine=xelatex

all.gpt.4.english.md:
	cat ./results/gpt-4-1106-preview/*.md > all.gpt.4.english.md
all.gpt.4.english.pdf: all.gpt.4.english.md
	pandoc $^ -o $@ --pdf-engine=xelatex	

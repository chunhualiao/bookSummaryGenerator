# must set bash, or source is not available!
SHELL := /bin/bash

#GPT_VERSION=gpt-3.5-turbo-0125
GPT_VERSION=gpt-4-1106-preview

# make check do the summarization and translation, generating individual .md files
# ---------------------------------------------------------------
check:generateBookSummaries.py
	. .venv/bin/activate && . ~/set.openai.key && python $^

clean:
	rm -rf all.${GPT_VERSION}.chinese.temp.md all.${GPT_VERSION}.chinese.md all.${GPT_VERSION}.english.md all.${GPT_VERSION}.chinese.pdf all.${GPT_VERSION}.english.pdf
# make all will consolidate all .md files to a single one
# ---------------------------------------------------------------
# all all-in-one targets	
all:all.${GPT_VERSION}.chinese.md all.${GPT_VERSION}.english.md  all.${GPT_VERSION}.chinese.pdf all.${GPT_VERSION}.english.pdf
	mv $^ all-in-one/.

# echo commands without any arguments are used to add empty lines. 
all.${GPT_VERSION}.chinese.temp.md:
	> $@
	for file in ./results/${GPT_VERSION}/chinese/*.md; do \
		filename=$$(basename -- "$$file" .md); \
		echo >> $@; \
		echo "# $$filename" >> $@; \
		echo >> $@; \
		cat "$$file" >> $@; \
		echo  >> $@; \
	done

all.${GPT_VERSION}.english.md:
	> $@
	for file in ./results/${GPT_VERSION}/*.md; do \
		filename=$$(basename -- "$$file" .md); \
		echo >> $@; \
		echo "# $$filename" >> $@; \
		echo >> $@; \
		cat "$$file" >> $@; \
		echo  >> $@; \
	done

# md.header is needed to specify chinese fonts needed	
all.${GPT_VERSION}.chinese.md:all.${GPT_VERSION}.chinese.temp.md results/md.header
	cat results/md.header $< > $@

# generic rule to build pdf from md
%.pdf: %.md
	pandoc $^ -o $@ --pdf-engine=xelatex

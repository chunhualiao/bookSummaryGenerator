# must set bash, or source is not available!
SHELL := /bin/bash

# make check do the summarization and translation, generating individual .md files
# ---------------------------------------------------------------
check:generateBookSummaries.py
	. .venv/bin/activate && . ~/set.openai.key && python $^

clean:
	rm -rf all.gpt.4.chinese.temp.md all.gpt.4.chinese.md all.gpt.4.english.md all.gpt.4.chinese.pdf all.gpt.4.english.pdf
# make all will consolidate all .md files to a single one
# ---------------------------------------------------------------
# all all-in-one targets	
all:all.gpt.4.chinese.md all.gpt.4.english.md  all.gpt.4.chinese.pdf all.gpt.4.english.pdf
	mv $^ all-in-one/.

# echo commands without any arguments are used to add empty lines. 
all.gpt.4.chinese.temp.md:
	> $@
	for file in ./results/gpt-4-1106-preview/chinese/*.md; do \
		filename=$$(basename -- "$$file" .md); \
		echo >> $@; \
		echo "# $$filename" >> $@; \
		echo >> $@; \
		cat "$$file" >> $@; \
		echo  >> $@; \
	done

all.gpt.4.english.md:
	> $@
	for file in ./results/gpt-4-1106-preview/*.md; do \
		filename=$$(basename -- "$$file" .md); \
		echo >> $@; \
		echo "# $$filename" >> $@; \
		echo >> $@; \
		cat "$$file" >> $@; \
		echo  >> $@; \
	done

# md.header is needed to specify chinese fonts needed	
all.gpt.4.chinese.md:all.gpt.4.chinese.temp.md results/md.header
	cat results/md.header $< > $@

# generic rule to build pdf from md
%.pdf: %.md
	pandoc $^ -o $@ --pdf-engine=xelatex

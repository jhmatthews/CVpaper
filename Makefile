##################################
#
# Makefile for pdflatex with bibliography
#
##################################

FILE=paper

DATE := $(shell date +'%y%m%d')

CMD = latex
PCMD = pdflatex

all: 
	pdflatex ${FILE}
	bibtex ${FILE}
	pdflatex ${FILE}
	pdflatex ${FILE}
	open -a preview ${FILE}.pdf

draft:
	python scripts/mnras.py draft.tex draft_mnras.tex
	${CMD} draft
	${CMD} draft_mnras
	bibtex draft 
	bibtex draft_mnras 
	${CMD} draft
	${CMD} draft_mnras
	${CMD} draft
	${CMD} draft_mnras
	dvips draft -o cvwinds_draft_jm_$(DATE).ps
	dvips draft_mnras -o cvwinds_draft_mnras_jm_$(DATE).ps
	ps2pdf cvwinds_draft_mnras_jm_$(DATE).ps
	ps2pdf cvwinds_draft_jm_$(DATE).ps
	cp cvwinds_draft_mnras_jm_$(DATE).pdf cvpaper_latest.pdf
	open -a preview cvpaper_latest.pdf 
	#open -a preview cvwinds_draft_jm_$(DATE).pdf
#	cp draft_mnras.pdf ~/Dropbox/Python/CVpaper/
#	cp draft.pdf ~/Dropbox/Python/CVpaper/draft_preprint.pdf
# draft:
# 	python scripts/mnras.py draft.tex draft_mnras.tex
# 	pdflatex draft
# 	bibtex draft
# 	pdflatex draft
# 	pdflatex draft
# 	pdflatex draft_mnras
# 	bibtex draft_mnras
# 	pdflatex draft_mnras
# 	pdflatex draft_mnras
# 	open -a preview draft_mnras.pdf

diffs:
	latexdiff --flatten old.tex draft.tex > diffs.tex
	python scripts/mnras.py diffs.tex diffs_mnras.tex
	${CMD} diffs
	${CMD} diffs_mnras
	bibtex diffs 
	bibtex diffs_mnras 
	${CMD} diffs
	${CMD} diffs_mnras
	${CMD} diffs
	${CMD} diffs_mnras
	dvips diffs -o diffs_$(DATE).ps
	dvips diffs_mnras -o diffs_mnras_$(DATE).ps
	ps2pdf diffs_$(DATE).ps
	ps2pdf diffs_mnras_$(DATE).ps

	cp diffs_mnras_$(DATE).pdf cvpaper_diff_latest.pdf
	open -a preview diffs_mnras_$(DATE).pdf 


rates:
	${PCMD} rates
	bibtex rates
	${PCMD} rates
	${PCMD} rates 

	
clean:	
	/bin/rm -f *.aux *.log *.dvi 

cleandates:
	/bin/rm -f *.dvi cvwinds*.pdf diffs*.pdf *.ps *.log *.aux



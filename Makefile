##################################
#
# Makefile for pdflatex with bibliography
#
##################################

FILE=paper

DATE := $(shell date +'%y%m%d')

CMD = latex

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


	#open -a preview cvwinds_draft_mnras_jm_$(DATE).pdf cvwinds_draft_jm_$(DATE).pdf
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
	
clean:	
	/bin/rm -f *.aux *.log *.dvi

cleandates:
	/bin/rm -f *.dvi *.pdf *.ps



##################################
#
# Makefile for latex with bibliography
#
##################################


DATE := $(shell date +'%y%m%d')

CMD = latex
PCMD = pdflatex


all:
	${CMD} draft_mnras
	bibtex draft_mnras 
	${CMD} draft_mnras
	${CMD} draft_mnras
	dvips draft_mnras -o cvwinds_draft_mnras_jm.ps
	
clean:	
	/bin/rm -f *.aux *.log *.dvi 

cleandates:
	/bin/rm -f *.dvi cvwinds*.pdf diffs*.pdf *.ps *.log *.aux



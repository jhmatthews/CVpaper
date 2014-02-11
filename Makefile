##################################
#
# Makefile for pdflatex with bibliography
#
##################################

FILE=paper

all: 
	pdflatex ${FILE}
	bibtex ${FILE}
	pdflatex ${FILE}
	pdflatex ${FILE}
	open -a preview ${FILE}.pdf

plan:
	pdflatex plan
	bibtex plan
	pdflatex plan
	pdflatex plan
	open -a preview plan.pdf
	
clean:	
	/bin/rm -f *.aux 



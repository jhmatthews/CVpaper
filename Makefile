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
	python scripts/mnras.py plan.tex plan_mnras.tex
	pdflatex plan
	pdflatex plan_mnras
	open -a preview plan.pdf plan_mnras.pdf
	
clean:	
	/bin/rm -f *.aux 



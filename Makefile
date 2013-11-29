FILE=paper

all: 
	pdflatex ${FILE}
	bibtex ${FILE}
	pdflatex ${FILE}
	pdflatex ${FILE}
	open -a preview ${FILE}.pdf
	
clean:	
	/bin/rm -f *.aux 



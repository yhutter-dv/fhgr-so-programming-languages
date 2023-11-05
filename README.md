# Programming Language Insights based on Stackoverflow Survey
A simple web application using rdflib and the stackoverflow survey results to display useful information about programming languages. 

## Documentation
As a base template the awesome pandoc-latex-template from [Wandmalfarbe](https://github.com/Wandmalfarbe/pandoc-latex-template) was used.

### Onetime Setup
First make sure pandoc and the necessary latex packages are installed:
```bash
sudo pacman -S pandoc texlive
```

### Build Documentation
In order to generate the documentation simply make the `doc.sh` file executable and run it:
```bash
cd doc
chmod +x doc.sh
./doc.sh
```


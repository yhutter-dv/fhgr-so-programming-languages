#!/bin/bash
pandoc --template ./eisvogel.tex --defaults ./doc.yaml --number-sections --listings --pdf-engine=lualatex

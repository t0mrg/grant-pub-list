# grant-pub-list

Script to format publications for grant proposals. This script takes a EuropePMC exported CSV as input and uses a Jinja template to output a HTML format publication list.

## Command line parameters

- ```-p```, ```--publications```: CSV file of publications from EuropePMC
- ```-m```, ```--names```: Text file of name strings for highlighting, one per line
- ```-t```, ```--template```: Jinja template
- ```-d```, ```--destination```: Output directory

## Example command

Assumes you have created a data directory and output directory, and that the data directory contains ```europepmc.csv``` downloaded from EuropePMC and ```names.csv``` manually edited to contain any names or variants of names you would like highlighted.

```
python scripts/create_bibliography.py -p data/europepmc.csv -m data/names.txt -t templates/bibliography.jinja -d output
```
import pandas as pd
import sqlite3 as sql
from jinja2 import Template
import argparse

# parse arguments
parser = argparse.ArgumentParser()
parser.add_argument("-p", "--publications", help="CSV file of publications from EuropePMC")
parser.add_argument("-m", "--names", help="Text file of name strings for highlighting, one per line")
parser.add_argument("-t", "--template", help="Jinja template")
parser.add_argument("-d", "--destination", help="Output directory")
args = parser.parse_args()

def get_names():
    names = [i.strip() for i in open(args.names,'r').readlines()] # Names to highlight
    return(names)

def load_publications():
    data = pd.read_csv(args.publications)
    return(data)

def annotate_authors(authors, names):
    try:
        authors = authors.split("; ")
        labelled_authors = []
        for author in authors:
            if author in names:
                author = f"""<span class='highlight'>{ author }</span>"""
            labelled_authors.append(author)
        return("; ".join(labelled_authors))
    except:
        return("[NO AUTHORS LISTED]")
    
def process_grants(grants):
    grant_output = []
    grants = grants.split(",")
    for grant in grants:
        grant = grant.split(":")
        if grant[0] == '"Cancer Research UK"':
            grant_output.append(grant[1].strip('"').strip())
    return(",".join(grant_output))

def parse_data(names, data):
    publications = []
    for index, row in data.iterrows():
        publication = {}
        publication['AUTHORS'] = annotate_authors(row['AUTHORS'], names)
        publication['TITLE'] = row['TITLE']
        publication['PUBLICATION_YEAR'] = row['PUBLICATION_YEAR']
        publication['JOURNAL'] = row['JOURNAL']
        publication['VOLUME'] = row['VOLUME']
        publication['ISSUE'] = row['ISSUE']
        publication['PAGE_INFO'] = row['PAGE_INFO']
        publication['GRANTS'] = process_grants(row['GRANTS'])
        publications.append(publication)
    return(publications)

def main():
    names = get_names()
    data = load_publications()
    publications = parse_data(names, data)
    with open(args.template) as f:
        tmpl = Template(f.read())
        with open(f"{args.destination}/publications.html", 'w') as bibliography:
            bib = tmpl.render(publications=publications)
            bibliography.write(bib)

if __name__ == "__main__":
    main()
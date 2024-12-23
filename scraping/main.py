"""
Perform scraping for pseudobase and rna3dhub structures then write each record to a file.
"""

from concurrent.futures import ThreadPoolExecutor
from pseudobase import scrape_pseudobase, fetch_pseudobase_record
from rna3dhub import scrape_rna3dhub, fetch_rna3dhub_record
from write_file import write_file

def pseudobase():
    """
    Scrape, retrieve, write pseudobase structures.
    """
    pseudobase_records = scrape_pseudobase()
    for i in pseudobase_records:
        print(f'pseudobase {i} | {pseudobase_records.index(i)}')
        rec = fetch_pseudobase_record(i)
        if rec:
            write_file(rec)

def rna3dhub():
    """
    Scrape, retrieve, write pseudobase structures.
    """
    rna3dhub_records = scrape_rna3dhub()
    for i in rna3dhub_records[30:]:
        print(f'rnahub3dhub {i} | {rna3dhub_records.index(i)}')
        rec = fetch_rna3dhub_record(i)
        if rec:
            write_file(rec)

if __name__ == "__main__":
    pseudobase()

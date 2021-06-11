This is a project that I worked on with Jasper Tsai, in Spring 2021. We significantly updated the script I wrote nearly a year before, used data that I had been collecting since April, and did some preliminary analysis for the current dataset. 

code: Folder for the three Python scripts used in this project 

- AllScrapes.py: Python module that scrapes Indeed job listings, with customizable parameters. This class is called by module-usage.py, which defines the parameters to be used. Stores the output in a local .tsv file for the specific query type, to allow for jobs that appear across multiple queries.
    
- module-usage.py: Script that imports AllScrapes, instantiates objects with some ideal parameters, and runs the scrapes. 
    
- tsv-combiner-final.py: Combines the disparate output files into one file. This inevitably creates duplicates, which would have been interesting to analyze later - e.g. which kinds of jobs have overlap, what skills are universal across this entire industry?

data: Folder for the data files, both raw and cleaned (SQLite)

- test.tsv: Data file of ~45,000 lines resulting from ~1.5 months of scraping, and combined through tsv-combiner-final.py. It is not included here, but can be downloaded from https://drive.google.com/file/d/1p_Pmpqt5qZHf1qzL4gQjvGCmnJ3AY-Wr/view?usp=sharing
    
- cleaned.sqlite: SQLite database file that contains the data from test.tsv after omitting missing information, cleaning, and parsing. Also not included, but the Webscrape-CleanUploadExtract_Final.ipynb notebook recreates it pretty quickly if missing (I delete this file before restarting & rerunning the program/kernel)

notebooks: We ended up doing everything in one notebook file, for easier code sharing & progress tracking.

- Webscrape-CleanUploadExtract_Final.ipynb: This is the main notebook file where most of the cleaning, uploading, and analysis was performed. Our report is embedded among the cells of the notebook, explaining the outputs and our conclusions; there is a button at the top that can toggle the code's visibility. 
    
- Webscrape-PreliminaryCleaning.ipynb: Preliminary data exploration & tentative data upload code. This notebook showed that ~3,000 lines consisted of junk reads, and another ~18,000 lines were more irregular, and not as easy to extract job text from. This is not the main notebook file, and is only kept around for reference. 

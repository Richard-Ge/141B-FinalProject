code: Folder for the three Python scripts used in this project 
    AllScrapes.py: Python module that scrapes Indeed job listings, with customizable parameters. This class is called by module-usage.py, which defines the parameters to be used. Stores the output in a local .tsv file for the specific query type, to allow for jobs that appear across multiple queries.
    module-usage.py: Script that imports AllScrapes, instantiates objects with some ideal parameters, and runs the scrapes. 
    tsv-combiner-final.py: Combines the disparate output files into one file. This inevitably creates duplicates, which would have been interesting to analyze later - e.g. which kinds of jobs have overlap, what skills are universal across this entire industry?

data: Folder for the data files, both raw and cleaned (SQLite)
    test.tsv: Data file of ~45,000 lines resulting from ~1.5 months of scraping, and combined through tsv-combiner-final.py. It is not included here, but can be downloaded from https://drive.google.com/file/d/1p_Pmpqt5qZHf1qzL4gQjvGCmnJ3AY-Wr/view?usp=sharing
    cleaned.sqlite: SQLite database file that contains the data from test.tsv after omitting missing information, cleaning, and parsing. Also not included, but the Webscrape-CleanUploadExtract_Final.ipynb notebook recreates it pretty quickly if missing (I delete this file before restarting & rerunning the program/kernel)

notebooks: 
    Webscrape-CleanUploadExtract_Final.ipynb: This is the main notebook file where most of the cleaning, uploading, and analysis was performed. Our report is embedded among the cells of the notebook, explaining the outputs and our conclusions; there is a button at the top that can toggle the code's visibility. 
    Webscrape-PreliminaryCleaning.ipynb: Preliminary data exploration & tentative data upload code. This notebook showed that ~3,000 lines consisted of junk reads, and another ~18,000 lines were more irregular, and not as easy to extract job text from. This is not the main notebook file, and is only kept around for reference. 

TextbookExcerpt-Comparing>2Proportions.pdf: This is an excerpt from my statistics textbook that describes how the chi-squared test is performed on multiple proportions, all of which do not have to add to 1. I found many conflicting sources regarding these chi-squared tests on the Internet, but I ultimately relied on this source. 

-------------------------------------------------------

I would also like to make sure that all of the points we can receive are accounted for: 

1. Project organization, writeup readability, and overall conclusions
Does your directory structure make sense, are the scripts separated by function, is the writeup(s) readable, can I figure out where to look from your README.md?  Are your conclusions backed up by the facts/visualizations presented?

- I have used the directory structure outlined in the project description.
- I have separated some scripts by function, where appropriate, and certain more-complex blocks have been turned into functions.
- The writeup (included among the main notebook's cells) should be fairly straightforward.
- Our conclusions are primarily backed up by the visualizations, but the possible explanations we came up with may be based on prior knowledge.

2. Code quality, readability, and efficiency
Is it easy to read the code, are the scripts modularized, are there docstrings, could I modify your code easily?

- We added comments for every block of code, and the notebook has markdown blocks embedded to explain what we did. 
- The scripts are decently split up across different purposes and blocks, although we ended up doing all the cleaning, uploading, and analysis in one notebook to streamline code sharing. 
- Docstrings have been included for every function in this program. 
- The code should be sufficiently spread out such that things could change comfortably.

3. Scientific programming, custom algorithms, and numpy use
If you write custom data processing scripts are they efficient?  Do they use numpy to its full effect/vectorize when possible?  Do you use numpy to extract custom features/create network data/etc?

- We calculated a chi-squared statistic for each skill investigated, across the proportions of each job query that mentioned that skill. 
- Numpy arrays were used to vectorize the operations, and numpy.random.chisquare() was also used to simulate the critical values of the chi-square distribution at different degrees of freedom, and therefore avoid inaccurate critical values with different df's. 

4. Data munging
Do you use the munging tools in pandas well, such as filtering, joining, grouping, transforming?  How do you handle missingness and timestamps?  Do you use indices appropriately?  Do you extract custom features with pandas?

- Much of our munging was done with base Python/SQL and not Pandas, but we did have to melt() the dataframe of proportions longer in order to display it in a multiple bar chart. 
- Any missing data was detected (length wouldn't be 7, or job ID wouldn't be 16 characters), and omitted from the database. 
- In addition to bad reads, messy job descriptions without the correct Indeed keywords were also removed.

5. Data visualization
Do you make sensible visualizations?  Do they follow the principles of data integrity?  Do you explain the visualizations and give appropriate context?  Are your visualizations rich with aesthetic mappings?

- We made many simple visualizations that showed the proportions of skills needed for each job query. 
- We also made two visualizations that were more aesthetically complex, but also more elucidating as to industry-wide patterns. 
- All of these visualizations are adequately explained. 

6. Data extraction
Do you use a web API and parse the JSON?  Do you scrape and parse HTML?  Are there other structured formats that you work with such as text data?  Do you have to crawl a website with requests?

- We scraped and parsed HTML for text; both with BeautifulSoup's get_text(), and manually, by finding text in between any '>' and '<' characters.
- We did work with the text itself by omitting entries without certain Indeed-determined keywords (i.e. "Job Description"), and searched within the text for specific skill keywords as well.

7. Data storage
Do you store your data in a relational database and interact through SQL queries?  Do you interact with your data in chunks and not read it all into memory first?

- After cleaning, the data is stored in a SQLite file, and we query it with SQL to quickly get results without storing the entire thing in RAM. 
- Chunk reading was unnecessary for us, as we were only retrieving one number at a time from the database (not much memory overhead). We also could not have used it to clean the data effectively, because many of the duplicate rows occurred with some distance from one another, and a chunk reader would often see them one at a time (i.e. deciding that no duplicates existed).

8. Interactive visualization
Do you use D3 or some other interactive data visualization tool to enable the exploration of the data?  Do you enable multiple views and filters of the data?

- We ended up not doing this in the end, due to time concerns.
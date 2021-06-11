from AllScrapes import IndeedScraper

intern_obj = IndeedScraper(["data analyst intern", "data scientist intern", "machine learning intern"], ["IndeedAnalysts.tsv", "IndeedScientists.tsv", "IndeedMLs.tsv"], pages=2)
full_obj = IndeedScraper(["data analyst", "data scientist", "machine learning"], ["IndeedAnalysts.tsv", "IndeedScientists.tsv", "IndeedMLs.tsv"], pages=3)

print(intern_obj)
print(full_obj)

intern_obj.scrape_all()
full_obj.scrape_all()

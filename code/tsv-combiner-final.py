import os; import time
start = time.time()

outputfile = "test.tsv"
allfiles = os.listdir(os.getcwd())
allfiles = [x for x in allfiles if (x[-3:]=="tsv" and x!=outputfile)] 
allfiles = ["IndeedMLs.tsv", "IndeedScientists.tsv", "IndeedAnalysts.tsv"]
print(allfiles)

## Create header for column names
with open(outputfile, "a") as outfile:
# outfile.write("Key\tTitle\tTimePosted\tTimeScraped\tCompanyDetails\tIfIntern\tDescription\n")

	## For each data file we have
	for data in allfiles:
	print(data)
	## Open that file
	with open(data, "r") as filer:
		## Discard the first line
		filer.readline()
		## For each line, in that file
		for line in filer:
			## Clean the line?
			# onejob = line.strip() #; print(onejob[0], end=", ")
			## Append the line
			outfile.write(line)
			# output file should be deleted every time

end = time.time()
print("Time needed: "+str(end-start)[:6]+" secs")

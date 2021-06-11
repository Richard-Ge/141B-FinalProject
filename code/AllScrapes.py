import requests
import bs4
import re
import time
import random

""" Temp. disabled until review/rating functionality is added again
def parseNum(inputStr):
	if("," in inputStr): 
		# if there are commas, split them out and recombine
		splitString = inputStr.split(",")
		resultStr = "".join(splitString)
	else:
		# if there aren't any, just return it
		resultStr = inputStr
	return resultStr
def pixelWidth(inputStr):
	# (measures from ": " to "px", and take whatever is in between)
	resultStr = ""
	for char in inputStr:
		if (char>='0' and char<='9') or char=='.':
			resultStr = resultStr + str(char)
		elif char=="p":
			break
	return resultStr
	"""

class IndeedScraper:
	"""
	The class itself contains the info needed for certain scrape(s). 
	We can create multiple instances for different queries&pages, like
		IndeedScraper(analyst_jobs, outfiles, pages=4)
		IndeedScraper(full_jobs, outfiles, pages=8)
		LinkedInScraper(full_jobs, outfiles, pages=2)
	"""
	queries = []
	outfiles = []
	pages = 0
	recent = True
	def __init__(self, queries, outfiles, pages=3, recent=True):
		"""
		Initializes an IndeedScraper object, with two lists (queries and
		their corresponding output files), the number of pages for all of 
		those queries, and whether to sort by recency in the URLs.
		"""
		self.queries = queries    # list of n
		self.outfiles = outfiles  # list of n
		self.pages = pages
		self.recent = recent

	def __str__(self):
		"""
		This turns the instance into a string, and allows us to easily see 
		what we're running in the program.
		"""
		return """Queries:      {}\nOutput files: {}\nPages: {}\nBy recent: {}""".format(
			self.queries, self.outfiles, self.pages, self.recent)

	def scrape_all(self):
		"""
		This method scrapes all the Indeed listings for each query provided, 
		using the parameters that this object was initialized with. 
		"""
		# start timing here
		startTime = time.time()
		# recent bool: resolve this before the loop
		if self.recent==True:
			sort_method = "&sort=date"  # recency
		else: 
			sort_method = ""  # relevance (Indeed's default)
		# scrape for each query & output
		for query, outfile in zip(self.queries, self.outfiles):
			query_plus = query.replace(" ", "+")
			results = []
			for searchIndex in range(0, self.pages*10, 10):
				oneURL = "https://www.indeed.com/jobs?q="+query_plus+"&l=United+States"+sort_method+"&start="+str(searchIndex)
				results.append(requests.get(oneURL))
				print("Search: {}/{}".format((searchIndex/10)+1, self.pages))
			# the search results are contained in a "td" with ID = "resultsCol"
			print("Time after requests: "+str(time.time()-startTime))  # DEBUG
			
			justjobs = []; temp = None; soup_jobs = None
			for eachResult in results:
				print("===One result")
				soup_jobs = bs4.BeautifulSoup(eachResult.text, "lxml")  # this is for IDs
				justjobs.extend(soup_jobs.find_all(attrs={"data-jk":True}))
			# Now, each div element has a data-jk. Get data-jk from each one!
			## But first, make sure not to get old job keys: 
				#### TODO: change this to work with SQLite!
			with open(outfile, "r") as file:
				text = file.readlines()  # How does this leave the with's scope?
			currJKs = []
			for eachLine in text[1:]:
				currJKs.append(eachLine[:16])
			currJKstr = str(currJKs)   #### TODO: remove pointless str variable; vvv replace with [-119:]
			print(str(len(text))+" JKs currently stored: ..."+currJKstr[len(currJKstr)-119:]) #DEBUG, 80 width - 26 chars
			# Now, we can get the data-jk's
			jobIDs = []
			for eachJob in justjobs: 
				startindex = str(eachJob).find("data-jk")
				temp0 = str(eachJob)[startindex+9:startindex+25]
				if (temp0 not in currJKs):
					jobIDs.append(temp0)
			# Remove duplicate ID's (Indeed re-shows some across diff. pages)
			jobIDs = list(set(jobIDs))
			# Print the new ones, to track progress
			IDs = " "
			for jobx in jobIDs:
				IDs = IDs + jobx + ", "
			print("\n"+str(len(jobIDs))+" *NEW* JobIDs for "+query+" found:"+IDs[:-2])

			#### SCRAPING
			# Put IDs into URLs, & scrape all of them for keywords
			jobListings = []
			jobDescs = []
			count = 1
			for IDstr in jobIDs:  
				# for each job, first get the page
				jobTemp = []
				jobTemp.append(str(IDstr)) ## 0
				print("This ID: "+str(IDstr)+", pause 1sec"); time.sleep(1)
				jobPage = requests.get("https://www.indeed.com/viewjob?jk="+IDstr)
				pageSoup = bs4.BeautifulSoup(jobPage.text, "lxml")

				# GET TITLE
				# Job title, full tag: <h1 class="icl-u-xs-mb--xs icl-u-xs-mt--none jobsearch-JobInfoHeader-title">Looker Data Analyst (Fully Remote)</h1>
				# now we clean it so only the job title is in position 0
				# the first index is fixed at 76, second one varies based on where "<" starts
				# so we substring for [1:], and .find("<")
				clutteredTitle = str(pageSoup.select('.icl-u-xs-mb--xs'))
				titleEnd = clutteredTitle[76:].find("<")
				jobTemp.append(clutteredTitle[77:76+titleEnd])  ## 1

				# GET JOB AGE
				jobAge = None
				jobFooter = str(pageSoup.select(".jobsearch-JobMetadataFooter"))  # print(jobFooter)  # DEBUG
				agoIndex = jobFooter.find(" ago")  
				justIndex = jobFooter.find("Just posted")
				todayIndex = jobFooter.find("Today")  
				# print("Age index: "+str(agoIndex))  # DEBUG
				# print("Just posted index: "+str(justIndex))  # DEBUG
				# print("Today index: "+str(todayIndex))  # DEBUG
				if(agoIndex != -1 and justIndex==-1 and todayIndex==-1):
					ageTemp = jobFooter[agoIndex-9:agoIndex]
					# print("Age temp: "+ageTemp)  # DEBUG
					dayStart = ageTemp.find(">")
					jobAge = ageTemp[dayStart+1:]
					# print("Job age: "+jobAge)  # DEBUG
				elif(justIndex != -1 and agoIndex==-1 and todayIndex==-1):
					jobAge = "Just posted"
				elif(todayIndex != -1 and justIndex==-1 and agoIndex==-1):
					jobAge = "Today"
				if(agoIndex==-1 and justIndex==-1 and todayIndex==-1):  # If there's no index (external listing, no page!)
					print("External Listing: "+IDstr)  
					jobAge = "External: WIP!"  # UNNEEDED! Indeed does its own webscrape of company sites, external listings will show with "original job" link
				if(jobAge != None and agoIndex==-1 and justIndex==-1 and todayIndex==-1):  
					# if it isn't "Just Posted" or external listing
					print("Something happened... "+IDstr)  # DEBUG
				jobTemp.append(jobAge)  ## 2

				# GET A TIMESTAMP OF THE SCRAPING
				jobTemp.append(time.asctime(time.gmtime()))  ## 3

				# GET A COMPANY'S DETAILS
				jobHeaderSel = pageSoup.select(".jobsearch-JobInfoHeader-subtitle")
				if str(jobHeaderSel) == "[]":
					print("Special case: webpage is different")
					with open("IndeedAnalysts.tsv", "a") as file:
						file.write(IDstr+"\t\t\t"+time.asctime(time.gmtime())+"\t"+query+"\t\n")
					count += 1
					continue
				jobHeaderText = ">"+str(jobHeaderSel[0])+"<"
				jobHeaderSplit = jobHeaderText.split("><")
				# print("========\nJob Header Split: "+str(jobHeaderSplit)+"\n========")
				jobDetails = ""
				for aTag in jobHeaderSplit:
					if(">" in aTag):
						infoStart = aTag.find(">") + 1
						infoEnd = aTag.find("<")
						jobDetails += "|"+aTag[infoStart:infoEnd]
				print(str(count)+"/"+str(len(jobIDs))+" Job Details: "+jobDetails+"\n{}\n========".format(time.asctime(time.gmtime())))
				jobTemp.append(jobDetails)  ## 4

				# GET THE QUERY WE FOUND THIS JOB WITH 
				jobTemp.append(query)  ## 5

				# GET THE JOB DESCRIPTION PAGE (TODO: use select(jobDescription...?))
				page_string = pageSoup.get_text("\n")  #easier printing for debugging
				page_backtick = page_string.replace("\n", "`")
					# putting the whole thing in for now
				jobTextTemp = IDstr+" at "+jobDetails+". Desc.: "+page_backtick  # removed +"\n"; unnecessary now?
				jobTemp.append(jobTextTemp)  ## 6

				# WRITE THE JOB TO THE OUTFILE
				with open(outfile, "a") as file:
					if(jobTemp[0] not in currJKs):  # double checking!
						file.write(jobTemp[0]+"\t"+jobTemp[1]+"\t"+jobTemp[2]+"\t"+jobTemp[3]+"\t"+jobTemp[4]+"\t"+jobTemp[5]+"\t"+jobTemp[6]+"\n")
				
				## End of job; increment & sleep 
				count += 1
				time.sleep(1)
			## End of query; 
			gaptime = random.randint(80,140)
			print("Finished query: {}\nWaiting {} secs...".format(query, gaptime))
			time.sleep(gaptime)
		## End of method
		endTime = time.time()
		totalRuntime = endTime - startTime
		print("BOTTOM of output ========")
		print("Time needed: "+str(totalRuntime)[:6]+" secs")















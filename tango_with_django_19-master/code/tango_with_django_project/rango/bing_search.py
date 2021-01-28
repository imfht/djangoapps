import json

# Add your Microsoft Account Key to a file called bing.key

def read_bing_key():
	"""
	reads the BING API key from a file called 'bing.key'
	returns: a string which is either None, i.e. no key found, or with a key
	remember to put bing.key in your .gitignore file to avoid committing it to the repo.
	"""
	
	# See Python Anti-Patterns - it is an awesome resource to improve your python code
	# Here we using "with" when opening documents
	# http://docs.quantifiedcode.com/python-anti-patterns/maintainability/not_using_with_to_open_files.html
	
	bing_api_key = None
	try:
		with open('bing.key','r') as f:
			bing_api_key = f.readline()
	except:
		raise IOError('bing.key file not found')
		
	return bing_api_key
	

def run_query(search_terms):
	
	bing_api_key = read_bing_key()
	if not bing_api_key:
		raise KeyError('Bing Key Not Found')
	
	# Specify the base url and the service (Bing Search API 2.0)
	root_url = 'https://api.datamarket.azure.com/Bing/Search/'
	service = 'Web'

	# Specify how many results we wish to be returned per page.
	# Offset specifies where in the results list to start from.
	# With results_per_page = 10 and offset = 11, this would start from page 2.
	results_per_page = 10
	offset = 0

	# Wrap quotes around our query terms as required by the Bing API.
	# The query we will then use is stored within variable query.
	query = "'{0}'".format(search_terms)
	
	# Turn the query into an HTML encoded string.
	# We use urllib for this - differences exist between Python 2 and 3.
	# The try/except blocks are used to determine which function call works.
	# Replace this try/except block with the relevant import and query assignment.
	try:
		from urllib import parse  # Python 3 import.
		query = parse.quote(query)
	except ImportError:  # If the import above fails, you are running Python 2.7.x.
		from urllib import quote
		query = quote(query)
	
	# Construct the latter part of our request's URL.
	# Sets the format of the response to JSON and sets other properties.
	search_url = "{0}{1}?$format=json&$top={2}&$skip={3}&Query={4}".format(
		root_url,
		service,
		results_per_page,
		offset,
		query)

	# Setup authentication with the Bing servers.
	# The username MUST be a blank string, and put in your API key!
	username = ''

	#headers = {'Authorization' : 'Basic {0}'.format( b64encode(bing_api_key) )}
	# Create a 'password manager' which handles authentication for us.
	
	try:
		from urllib import request  # Python 3 import.
		password_mgr = request.HTTPPasswordMgrWithDefaultRealm()
	except ImportError:  # Running Python 2.7.x - import urllib2 instead.
		import urllib2
		password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
	
	password_mgr.add_password(None, search_url, username, bing_api_key)

	# Create our results list which we'll populate.
	results = []

	try:
		# Prepare for connecting to Bing's servers.
		try:  # Python 3.5 and 3.6
			handler = request.HTTPBasicAuthHandler(password_mgr)
			opener = request.build_opener(handler)
			request.install_opener(opener)
		except UnboundLocalError:  # Python 2.7.x
			handler = urllib2.HTTPBasicAuthHandler(password_mgr)
			opener = urllib2.build_opener(handler)
			urllib2.install_opener(opener)
	
		# Connect to the server and read the response generated.
		try:  # Python 3.5 or 3.6
			response = request.urlopen(search_url).read()
			response = response.decode('utf-8')
		except UnboundLocalError:  # Python 2.7.x
			response = urllib2.urlopen(search_url).read()
	
		# Convert the string response to a Python dictionary object.
		json_response = json.loads(response)
	
		# Loop through each page returned, populating out results list.
		for result in json_response['d']['results']:
			results.append({
				'title': result['Title'],
				'link': result['Url'],
				'summary': result['Description']})
	except:
		print("Error when querying the Bing API")
	
	# Return the list of results to the calling function.
	return results
	

def main():
	print("Enter a query ")
	query = raw_input()
	results = run_query(query)
	for result in results:
		print(result['title'])
		print('-'*len(result['title']))
		print(result['summary'])
		print(result['link'])
		print()
		
	
if __name__ == '__main__':
	main()
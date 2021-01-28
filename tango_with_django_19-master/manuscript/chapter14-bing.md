# Bing Search {#chapter-bing}
Now that our Rango application is looking good and most of the core functionality has been implemented, we can move onto some of the more advanced functionality. In this chapter, we will connect Rango up to Bing's Search API so that users can also search for pages, rather than just browse categories. Before we can do so, we need to set up an account to use Bing's Search API and write a wrapper to call Bing's Web search functionality.

## The Bing Search API
The Bing Search API provides you with the ability to embed search results from the Bing search engine within your own applications. Through a straightforward interface, you can request results from Bing's servers to be returned in either XML or JSON. The data returned can then be interpreted by a XML or JSON parser, with the results then rendered as part of a template within your application.

Although the Bing API can handle requests for different kinds of content, we'll be focusing on web search only for this tutorial - as well as handling JSON responses. To use the Bing Search API, you will need to sign up for an *API key*. The key currently provides subscribers with access to 5000 queries per month, which should be more than enough for our purposes.

I> ### Application Programming Interface (API)
I> An [Application Programming Interface](http://en.wikipedia.org/wiki/Application_programming_interface) specifies how software components should interact with one another. In the context of web applications, an API is considered as a set of HTTP requests along with a definition of the structures of response messages that each request can return. Any meaningful service that can be offered over the Internet can have its own API - we aren't limited to web search. For more information on web APIs, [Luis Rei provides an excellent tutorial on APIs](http://blog.luisrei.com/articles/rest.html).


### Registering for a Bing API Key
To register for a Bing API key, you must first register for a free Microsoft account. The account provides you with access to a wide range of Microsoft services. If you already have a Hotmail account, you already have one! Otherwise, you can go online and create a free account with Microsoft at [`https://account.windowsazure.com`](https://account.windowsazure.com).

When your account has been created, go to the [Windows Azure Marketplace Bing Search API page](https://datamarket.azure.com/dataset/5BA839F1-12CE-4CCE-BF57-A49D98D29A44) and login.

<!-->. At the top of the screen, you may first need to click the *Sign In* button - if you have already signed into your Microsoft account, you won't need to provide your account details again. If the text says *Sign Out*, you're already logged in.
-->
On the right hand side of the page you should see a list of transactions per month. At the bottom of the list is *5,000 Transactions/month*. Click the sign up button to the right - subscribe for the free service.

{id="fig-bing-search"}
![The Bing Search API services - sign up for the 5,000 transactions/month for free.
](images/ch14-bing-search-api.png)

<!--> Once you've read the *Publisher Offer Terms*, agreed and click *Sign Up* to continue. You will  then be presented with a page confirming that you have successfully signed up.-->

Once you've signed up, click the *Data* link at the top of the page. From there, you should be presented with a list of data sources available through the Windows Azure Marketplace. At the top of the list should be *Bing Search API* - it should also say that you are *subscribed* to the data source. Click the *use* link associated with the Bing Search API located on the right of the page. 


{id="fig-bing-explore"}
![The Account Information Page. In this screenshot, the *Primary Account Key* is deliberately obscured. You should make sure you keep your key secret, too!
](images/ch14-bing-account.png)

	
This page allows you to try out the Bing Search API by filling out the boxes to the left. For example, the *Query* box allows you to specify a query to send to the API. Ensure that at the bottom of the screen you select *Web* for web search results only. Note the URL provided in the blue box at the top of the page changes as you alter the settings within the webpage. Take a note of the Web search URL. We'll be using part of this URL within our code later on. The following example is a URL that we'd need to construct in order to perform a web search using the query *rango*.

{lang="text",linenos=off}
	https://api.datamarket.azure.com/Bing/Search/v1/Web?Query=%27rango%27


Assuming this all works take a copy of your API key. We will need this when we make requests as part of the authentication process. To obtain your key, locate the text *Primary Account Key* at the top of the page and click the *Show* link next to it. Your key will then be shown.   We'll be using it later, so take a note of it - and keep it safe!  The Bing API Service Explorer keeps a tab of how many queries you have left of your monthly quota. So if someone obtains your key, they'll be able to use your quota.  

## Adding Search Functionality
Below we have provided the code that we can use to issue queries to the Bing search service. Create a file called `rango/bing_search.py` and import the following code. You'll also need to take a copy of your Bing Search API key - we'll show you what to do with that shortly.

I> ### Python 2 and 3 `import` Differences
I> 
I> In [Python 3 they refactored the `urllib` package](http://stackoverflow.com/a/2792652), so the way that we connect and work with external web resources has changed from Python 2.7+. Below we have two versions of the code, one for Python 2.7+ and one for Python 3+.
I> Make sure you use the correct one.


### Python 2 Version

{lang="python",linenos=on}
	import json
	import urllib, urllib2  # Py2.7.x
	
	# Add your Microsoft Account Key to a file called bing.key
	
	def read_bing_key():
	    """
	    Reads the BING API key from a file called 'bing.key'.
	    returns: a string which is either None, i.e. no key found, or with a key.
	    Remember: put bing.key in your .gitignore file to avoid committing it!
	    """
	    # See Python Anti-Patterns - it's an awesome resource!
	    # Here we are using "with" when opening documents.
	    # http://docs.quantifiedcode.com/python-anti-patterns/maintainability/
	    bing_api_key = None
	    
	    try:
	        with open('bing.key','r') as f:
	            bing_api_key = f.readline()
	    except:
	        raise IOError('bing.key file not found')
	        
	    return bing_api_key
	    
	def run_query(search_terms):
	    """
	    Given a string containing search terms (query),
	    returns a list of results from the Bing search engine.
	    """
	    bing_api_key = read_bing_key()
	    
	    if not bing_api_key:
	        raise KeyError("Bing Key Not Found")
	    
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
	    
	    # Turn the query into an HTML encoded string, using urllib.
	    # Use the line relevant to your version of Python.
	    query = urllib.quote(query)  # Py2.7.x
	    
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
	    
	    # Setup a password manager to help authenticate our request.
	    # Watch out for the differences between Python 2 and 3!
	    password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()  # Py2.7.x
	    
	    # The below line will work for both Python versions.
	    password_mgr.add_password(None, search_url, username, bing_api_key)
	    
	    # Create our results list which we'll populate.
	    results = []
	    
	    try:
	        # Prepare for connecting to Bing's servers.
	        # Python 2.7.x import (three lines)
	        handler = urllib2.HTTPBasicAuthHandler(password_mgr)  # Py2.7.x
	        opener = urllib2.build_opener(handler)  # Py2.7.x
	        urllib2.install_opener(opener)  # Py2.7.x
	        	        
	        # Connect to the server and read the response generated.
	        # Once again, watch for differences between Python 2.7.x and 3.
	        response = urllib2.urlopen(search_url).read()  # Py2.7.x
	        
	        # Convert the string response to a Python dictionary object.
	        json_response = json.loads(response)
	        
	        # Loop through each page returned, populating out results list.
	        for result in json_response['d']['results']:
	            results.append({'title': result['Title'],
	                            'link': result['Url'],
	                            'summary': result['Description']})
	    except:
	        print("Error when querying the Bing API")
	    
	    # Return the list of results to the calling function.
	    return results
		
{pagebreak}
		
### Python 3 Version

{lang="python",linenos=on}
	import json
	import urllib  # Py3
	
	# Add your Microsoft Account Key to a file called bing.key
	
	def read_bing_key():
	    """
	    Reads the BING API key from a file called 'bing.key'.
	    returns: a string which is either None, i.e. no key found, or with a key.
	    Remember: put bing.key in your .gitignore file to avoid committing it!
	    """
	    # See Python Anti-Patterns - it's an awesome resource!
	    # Here we are using "with" when opening documents.
	    # http://docs.quantifiedcode.com/python-anti-patterns/maintainability/
	    bing_api_key = None
	    
	    try:
	        with open('bing.key','r') as f:
	            bing_api_key = f.readline()
	    except:
	        raise IOError('bing.key file not found')
	        
	    return bing_api_key
	    
	def run_query(search_terms):
	    """
	    Given a string containing search terms (query),
	    returns a list of results from the Bing search engine.
	    """
	    bing_api_key = read_bing_key()
	    
	    if not bing_api_key:
	        raise KeyError("Bing Key Not Found")
	    
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
	    
	    # Turn the query into an HTML encoded string, using urllib.
	    # Use the line relevant to your version of Python.
	    query = urllib.parse.quote(query)  # Py3
	    
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
	    
	    # Setup a password manager to help authenticate our request.
	    # Watch out for the differences between Python 2 and 3!
	    password_mgr = urllib.request.HTTPPasswordMgrWithDefaultRealm()  # Py3
	    
	    # The below line will work for both Python versions.
	    password_mgr.add_password(None, search_url, username, bing_api_key)
	    
	    # Create our results list which we'll populate.
	    results = []
	    
	    try:
	        # Prepare for connecting to Bing's servers.	        
	        # Python 3 import (three lines)
	        handler = urllib.request.HTTPBasicAuthHandler(password_mgr)  # Py3
	        opener = urllib.request.build_opener(handler)  # Py3
	        urllib.request.install_opener(opener)  # Py3
	        
	        # Connect to the server and read the response generated.
	        response = urllib.request.urlopen(search_url).read()  # Py3
	        response = response.decode('utf-8')  # Py3
	        
	        # Convert the string response to a Python dictionary object.
	        json_response = json.loads(response)
	        
	        # Loop through each page returned, populating out results list.
	        for result in json_response['d']['results']:
	            results.append({'title': result['Title'],
	                            'link': result['Url'],
	                            'summary': result['Description']})
	    except:
	        print("Error when querying the Bing API")
	    
	    # Return the list of results to the calling function.
	    return results


In the module(s) above, we have implemented two functions: one to retrieve your Bing API key from a local file, and another to issue a query to the Bing search engine. Below, we discuss how both of the functions work.

### `read_bing_key()` - Reading the Bing Key {#section-bing-adding-key}
The `read_bing_key()` function reads in your key from a file called `bing.key`, located in your Django project's root directory (i.e. `<workspace>/tango_with_django/`). We have created this function because if you are putting your code into a public repository on GitHub for example, you should take some precautions to avoid sharing your API Key publicly. 

From the Azure website, take a copy of your *Account key* and save it into `<workspace>/tango_with_django/bing.key`. The key should be the only contents of the file - nothing else should exist within it. This file should be kept from being committed to your GitHub repository. To make sure that you do not accidentally commit it, update your repository's `.gitignore` file to exclude any files with a `.key` extension, by adding the line `*.key`. This way, your key file will only be stored locally and you will not end up with someone using your query quota.
	
T> ### Keys and Rings
T>
T> Keep them secret, keep them safe!


### `run_query()` - Executing the Query
The `run_query()` function takes a query as a string, and returns the top ten results from Bing in a list that contains a dictionary of the result items (including the `title`, a `link`, and a `summary`). If you are interested, the inline commentary in the code snippet above describes how the request is created and then issued to the Bing API - check it out to further your understanding.

To summarise though, the logic of the `run_query()` function can be broadly split into six main tasks.

* First, the function prepares for connecting to Bing by preparing the URL that we'll be requesting.
* The function then prepares authentication, making use of your Bing API key. This is obtained by calling `read_bing_key()`, which in turn pulls your Account key from the `bing.key` file you created earlier.
* We then connect to the Bing API through the function call `urllib2.urlopen()` (for Python 2.7.x), or `urllib.request.urlopen()` (for Python 3). The results from the server are read and saved as a string.
* This string is then parsed into a Python dictionary object using the `json` Python package.
* We loop through each of the returned results, populating a `results` dictionary. For each result, we take the `title` of the page, the `link` or URL and a short `summary` of each returned result.
* The list of dictionaries is then returned by the function.

Notice that results are passed from Bing's servers as JSON. This is because we explicitly specify to use JSON in our initial request - check out the `format` key/value pair in the `search_url` variable that we define. 

Also, note that if an error occurs when attempting to connect to Bing's servers, the error is printed to the terminal via the `print` statement within the `except` block.

I> ###Bing it on!
I> There are many different parameters that the Bing Search API can handle which we don't cover here. 
I> If you want to know more about the API check out the [Bing Search API Migration Guide and FAQ](http://datamarket.azure.com/dataset/bing/search).

X> ### Exercises
X> Extend your `bing_search.py` module so that it can be run independently, i.e. running `python bing_search.py` from your terminal or Command Prompt. Specifically, you should implement functionality that:
X> 
X> - prompts the the user to enter a query, i.e. use `raw_input()`; and
X> - issues the query via `run_query()`, and prints the results.

T> ### Hint
T> Add the following code, so that when you run `python bing_search.py` it calls the `main()` function:
T> 	
T> {lang="python",linenos=off}
T>		def main():
T>		    #insert your code here
T>		
T>		if __name__ == '__main__':
T>		    main()
T>
T> When you run the module explicitly via `python bing_search.py`, the `bing_search` module is treated as the `__main__` module, and thus triggers `main()`. However, when the module is imported by another module, then `__name__` will not equal `__main__`, and thus the `main()` function not be called. This way you can `import` it with your application without having to call `main()`.

## Putting Search into Rango
Now that we have successfully implemented the search functionality module, we need to integrate it into our Rango app. There are two main steps that we need to complete for this to work.

-  We must first create a `search.html` template that extends from our `base.html` template. The `search.html` template will include a HTML `<form>` to capture the user's query as well as template code to present any results.
- We then create a view to handle the rendering of the `search.html` template for us, as well as calling the `run_query()` function we defined above.

### Adding a Search Template
Let's first create a template called, `rango/search.html`. Add the following HTML markup, Django template code, and Bootstrap classes.

{lang="html",linenos=on}
	{% extends 'rango/base.html' %}
	{% load staticfiles %}
	
	{% block title %} Search {% endblock %}
	
	{% block body_block %}
	<div>
	    <h1>Search with Rango</h1>
	    <br/>
	    <form class="form-inline" id="user_form" 
	          method="post" action="{% url 'search' %}">
	        {% csrf_token %}
	        <div class="form-group">
	            <input class="form-control" type="text" size="50" 
	                   name="query" value="" id="query" />
	        </div>
	        <button class="btn btn-primary" type="submit" name="submit"
	                value="Search">Search</button>
	    </form>
	    
	    <div>
	        {% if result_list %}
	        <h3>Results</h3>
	        <!-- Display search results in an ordered list -->
	        <div class="list-group">
	        {% for result in result_list %}
	            <div class="list-group-item">
	                <h4 class="list-group-item-heading">
	                    <a href="{{ result.link }}">{{ result.title }}</a>
	                    </h4>
	                    <p class="list-group-item-text">{{ result.summary }}</p>
	            </div>
	        {% endfor %}
	        </div>
	        {% endif %}
	    </div>
	</div>	
	{% endblock %}

The template code above performs two key tasks.

- In all scenarios, the template presents a search box and a search buttons within a HTML `<form>` for users to enter and submit their search queries.
- If a `results_list` object is passed to the template's context when being rendered, the template then iterates through the object displaying the results contained within.
	
To style the HTML, we have made use of Bootstrap [panels](http://getbootstrap.com/components/#panels), [list groups](http://getbootstrap.com/components/#list-group), and [inline forms](http://getbootstrap.com/css/#forms-inline).

In the view code, in the next subsection, we will only pass through the results to the template, when the user issues a query. Initially, there will be not results to show.

### Adding the View
With our search template added, we can then add the view that prompts the rendering of our template. Add the following `search()` view to Rango's `views.py` module.

{lang="python",linenos=off}	
	def search(request):
	    result_list = []
	    
	    if request.method == 'POST':
	        query = request.POST['query'].strip()
	        if query:
	            # Run our Bing function to get the results list!
	            result_list = run_query(query)
	    
	    return render(request, 'rango/search.html', {'result_list': result_list})
	
By now, the code should be pretty self explanatory to you. The only major addition is the calling of the `run_query()` function we defined earlier in this chapter. To call it, we are required to also import the `bing_search.py` module, too. Ensure that before you run the script that you add the following `import` statement at the top of the `views.py` module.

{lang="python",linenos=off}
	from rango.bing_search import run_query

You'll also need to ensure you do the following, too.

- Add a mapping between your `search()` view and the `/rango/search/` URL calling it `name='search'` by adding in `url(r'search/$', views.search, name='search'),` to `rango/urls.py`.
- Also, update the `base.html` navigation bar to include a link to the search page. Remember to use the `url` template tag to reference the link.
- You will need a copy of the `bing.key` in your project's root directory (`<workspace>/tango_with_django_project`, alongside `manage.py`).

Once you have put in the URL mapping and added a link to the search page, you should now be able issue queries to the Bing Search API and have the results shown within the Rango app (as shown in the figure below).

{id="fig-bing-python-search"}
![Searching for "Python for Noobs".](images/ch14-bing-python-search.png)

X> ### Additional Exercise
X>
X> You may notice that when you issue a query, the query disappears when the results are shown. This is not very user friendly. Update the view and template so that the user's query is displayed within the search box.
X>
X> Within the view, you will need to put the `query` into the context dictionary. Within the template, you will need to show the query text in the search box.
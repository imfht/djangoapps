# Webhose Search {#chapter-searchapi}
Now that our Rango app is looking good and most of the core functionality has been implemented, we can move onto some of the more advanced functionality. In this chapter, we will connect Rango up to the *Webhose API* so that users can also search for pages, rather than simply browse categories. Before we do so, we need to set up an account with Webhose, and write a [wrapper](https://en.wikipedia.org/wiki/Adapter_pattern) to query and obtain results from their API.

## The Webhose API
The Webhose API provides you with the ability to programmatically query [*Webhose*](https://webhose.io/), an online service that collates information from a variety of online sources in real-time. Through a straightforward interface, you can request results for a query in JSON. The returned data can then be interpreted by a JSON parser, with the results then rendered as part of a template within you app.

Although Webhose allows you to obtain results for information that has been recently [crawled](https://en.wikipedia.org/wiki/Web_crawler), we'll be focusing on returning content ranked by its *relevancy* to the query that a user of Rango provides. To use the Webhose API, you'll need an *API key*. The key provides you with 1,000 free queries per month -- more than enough for our purposes.

I> ### What is an *Application Programming Interface (API)*?
I> An [Application Programming Interface](http://en.wikipedia.org/wiki/Application_programming_interface) specifies how software components should interact with one another. In the context of web applications, an API is considered as a set of HTTP requests along with a definition of the structures of response messages that each request can return. Any meaningful service that can be offered over the Internet can have its own API - we aren't limited to web search. For more information on web APIs, [Luis Rei provides an excellent tutorial on APIs](http://blog.luisrei.com/articles/rest.html).

### Registering for a Webhose API Key
To obtain a Webhose API key, you must first register for a free Webhose account. Head over to [`https://www.webhose.io`](https://www.webhose.io) in your Web browser, and sign up by clicking *'Use it for free'* at the top right of the page. You don't need to provide a company name -- and in company e-mail, simply provide a valid e-mail address.

Once you have created your account, you'll be taken to the Webhose *Dashboard*, [as can be seen below](#fig-webhose-dashboard). From the dashboard, you can see a count of how many queries you have issued over the past month, and how many free queries you have remaining. There's also a neat little graph which demonstrates the rate at which you issue queries to Webhose over time. Scroll down the page, and you'll find a section called *Active API Key*. **Take a note of the key shown here by copying it into a blank text file -- you'll be needing this later on.** This is your unique key, that when sent with a request to the Webhose API, will identify you to their servers.

{id="fig-webhose-dashboard"}
![The Webhose dashboard, showing where the API key is displayed on the page. You'll most likely have to scroll down to see it. In the screenshot, the API key has been obscured. Keep your key safe and secure!
](images/ch14-webhose-dashboard.png)

Once you have your API key, scroll back up to the top of the Webhose dashboard, and click the [*Get live data* button](https://webhose.io/api), which is in blue. You'll then be taken to the API page, which allows you to play around with the Webhose API interface. Try it out!

1. In the box under *Return posts containing the following keywords*, enter a query.
2. In the *Sort by* dropdown box, choose *Relevancy*.
3. You can then choose a value for *Return posts crawled since*, but leaving it at the 3 day default should be fine.
3. Click *Test the Query*, and you'll then be presented with a series of results to the query you entered. [The screenshot below shows example output for the query *Glasgow*.](#fig-webhose-query)

{id="fig-webhose-query"}
![A sample response from the Webhose API for the query *Glasgow*. Shown is the *Visual Glimpse*; you can also see the raw JSON response from the server by clicking the *JSON* tab. 
](images/ch14-webhose-query.png)

Have a look at what you get back, and also have a look at the raw JSON response that is returned by the Webhose API. You can do this by clicking on the *JSON* tab. You can try copying and pasting the JSON response in to an online [JSON pretty printer](http://jsonprettyprint.com/) to see how it's structured if you want. Close the response by clicking the *X* to the right of the *Output Stream* title, and you'll be returned the API page. You can now scroll down to find the *Integration Examples* section. Make sure the *Endpoint* tab is selected, and have a look at the URL that you are shown. This is the URL that your Rango app will be communicating with to obtain search results -- or, in other words, the *endpoint URL*. We'll be making use of it later. An example of the Webhose API endpoint URL -- for a given configuration, with the API key and query redacted -- is shown below.

`http://webhose.io/search ? token=<KEY>&format=json&q=<QUERY>&sort=relevancy`

The URL can essentially be split into two parts - the *base URL* on the left of the question mark, and the querystring to the right. Consider the base URL as the path to the API, and the querystring a series of key and value pairings (e.g. `format` for a key, `json` for a value) that tell the API exactly what you want to get from it. You'll see in the code sample shortly that we take the same process of splitting the URL into a base URL before combining the querystring together to get the complete request URL.

## Adding Search Functionality
Now you've got your Webhose API key, you're ready to implement functionality in Python that issues queries to the Webhose API. Create a new module (file) in the `rango` app directory called `webhose_search.py`, and add the following code -- picking the correct one for your Python version. As mentioned earlier in the book, it's better you go through and type the code out -- you'll be thinking about how it works as you type (and understanding what's going on), rather than blindly copying and pasting.

I> ### Differences between Python 2 and 3
I> In [Python 3, the `urllib` package was refactored](http://stackoverflow.com/a/2792652), so the way that we connect and work with external web resources has changed from Python 2.7+. Below we have two versions of the code, one for Python 2.7+ and one for Python 3+. Make sure you use the correct one for your environment.

### Python 2 Version
{lang="python",linenos=on}
	import json
	import urllib
	import urllib2
	
	def read_webhose_key():
	    """
	    Reads the Webhose API key from a file called 'search.key'.
	    Returns either None (no key found), or a string representing the key.
	    Remember: put search.key in your .gitignore file to avoid committing it!
	    """
	    # See Python Anti-Patterns - it's an awesome resource!
	    # Here we are using "with" when opening files.
	    # http://docs.quantifiedcode.com/python-anti-patterns/maintainability/
	    webhose_api_key = None
	
	    try:
	        with open('search.key', 'r') as f:
	            webhose_api_key = f.readline().strip()
	    except:
	        raise IOError('search.key file not found')
	
	    return webhose_api_key
	
	def run_query(search_terms, size=10):
	    """
	    Given a string containing search terms (query), and a number of results to
	    return (default of 10), returns a list of results from the Webhose API,
	    with each result consisting of a title, link and summary.
	    """
	    webhose_api_key = read_webhose_key()
	
	    if not webhose_api_key:
	        raise KeyError('Webhose key not found')
	
	    # What's the base URL for the Webhose API?
	    root_url = 'http://webhose.io/search'
	
	    # Format the query string - escape special characters.
	    query_string = urllib.quote(search_terms)
	
	    # Use string formatting to construct the complete API URL.
	    # search_url is a string split over multiple lines.
	    search_url = ('{root_url}?token={key}&format=json&q={query}'
	                  '&sort=relevancy&size={size}').format(
	                    root_url=root_url,
	                    key=webhose_api_key,
	                    query=query_string,
	                    size=size)
	
	    results = []
	
	    try:
	        # Connect to the Webhose API, and convert the response to a
	        # Python dictionary.
	        response = urllib2.urlopen(search_url).read()
	        json_response = json.loads(response)
	
	        # Loop through the posts, appending each to the results list as
	        # a dictionary. We restrict the summary to the first 200
	        # characters, as summary responses from Webhose can be long!
	        for post in json_response['posts']:
	            results.append({'title': post['title'],
	                            'link': post['url'],
	                            'summary': post['text'][:200]})
	    except:
	        print("Error when querying the Webhose API")
	
	    # Return the list of results to the calling function.
	    return results

### Python 3 Version
{lang="python",linenos=on}
	import json
	import urllib.parse  # Py3
	import urllib.request  # Py3
	
	def read_webhose_key():
	    """
	    Reads the Webhose API key from a file called 'search.key'.
	    Returns either None (no key found), or a string representing the key.
	    Remember: put search.key in your .gitignore file to avoid committing it!
	    """
	    # See Python Anti-Patterns - it's an awesome resource!
	    # Here we are using "with" when opening files.
	    # http://docs.quantifiedcode.com/python-anti-patterns/maintainability/
	    webhose_api_key = None
	
	    try:
	        with open('search.key', 'r') as f:
	            webhose_api_key = f.readline().strip()
	    except:
	        raise IOError('search.key file not found')
	
	    return webhose_api_key
	
	def run_query(search_terms, size=10):
	    """
	    Given a string containing search terms (query), and a number of results to
	    return (default of 10), returns a list of results from the Webhose API,
	    with each result consisting of a title, link and summary.
	    """
	    webhose_api_key = read_webhose_key()
	
	    if not webhose_api_key:
	        raise KeyError('Webhose key not found')
	
	    # What's the base URL for the Webhose API?
	    root_url = 'http://webhose.io/search'
	
	    # Format the query string - escape special characters.
	    query_string = urllib.parse.quote(search_terms)  # Py3
	
	    # Use string formatting to construct the complete API URL.
	    # search_url is a string split over multiple lines.
	    search_url = ('{root_url}?token={key}&format=json&q={query}'
	                  '&sort=relevancy&size={size}').format(
	                    root_url=root_url,
	                    key=webhose_api_key,
	                    query=query_string,
	                    size=size)
	
	    results = []
	
	    try:
	        # Connect to the Webhose API, and convert the response to a
	        # Python dictionary.
	        response = urllib.request.urlopen(search_url).read().decode('utf-8')
	        json_response = json.loads(response)
	    
	        # Loop through the posts, appending each to the results list as
	        # a dictionary. We restrict the summary to the first 200
	        # characters, as summary responses from Webhose can be long!
	        for post in json_response['posts']:
	            results.append({'title': post['title'],
	                            'link': post['url'],
	                            'summary': post['text'][:200]})
	    except:
	        print("Error when querying the Webhose API")
	
	    # Return the list of results to the calling function.
	    return results

In the code samples above, we have implemented two functions: one to retrieve your Webhose API key from a local file (through function `read_webhose_key()`), and another to issue a query to the Webhose API and return results (`run_query()`). Below, we discuss how both of the functions work.

### `read_webhose_key()` -- Reading the Webhose API Key {#section-searchapi-adding-key}
The `read_webhose_key()` function reads in your Webhose API key from a file called `search.key`. This file should be located in your Django project's root directory, **not Rango's directory** (i.e. `<workspace>/tango_with_django_project/`). We have created this function as it allows you to separate your private API key from the code that utilises it. This is advantageous in scenarios where code is shared publicly (i.e. on GitHub) -- you don't want people using your API key!

You should create the `search.key` file now. Take the Webhose API key you copied earlier, and save it into the file `<workspace>/tango_with_django_project/search.key`. The key should be the only contents of the file -- nothing else should exist within it. Avoid committing the file to your GitHub repository by updating your repository's `.gitignore` file to exclude any files with a `.key` extension by adding the line `*.key`. This way, your key is only stored locally, and cannot be committed to your remote Git repository by accident.

T> ### Keys
T> Keep them secret, keep them safe!
T>
T> Don't let anyone use your code. If they misuse it, you could be banned from the service to which it corresponds. Or worse, end up having to pay for the services you did not use.

### `run_query()` -- Executing the Query
The `run_query()` function takes two parameters: `search_terms`, a string representing a user's query; and `size`, an [optional parameter](http://www.diveintopython.net/power_of_introspection/optional_arguments.html), set to a default of `10`. This second parameter allows us to control the number of results to return from the Webhose API. Given these parameters, the function then communicates with the Webhose API, and returns a series of Python dictionaries within a list, with each dictionary representing an individual result -- consisting of a result `title`, `link` and `summary`. The inline commentary in the function definitions above (for both Python 2.7.x and Python 3) explain what's happening at each stage -- check out the commentary further to increase your understanding of what is going on.

To summarise, the logic of `run_query()` can be broadly split into seven main tasks, which are explained below.

* First, the function obtains the Webhose API key by calling the `read_webhose_key()` function.
* The function then correctly formats the query string to be sent to the API. This is done by [*URL encoding*](https://en.wikipedia.org/wiki/Percent-encoding) the string, converting special characters such as spaces to a format that can be understood by Web servers and browsers. As an example, the space character `' '` is converted to `%20`.
* The complete URL for the Webhose API call is then constructed by concatenating the URL encoded `search_terms` string and `size` parameters -- as well as your Webhose API key -- together into a series of [querystring](https://en.wikipedia.org/wiki/Query_string) arguments as dictated by the [Webhose API documentation](https://webhose.io/documentation).
* We then connect to the Webhose API using the Python `urllib2` (for Python 2.7.x) or `urllib` modules. The string response from the server is then saved in the variable `response`.
* This response is then converted to a Python dictionary object using the Python `json` library.
* The dictionary is then iterated over, with each result returned from the Webhose API saved to the `results` list as a dictionary, consisting of `title`, `link` and `summary` key/value pairings.
* The `results` list is then returned by the function.

I> ### Exploring API Options
I> When starting off with a new API, it's always a good idea to explore the provided documentation to see what options you can play with. We recommend exploring the [Webhose API documentation](https://webhose.io/documentation) and play around with some of the options that you can vary.

X> ### Exercises
X> Extend your `webhose_search.py` module so that it can be run independently. By this, we mean running `python webhose_search.py` from your terminal or Command Prompt, without running Django's development server. Specifically, you should implement functionality that:
X> 
X> - prompts the user to enter a query, i.e. use `raw_input()`; and
X> - issues the query via `run_query()`, and prints the results.
X>
X> For each result, you should display the corresponding `title` and `summary`, with a line break between each result.
X>
X> You'll also need to modify the `read_webhose_key()` function so that the `search.key` file can be found from the `rango` directory in which `webhose_search.py` is launched. When running the Django development server, Python would expect to find `search.key` in the directory you launched `manage.py`. When you run `webhose_search.py` in the `rango` directory, you'll need to look one directory up. How could you modify the `read_webhose_key()` function to work both ways?
X>
X> If you are developing Rango on a Windows computer with Python 2.7.x, you'll need to encode the output of each `print` statement using the `str` `encode()` function with `utf-8`. For example, to display the `title` of a result, you would use `print(result['title']).encode('utf-8')`. This is due to the way that Python calls underlying Windows functions to output content. If you receive a `UnicodeEncodeError`, this may be your solution. Python 3 should be unaffected by this issue.

T> ### Hint
T> You've already done this in your [population script](#section-models-population) for Rango! Try following the [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html#Main) to make everything look the part by adding a `main()` function, and calling whatever you need to from there. You should also make use of the following line -- if you aren't sure what this line means, [have a look online for an answer](http://stackoverflow.com/questions/419163/what-does-if-name-main-do), or refer [back to the section of the tutorial discussing the population script](#section-models-population).
T> 	
T> {lang="python",linenos=off}
T>		if __name__ == '__main__':
T>		    main()
T>
T> Using this line will ensure that you can run your module independently of anything else -- yet still include the module within another Python program (i.e. your Django project) and not have code automatically executed when you `import`.
T>
T> To modify your `read_webhose_key()` function, there's a few things you could try. The easiest approach would be to make use of the `os.path.isfile()` function to check if `search.key` is a file that exists in the current directory. If it doesn't exist, then you could assume that the key can be found in `../search.key` -- [one directory up (`..`)](http://teaching.idallen.com/cst8207/12f/notes/160_pathnames.html) from where your script is running. To access the `isfile()` function, you'll need to make sure the `os` module is imported at the top of `webhose_search.py`.

## Putting Webhose Search into Rango
Now that we have successfully implemented the search functionality module `webhose_search.py`, we need to integrate it into our Rango app. There are three main steps that we need to complete for this to work.

1. We must first create a `search.html` template that extends from Rango's `base.html` template. The `search.html` template will include a HTML `<form>` to capture the user's query, as well as template code to present any results.
2. We then create a Django view to handle the rendering of the `search.html` template for us, as well as calling the `run_query()` function we defined earlier in this chapter. W then allow users to access the new view by mapping it to a new URL within Rango's `urls.py` module.

### Adding a Search Template
Let's first start at the beginning, and create a new template called `search.html`. Place it within the `rango` directory of your project's `templates` directory. Add the following HTML markup and Django template code.

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

* The template presents a search box and *Search* button within a HTML `<form>` for users to enter and submit their queries.
* If a `results_list` object is passed to the template's context when rendering, the template then iterates through the `results_list` object, rendering the results contained within. The template expects that each result consists of a `title`, `link` and `summary` -- consistent with what is returned from the `run_query()` function defined earlier in this chapter.

To style the page that is rendered, we have made use of Bootstrap [panels](http://getbootstrap.com/components/#panels), [list groups](http://getbootstrap.com/components/#list-group), and [inline forms](http://getbootstrap.com/css/#forms-inline).

The Django view in the following subsection will only pass through results to the template above in a context variable called `results_list` when the user issues a query. Initially, no results will be available to show -- so `results_list` will not be provided to the template, and thus, no results will be rendered.

### Adding the View
With the new template added, we can then add the view that prompts the rendering of our template. Add the following `search()` view to Rango's `views.py` module.

{lang="python",linenos=off}	
	def search(request):
	    result_list = []
	    
	    if request.method == 'POST':
	        query = request.POST['query'].strip()
	        if query:
	            # Run our Webhose search function to get the results list!
	            result_list = run_query(query)
	    
	    return render(request, 'rango/search.html', {'result_list': result_list})

By now, the code above should be pretty self explanatory to you. The only major addition here that you wouldn't have done so far is the calling of the `run_query()` function we defined earlier in this chapter. To call it, we are also required to `import` the `webhose_search.py` module, too. Ensure that before you run the Django development server that you add the following `import` statement at the top of Rango's `views.py` module.

{lang="python",linenos=off}
	from rango.webhose_search import run_query

We then need to create the URL mapping between a URL and the `search()` view, as well as make it possible for users to navigate to the search page through Rango's navigation bars.

* Add the URL mapping between the `search()` view and the URL `/rango/search/`, with `name='search'`. This can be done by adding the line `url(r'search/$', views.search, name='search')` to Rango's `urls.py` module.
* Update the `base.html` navigation bar to include a link to the search page. Remember to use the `url` template tag to reference the link, rather than hard coding it into the template.
* Finally, ensure that the `search.key` file is created -- with your Webhose API key contained within it -- and it is located in your Django project's root directory (i.e. `<workspace>/tango_with_django_project/`, alongside `manage.py`).

Once you have put the URL mapping together and added a link to the search page, you should now be able to issue queries to the Webhose API, with results now showing in the Rango app -- as shown [in the figure below](#fig-bing-python-search).

{id="fig-bing-python-search"}
![Searching for "Python for Noobs".](images/ch14-bing-python-search.png)

X> ### Additional Exercise
X>
X> You may notice that when you issue a query, the query disappears when the results are shown. This is not very user friendly. Update the `search()` view and `search.html` template so that the user's query is displayed within the search box.
X>
X> Within the view, you will need to put the `query` into the context dictionary. Within the template, you will need to show the query text in the search box.

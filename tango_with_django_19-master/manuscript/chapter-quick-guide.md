# Cheat Sheet - Quick Command Reference Guide

A quick guide to common Django Commands, Functions and Methods.

## Start the Project/Application

### Create the Project
To setup and create a project called `<project_name>`:

    $ django-admin.py startproject <project_name>

###Create an Application

    $ python manage.py startapp <app_name>

Remember to add the application name `<app_name>` to `INSTALLED_APPS` in `settings.py`.


## Run Server
To kick off the server with port `<port>`:

    $ python manage.py runserver <port>

if `<port>` is not specified, defaults to 8000.


## Database Commands


### Setup database
The simplest database setup is to use an  SQL Lite 3 database (which is a native database). In `settings.py`, set the `DATABASES` dictionary up as follows:


```
DATABASES = {
     'default': {
         'ENGINE': 'django.db.backends.sqlite3',
         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
     }
 }
```
Ensure that `BASE_DIR` is defined and `os` is imported, i.e:

```
import os
BASE_DIR = os.getcwd()
```

### Perform Migrations
To perform the migrations:

    $ python manage.py migrate

Note: you need to run migrate before running the server for the first time for Django to setup a series of tables.

### Create a superuser
Create a superuser, if you have not done so already

    $ python manage.py createsuperuser

### Update Database
When you changes your models you will need to undertake the migration process. First make the migrations:

    $ python manage.py makemigrations <app_name>

Then apply the migrations:

    $ python manage.py migrate


Sometime the migrations wont go smoothly because of an unresolvable conflict. If this happens, you can delete the database and all the migrations in the directory `<app_name>/migrations`, and then repeat the process above. This will destroy all your data!


## Setup Paths
Set up your `BASE_DIR`, in `settings.py`:

```
import os
BASE_DIR = os.getcwd()
```

### Templates Path

In `settings.py` add:
```
 TEMPLATE_PATH = os.path.join(BASE_DIR, 'templates')
 TEMPLATE_DIRS = (TEMPLATE_PATH,)
```
For each `<app_name>`, create a directory called `<app_name>` in this templates directory. Then refer to `<app_name>/<template_name>' in your code i.e. when calling  `render()`.

Create a Simple View
--------------------

In `<app_name>/views.py`:

```
from django.http import HttpResponse

def index(request):
    return HttpResponse("Rango says hey there world!")

```

In `<app_name>/urls.py`:

```
from django.conf.urls import patterns, url
from <app_name> import views

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'))

```

Remember to include a pointer to your `<app_name>` urls in `<project_name>/urls.py` add:

```
 url(r'^rango/', include('rango.urls')),
```




### Set up Static Path
In `settings.py` add/include:

```
    STATIC_PATH = os.path.join(BASE_DIR,'static')
    STATIC_URL = '/static/'
```

You may find this is already defined as such.

```
    STATICFILES_DIRS = (
        STATIC_PATH,
    )
```

In `<project_name>/urls.py` add:

```

from django.conf import settings # New Import
from django.conf.urls.static import static # New Import


if not settings.DEBUG:
        urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)```



To include staticfiles in the templates, in the template include:

```
{% load staticfiles %}
```

Reference static media with the static tag, i.e:


```
<img src="{% static "images/rango.jpg" %}" alt="Picture of Rango" />
```


###Set up the Media Server (for debugging)

In `<project_name>/urls.py` add:

```
if settings.DEBUG:
     urlpatterns += patterns(
         'django.views.static',
         (r'^media/(?P<path>.*)',
         'serve',
         {'document_root': settings.MEDIA_ROOT}), )
```


And in `settings.py` add:
```
    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```



##Models

### Create the Model

In `<app_name>/models.py`, create a model:

```
class <model_name>(models.Model):
	<field_name_1> = models.<FieldType>()
    <field_name_2> = models.<FieldType>()


	def __unicode__(self):
		# need to return a unicode string
		return self.<field_name_x>

```

where common `<FieldType>`s include `CharField`, `IntegerField`, `BooleanField`, see more at: [Django Models Field Reference](https://docs.djangoproject.com/en/1.7/ref/models/fields/)


### Register your model in the admin interface

In `<app_name>/admin.py` add in the code to register the interface:

```
from django.contrib import admin
from rango.models import <model_name>

admin.site.register(model_name)
```

###Create a population script

The basic template for the population script is:

```
	import os
	os.environ.setdefault('DJANGO_SETTINGS_MODULE', '<project_name>.settings')

	import django
	django.setup()

	from <app_name>.models import <model_name>

	def populate():

		<model_name>.objects.get_or_create('values')
		....

	if __name__ == '__main__':
	    print("Starting population script...")
	    populate()

```

Save the script into the base directory and to run the population script:

    python populate.py

Note that if you use `<model_name>.objects.get_or_create()` it will return a list of records matching that values provided.

Let's say you have a Person model with name and age (default=0). So you add a Person, with

    Person.objects.get_or_create(name='Jim', age='20')

If you want to update Jim's age, and change the script so that it is:

    Person.objects.get_or_create(name='Jim', age='21')

Then django will create a new record, and so you will have two records: (Jim, 20) and (Jim, 21) in the database.

Now if you asked for:

    jims = Person.objects.get_or_create(name='Jim')

you would have a list of records that match the name 'Jim', in this case the list would contain [ (Jim, 20), (Jim, 21) ]. If the model was empty, then a new Jim record would be created and it would return [ (Jim, 0) ]

Let's say that the name property is unique and that the model contains (Jim, 20), when the script is updated with:

    Person.objects.get_or_create(name='Jim', age='21')

and then executed, a unique constraint error will occur. This is because Django tries to create a new Jim record, because it can not find a jim who is 21 in the model. To avoid such problems, we need to first find the record by the unique fields first, i.e:

    jim = Person.objects.get_or_create(name='Jim')[0]

Then update jim's record, note we have to select the first (and only) Jim from the list.

    jim.age = 21
    jim.save()

Note we have to change the attribute and then save it!

##Create a Data-Driven Page

You will need to:

* create the view function to handle the request
* create the template to present/house the data
* create the url mapping that points to the view


### View

In `views.py`, in the `<view_function name>`select the data that you want to present, for example:


```
def <view_function_name>(request):
    n = 10 #max number of objects to take from the model
    data_to_show = <model_name>.objects.order_by('-<some_attribute>')[:n]
    context_dict = {'<variable_name_that_references_data_in_template>': data_to_show}
    return render (request, '<appname>/template_name.html', context_dict)

```

In this view, up to ten items from <model_name> are selected, and then passed to the template.

### Template

In template, `<appname>/template_name.html`, access the data:

```
	{% for record in <variable_name_that_references_data_in_template> %}
    	<p>{{ field.<attribute_name> }}</p>
    {% endfor %}

```
### URL Mapping
Finally you need to link your view to a URL. For the example you would add the following to `urls.py`:


    url(r’^datadriven/$’, view.<view_function_name>, name=‘datadriven’)



## URL Patterns

Some special characters that can be put in URL patterns:

* `^` starts with
* `d` alphanumeric
* `|` optional, i.e. drinks/mocha|expresso
* `$` no trailing characters

Below are a number of example URLs, URL patterns along with the matching view function headers and template references:

### URL with a 4 digit number
Examples:

* /year/2002/
* /year/2042/

Url Mapping:

	url(r’^year/(?P<year>\d{4})/$’, view.year_view, name=‘year’)

View:

	def year_view(request, year):

Template:

	{% url ‘year’ 1945 %}
	{% url ‘year’ {{item.year}} %}

where `item` is an object with an attribute year.


### URL with a four digit and two digit number

Examples:

* /yearmonth/2002/12/
* /yearmonth/2042/03/


Url Mapping:

    url(r’^year/(?P<year>\d{4})/(?P<month>\d{2})/$’, view.year_month_view)

View:

    def year_month_view(request, year, month):

Template:

tba


### URL with a number of any length

Examples:

* /number/38382992/
* /number/3838/
* /number/123/

Url Mapping:

    url(r’^year/(?P<number>\d+)/$’, view.number_view)

View:

    def number_view(request, number):

# URL with slug lines

Examples:
* /slug/monkey-brains-eaten/
* /slug/temple-destroyed/
* /slug/arc-stolen-from-temple/

Urls Mapping:

	url(r’^slug/(?P<page_slug>[\w\-]+)’, view.slug_view, name=‘slug’)

The string must contain alphanumeric (`\w`) characters and/or dashes(`\-`)
and there can be any number of these (i.e. `+`)

views:

	def slug_view(request, page_slug)

Templates:

	{% url ‘slug’ monkey-brains-eaten %}
	{% url ‘slug’ item.slug %}

where item is an object with an attribute slug.







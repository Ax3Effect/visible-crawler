from django.shortcuts import render

from web.crawler import Crawler
from web.forms import UrlForm


# Create your views here.
def get_name_view(request):
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = UrlForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            url = form.cleaned_data["url"]
            crawler = Crawler(url)
            data = crawler.crawl(url)
            print(type(data))
            return render(request, "pages/crawler.html", {"form": form, "data": data})

    # if a GET (or any other method) we'll create a blank form
    else:
        form = UrlForm()

    return render(request, "pages/crawler.html", {"form": form})

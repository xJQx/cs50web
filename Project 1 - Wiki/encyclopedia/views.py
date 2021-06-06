from django.shortcuts import render
from markdown2 import markdown
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from random import randrange

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })
    

def title(request, title):
    if util.get_entry(title) == None:
        return render(request, "encyclopedia/error.html", {
            "message": "entry not found!"
        })
    # if entry exists
    else:
        entry = util.get_entry(title)
        return render(request, "encyclopedia/entry.html", {
            "entry": markdown(entry),
            "title": title
        })

def search(request):
    if request.method == "POST":
        result = request.POST
        title = result["q"]

        # if query gives a result
        if util.get_entry(title) != None:
            return render(request, "encyclopedia/entry.html", {
                "entry": markdown(util.get_entry(title)),
                "title": title
            })
        
        # when query does not match any entry, show a result page when titles are links to entry pages
        else:
            # list to store matching substrings
            results = []

            query = title.upper()
            query_length = len(query)
            titles = util.list_entries()
            for name in titles:
                n = 0
                for i in range(0, query_length):
                    if query[i] in name.upper():
                        n += 1
                if n == query_length:
                    results.append(name)

            return render(request, "encyclopedia/search.html", {
                "results": results
            })
    else:
        render(request, "encyclopedia/index.html")

def newpage(request):
    if request.method == "POST":
        # store values from post into a dict
        info = request.POST
        title = info["title"]
        textarea = info["textarea"]

        # check if title already exists in the encyclopedia
        title_list = util.list_entries()
        for name in title_list:
            if title == name:
                return render(request, "encyclopedia/error.html", {
                    "message": "title already exists in the encyclopedia!"
                })
        
        # create the new entry in the encyclopedia
        util.save_entry(title, textarea)
        return HttpResponseRedirect(reverse("title", kwargs={'title':title}))

    else:
        return render(request, "encyclopedia/newpage.html")


def editpage(request, title):
    if request.method == "POST":
        info = request.POST
        name = info["title"]
        textarea = info["textarea"]
        
        # save the new entry
        util.save_entry(name, textarea)

        # redirect back to entry page
        return HttpResponseRedirect(reverse("title", kwargs={'title':title}))

    else:
        old_text = util.get_entry(title)
        return render(request, "encyclopedia/editpage.html", {
            "old_text": old_text,
            "title": title
        })

def random(request):
    titles = util.list_entries()
    n = randrange(0, len(titles), 1)
    title = titles[n]

    return HttpResponseRedirect(reverse("title", kwargs={"title":title}))
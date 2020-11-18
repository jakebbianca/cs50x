from django import forms
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
import markdown2

from . import util

class newSearchForm(forms.Form):
    q = forms.CharField(label="Search Encyclopedia")


def index(request):

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(), "form": newSearchForm()
    })

def entry(request, title):

    if not util.get_entry(title):
        return render(request, "encyclopedia/no_entry.html")
    
    return render(request, "encyclopedia/entry.html", {
        "title": title, "content": markdown2.markdown(util.get_entry(title)), "form": newSearchForm()
    })

def search(request):

    if request.method == "POST":

        form = newSearchForm(request.POST)

        if form.is_valid():

            q = form.cleaned_data["q"]

            entries = util.list_entries()

            for entry in entries:
                if entry.casefold() == q.casefold():
                    return render(request, "encyclopedia/entry.html", {
                        "title": entry, "content": markdown2.markdown(util.get_entry(entry)), "form": form
                    })

            filtered = [k for k in entries if q.casefold() in k.casefold()]

            return render(request, "encyclopedia/search.html", {
                "entries": filtered, "q": q, "form": form
            })
    
        else:

            return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries(), "form": form
            })

    else:

        return render(request, "encyclopedia/search.html", {
            "entries": [], "form": newSearchForm
        })
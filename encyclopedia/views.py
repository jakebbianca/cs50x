from django import forms
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponseNotFound
import markdown2

from . import util

class newSearchForm(forms.Form):
    q = forms.CharField(label="Search Encyclopedia")

class newEntryForm(forms.Form):
    title = forms.CharField(label="Entry Title")
    content = forms.CharField(widget=forms.Textarea, label="Content")


def index(request):

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(), "searchForm": newSearchForm()
    })

def entry(request, title):

    if not util.get_entry(title):
        return HttpResponseRedirect(reverse("no_entry"))
    
    return render(request, "encyclopedia/entry.html", {
        "title": title, "content": markdown2.markdown(util.get_entry(title)), "searchForm": newSearchForm()
    })

def no_entry(request):
    return render(request, "encyclopedia/no_entry.html", {
        "searchForm": newSearchForm()
    })

def search(request):

    if request.method == "POST":

        form = newSearchForm(request.POST)

        if form.is_valid():

            q = form.cleaned_data["q"]

            entries = util.list_entries()

            for entry in entries:
                if entry.casefold() == q.casefold():
                    return HttpResponseRedirect(reverse("entry", kwargs={"title": entry}))

            filtered = [k for k in entries if q.casefold() in k.casefold()]

            return render(request, "encyclopedia/search.html", {
                "entries": filtered, "q": q, "searchForm": form
            })
    
        else:

            return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries(), "searchForm": form
            })

    else:

        return render(request, "encyclopedia/search.html", {
            "entries": [], "searchForm": newSearchForm
        })

def new(request):

    if request.method == "POST":

        entryForm = newEntryForm(request.POST)

        if entryForm.is_valid():

            title = entryForm.cleaned_data["title"]
            entries = util.list_entries()

            for entry in entries:
                if title.casefold() == entry.casefold():
                    return render(request, "encyclopedia/new.html", {
                        "searchForm": newSearchForm(), "form": entryForm, "error": f"An entry with the title '{title}' already exists."
                    })

            content = newEntryForm.cleaned_data["content"]

            return render(request, "encyclopedia/new.html", {
                "searchForm": newSearchForm(), "form": newEntryForm()
            })




    return render(request, "encyclopedia/new.html", {
        "searchForm": newSearchForm(), "form": newEntryForm()
    })
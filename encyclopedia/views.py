from django import forms
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponseNotFound
import markdown2

from . import util


# define custom django form classes
class newSearchForm(forms.Form):
    q = forms.CharField(label="Search Encyclopedia")

class newEntryForm(forms.Form):
    title = forms.CharField(label="Entry Title")
    content = forms.CharField(widget=forms.Textarea, label="Content")

class newEditForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea, label="Content")


def index(request):
    
    # render a page with a list of all wiki entries
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(), "searchForm": newSearchForm()
    })


def entry(request, title):

    # if no entry exists for a given title, redirect to a 'not found' page
    if not util.get_entry(title):
        return HttpResponseRedirect(reverse("no_entry"))
    
    # if entry does exist, return that entry's contents
    return render(request, "encyclopedia/entry.html", {
        "title": title, "content": markdown2.markdown(util.get_entry(title)), "searchForm": newSearchForm()
    })


def no_entry(request):
    # not found page for nonexistent entries
    return render(request, "encyclopedia/no_entry.html", {
        "searchForm": newSearchForm()
    })


def search(request):

    if request.method == "POST":
        
        # pull user-entered data from search form
        form = newSearchForm(request.POST)

        # if data is valid, pull cleaned data for user query
        if form.is_valid():

            q = form.cleaned_data["q"]

            entries = util.list_entries()

            # compare user query to existing entries for case-insensitive match
            # if match exists, redirect user directly to the entry page
            for entry in entries:
                if entry.casefold() == q.casefold():
                    return HttpResponseRedirect(reverse("entry", kwargs={"title": entry}))

            # if no case-insensitive match, filter existing entries which contain the query string
            filtered = [k for k in entries if q.casefold() in k.casefold()]

            # return search results using filtered list
            return render(request, "encyclopedia/search.html", {
                "entries": filtered, "q": q, "searchForm": form
            })
    
        else:

            # if form isn't valid, return user to index
            return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries(), "searchForm": form
            })

    else:

        # if user GETs the search page, redirect them to the index page
        return HttpResponseRedirect(reverse("index"))


def new(request):

    if request.method == "POST":

        # pull user-entered data from new entry creation form
        entryForm = newEntryForm(request.POST)

        # if data passes is_valid(), check if an entry with the given title already exists
        if entryForm.is_valid():

            title = entryForm.cleaned_data["title"]
            entries = util.list_entries()

            for entry in entries:
                # if entry with this title already exists, return with error message to user
                if title.casefold() == entry.casefold():
                    return render(request, "encyclopedia/new.html", {
                        "searchForm": newSearchForm(), "form": entryForm, "error": f"An entry with the title '{title}' already exists."
                    })

            # if entry doesn't already exist, grab content input
            content = entryForm.cleaned_data["content"]
            # save the new entry
            util.save_entry(title, content)
            # redirect user to the page of the entry whihc they just created and saved
            return HttpResponseRedirect(reverse("entry", kwargs={"title": title}))

    # if GET request, bring user to empty page for new entry input
    return render(request, "encyclopedia/new.html", {
        "searchForm": newSearchForm(), "form": newEntryForm()
    })


def edit(request, title):

    if request.method == "POST":

        editForm = newEditForm(request.POST)

        if editForm.is_valid():

            content = editForm.cleaned_data["content"]

            util.save_entry(title, content)
        
            return HttpResponseRedirect(reverse("entry", kwargs={"title": title}))

    else:

        # if GET request, retrieve edit page for current entry
        # fill content Textarea with existing content

        form = newEditForm()
        form.fields["content"].initial = util.get_entry(title)

        return render(request, "encyclopedia/edit.html", {
            "title": title, "searchForm": newSearchForm(), "form": form
        })

from django.forms.widgets import Textarea
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django import forms
from django.urls import reverse

from . import util
import markdown
import random

class newPage(forms.Form):
    title = forms.CharField(label="Title of Page")
    # This would specify a form with a comment that uses a larger Textarea widget, rather than the default TextInput widget.
    textarea = forms.CharField(widget=forms.Textarea(attrs={'rows':'5'}), label='')

class Search(forms.Form):
    item = forms.CharField(widget=forms.TextInput(attrs={'class' : 'myfieldclass', 'placeholder': 'Search'}))

class Edit(forms.Form):
    textarea = forms.CharField(widget=forms.Textarea(attrs={'rows':'15'}), label='')


def index(request):
    entries = util.list_entries()
    requested = []
    if request.method == "POST":
        form = Search(request.POST)     # fetching the requested title into form
        if form.is_valid():
            item = form.cleaned_data["item"]
            for i in entries:
                if item in entries:
                    page = util.get_entry(item)
                    page_converted = markdown.markdown(page)
                    return render(request, "encyclopedia/read.html", {
                        'page': page_converted,
                        'title': item,
                        'form': Search()
                    })
                if item.lower() in i.lower():
                    requested.append(i)
            return render(request, "encyclopedia/search.html", {
                'searched': requested,
                'form': Search()
            })
        else:
            return render(request, "encyclopedia/index.html", {
                'form': form
            })
    else:
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries(),
            'form': Search()
        })

def new_page(request):
    if request.method == "POST":
        form = newPage(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["textarea"]
            entries = util.list_entries()
            if title in entries:
                return render(request, "encyclopedia/error.html", {
                    'form': Search(),
                    'message': "The Page already exist"
                })
            else:
                util.save_entry(title, content)
                page = util.get_entry(title)
                page_converted = markdown.markdown(page)
                return render(request, "encyclopedia/read.html", {
                    'form': Search(),
                    'page': page_converted,
                    'title': title
                })
    else:
        return render(request, "encyclopedia/new.html", {
            'form': Search(),
            'post': newPage()
        })

def edit(request, title):
    if request.method == 'GET':
        page = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
            'form': Search(),
            'edit': Edit(initial={'textarea': page}),
            'title': title
        })
    else:
        form = Edit(request.POST)
        if form.is_valid():
            textarea = form.cleaned_data["textarea"]
            util.save_entry(title,textarea)
            page = util.get_entry(title)
            page_converted = markdown.markdown(page)

            context = {
                'form': Search(),
                'page': page_converted,
                'title': title
            }

            return render(request, "encyclopedia/read.html", context)


def read_page(request, title):
    entries = util.list_entries()
    if title in entries:
        page = util.get_entry(title)
        page_converted = markdown.markdown(page)
        return render(request, "encyclopedia/read.html", {
            'title': title,
            'content': page_converted,
            'form': Search()
        })
    else:
        return render(request, "encyclopedia/error.html", {
            'message': 'The requested page was unable to locate',
            'form': Search()
        })

def search(request):
    query = request.GET.get("query")
    if query is None or query=="":
        return render(request, "encyclopedia/search.html", {
            'entries_list': "",
            'query': query
        })
    entries = util.list_entries()
    entries_list = [entry for entry in entries if query.lower() in entry.lower()]
    if len(entries_list)==1:
        return redirect("index.html", entries_list[0])
    return render(request, "encyclopedia/search.html", {
        'entries_list': entries_list,
        'query': query
    })
        
def random_page(request):
    return read_page(request, random.choice(util.list_entries()))
from django.shortcuts import render, redirect
from django.http import Http404
from django import forms
from random import choice
import markdown2
import os

ENTRIES_DIR = "entries"

class NewEntryForm(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(widget=forms.Textarea, label="Content")

class EditEntryForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea, label="Content")

def list_entries():
    entries = []
    if os.path.exists(ENTRIES_DIR):
        for filename in os.listdir(ENTRIES_DIR):
            if filename.endswith(".md"):
               entries.append(filename[:-3])
    return entries
def get_entry(title):
   filename = os.path.join(ENTRIES_DIR, f"{title}.md")
   if os.path.exists(filename):
      with open(filename, "r") as f:
          return f.read()
   else:
     return None


def save_entry(title, content):
    filename = os.path.join(ENTRIES_DIR, f"{title}.md")
    with open(filename, "w") as f:
        f.write(content)



def index(request):
    entries = list_entries()
    return render(request, "encyclopedia/index.html", {
        "entries": entries
    })

def entry_page(request, title):
    content = get_entry(title)
    if content is None:
        raise Http404("Page not found")
    html_content = markdown2.markdown(content)
    return render(request, "encyclopedia/entry_page.html", {
        "title": title,
        "content": html_content
    })

def search(request):
    query = request.GET.get('q', '')
    if not query:
      return redirect('index')

    entries = list_entries()
    if query in entries:
        return redirect('entry_page', title=query)

    search_results = [entry for entry in entries if query.lower() in entry.lower()]
    return render(request, "encyclopedia/search_results.html", {
        "query": query,
        "results": search_results
    })

def new_page(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            if get_entry(title):
              return render(request, "encyclopedia/error.html", {"message": "Entry already exists with this title."})

            save_entry(title, content)
            return redirect('entry_page', title=title)
    else:
        form = NewEntryForm()
        return render(request, "encyclopedia/new_page.html", {"form": form})

def edit_page(request, title):
    content = get_entry(title)
    if content is None:
        raise Http404("Page not found")

    if request.method == "POST":
        form = EditEntryForm(request.POST)
        if form.is_valid():
            new_content = form.cleaned_data["content"]
            save_entry(title, new_content)
            return redirect('entry_page', title=title)
    else:
      form = EditEntryForm(initial={'content': content})
      return render(request, "encyclopedia/edit_page.html", {
          "title": title,
          "form": form
      })

def random_page(request):
    entries = list_entries()
    if entries:
        random_entry = choice(entries)
        return redirect('entry_page', title=random_entry)
    else:
      return redirect('index')
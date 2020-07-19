from django.shortcuts import render,redirect
import markdown2
from django.http import HttpResponse
import random
from django import forms
from django.contrib import messages
from . import util

#djnago form
class contentform(forms.Form):
    content=forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))

#home page
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

#page for any entry
def title(request,title):
    entry=util.get_entry(title)
    if entry is None:
        return HttpResponse(" 404: Requested page doesn't exist")
    else:
        entry=markdown2.markdown(entry)
        return render(request,"encyclopedia/entry.html",{
        "entry":entry, "title":title
    })

#for search results page
def search(request):
    result=request.POST['q']
    print(result)
    check=util.get_entry(result)
    if check is None:
        results=[]
        entries=util.list_entries()
        for entry in entries :
            if result.upper()  in entry.upper():
                results.append(entry)

        return render (request,"encyclopedia/search.html",{
        "results":results
        })
    else:
        entry=markdown2.markdown(check)
        print(entry)
        return redirect(f'/wiki/{result}')


#for random page
def anypage(request):
    entries=util.list_entries()
#to generate a random number for a random page
    n=random.randint(0,len(entries)-1)
    entry=entries[n]
    return redirect(f'/wiki/{entry}')


#function to create a entry
def create(request):
    if request.method == 'POST':

        title=request.POST['Title']
        content=request.POST['content']

        check=util.get_entry(title)
        if check is None:
            util.save_entry(title,content)
            return redirect(f'/wiki/{title}')
        else:
            messages.error(request, 'The page already exists.')
            return render (request,"encyclopedia/create.html")
    else:
        return render (request,"encyclopedia/create.html")

#function to edit a page 
def editpage(request,title):
    if request.method == 'POST':
        form=contentform(request.POST)
        if form.is_valid():
            content=form.cleaned_data["content"]
            util.save_entry(title,content)
            return redirect(f'/wiki/{title}')
    else:
        text=util.get_entry(title)
        content = contentform ({'content': f'{text}'})

        return render (request,"encyclopedia/edit.html",{
        "form":content,"title":title
        })

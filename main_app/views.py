from django.shortcuts import render, redirect
from .models import Finch
# Create your views here.
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import HttpResponse
from .forms import FeedingForm

# Define the home view
def home(request):
  return HttpResponse('<h1>Hello, I\'m a finch.</h1>')

def about(request):
  return render(request, 'about.html')

def finches_index(request):
  finches = Finch.objects.all()
  return render(request, 'finches/index.html', {'finches': finches})

def finches_detail(request, finch_id):
  finch = Finch.objects.get(id=finch_id)
  return render(request, 'finches/detail.html', { 'finch': finch })

# use class(instead of def) to create CBV(class-based-view)
# see changes at urls.py line10
class FinchCreate(CreateView):
  model = Finch
  #CreateView rendered fileds as a form, with the help of finch_forn.html
  fields = '__all__'
  # or define field selectively:
  # fields = ['name', 'breed', 'description', 'age']
  
  # redirect to listview if create succussfully
  # success_url = '/finches/'

class FinchUpdate(UpdateView):
  model = Finch
  # Let's disallow the renaming of a finch by excluding the name field!
  fields = ['breed', 'description', 'age']

class FinchDelete(DeleteView):
  model = Finch
  success_url = '/finches/'

def finches_detail(request, finch_id):
  finch = Finch.objects.get(id=finch_id)
  # instantiate FeedingForm to be rendered in the template
  feeding_form = FeedingForm()
  return render(request, 'finches/detail.html', {
    # include the cat and feeding_form in the context
    'finch': finch, 'feeding_form': feeding_form
  })

def add_feeding(request, finch_id):
  form = FeedingForm(request.POST)
  # validate the form
  if form.is_valid():
    # don't save the form to the db until it
    # has the finch_id assigned
    new_feeding = form.save(commit=False)
    new_feeding.finch_id = finch_id
    new_feeding.save()
  return redirect('detail', finch_id=finch_id)
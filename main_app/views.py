from django.shortcuts import render, redirect
from .models import Finch, Toy
# Create your views here.
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import HttpResponse
from .forms import FeedingForm
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

# Define the home view
def home(request):
  return render(request, 'about.html')

def about(request):
  return render(request, 'about.html')

@login_required
def finches_index(request):
  finches = Finch.objects.filter(user=request.user)
  return render(request, 'finches/index.html', {'finches': finches})

def finches_detail(request, finch_id):
  finch = Finch.objects.get(id=finch_id)
    # Get the toys the cat doesn't have
  toys_finch_doesnt_have = Toy.objects.exclude(id__in = finch.toys.all().values_list('id'))
  feeding_form = FeedingForm()
  return render(request, 'finches/detail.html', { 
    'finch': finch,
    'feeding_form':feeding_form,
    'toys':toys_finch_doesnt_have
  })

# use class(instead of def) to create CBV(class-based-view)
# see changes at urls.py line10
class FinchCreate(LoginRequiredMixin, CreateView):
  model = Finch
  #CreateView rendered fileds as a form, with the help of finch_form.html
  fields = '__all__'
  # or define field selectively:
  # fields = ['name', 'breed', 'description', 'age']
  # This inherited method is called when a
  # valid form is being submitted
  def form_valid(self, form):
    # Assign the logged in user (self.request.user)
    form.instance.user = self.request.user  # form.instance is the cat
    # Let the CreateView do its job as usual
    return super().form_valid(form)
  
  # redirect to listview if create succussfully
  # success_url = '/finches/'

class FinchUpdate(UpdateView):
  model = Finch
  # Let's disallow the renaming of a finch by excluding the name field!
  fields = ['breed', 'description', 'age']

class FinchDelete(DeleteView):
  model = Finch
  success_url = '/finches/'


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

def assoc_toy(request, finch_id, toy_id):
  # Note that you can pass a toy's id instead of the whole object
  Finch.objects.get(id=finch_id).toys.add(toy_id)
  return redirect('detail', finch_id=finch_id)

def signup(request):
  error_message = ''
  if request.method == 'POST':
    # This is how to create a 'user' form object
    # that includes the data from the browser
    form = UserCreationForm(request.POST)
    if form.is_valid():
      # This will add the user to the database
      user = form.save()
      # This is how we log a user in via code
      login(request, user)
      return redirect('index')
    else:
      error_message = 'Invalid sign up - try again'
  # A bad POST or a GET request, so render signup.html with an empty form
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)
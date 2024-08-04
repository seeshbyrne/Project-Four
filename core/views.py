from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView

from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required # protect view functions
from django.contrib.auth.mixins import LoginRequiredMixin # protect class based views


from .models import Event

# def home(request):
#      return render(request, 'home.html')

class Home(LoginView):
    template_name = 'home.html'

def about(request):
    return render(request, 'about.html')

def signup(request):
    error_message = ''
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('cat-index')
        else:
            error_message = 'Invalid login - try again'
            # this would be the last line of the post request
    # everything here runs IF we had a GET request
    # OR if the form was invalid
    context = {'form': form, 'error_messsage': error_message}
    return render(request, 'signup.html', context)

@login_required
def event_index(request):
    events = Event.objects.all()
    return render(request, 'events/index.html', {'events': events})

@login_required
def event_detail(request, event_id):
    event = Event.objects.get(id=event_id)
    return render(request, 'events/detail.html', {'event': event})

class EventCreate(LoginRequiredMixin, CreateView):
    model = Event
    fields = ['name', 'date', 'location', 'description']

    def form_valid(self, form):
        # Assign the logged in user (self.request.user)
        form.instance.user = self.request.user  # form.instance is the event
        # Let the CreateView do its job as usual
        return super().form_valid(form)
    
class EventUpdate(LoginRequiredMixin, UpdateView):
    model = Event
    # Let's disallow the renaming of a cat by excluding the name field!
    fields = ['date', 'location', 'description']

class EventDelete(LoginRequiredMixin, DeleteView):
    model = Event
    success_url = '/events/'

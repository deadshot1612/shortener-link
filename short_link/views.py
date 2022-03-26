from datetime import datetime
from django.shortcuts import render 
from django.http import Http404, HttpResponseRedirect
from django.contrib.auth.decorators import login_required


from short_link.models import Shortener
from short_link.forms import ShortenerForm

# Create your views here.

@login_required(login_url='../accounts/register')
def home_view(request):
    context = {}
    context['form'] = ShortenerForm()
    if request.method == 'GET':
        return render(request, 'short_link/home.html', context)
    elif request.method == 'POST':
        used_form = ShortenerForm(request.POST)
        if used_form.is_valid():
            shortened_object = used_form.save()
            shortened_object.user = request.user
            shortened_object.save()
            new_url = request.build_absolute_uri('/') + shortened_object.short_url
            long_url = shortened_object.long_url 
            context['new_url']  = new_url
            context['long_url'] = long_url
            return render(request, 'short_link/home.html', context)
        context['errors'] = used_form.errors
        return render(request, 'short_link/home.html', context)


def redirect_url_view(request, shortened_part):
    try:
        shortener = Shortener.objects.get(short_url=shortened_part.lower())    
        shortener.used = datetime.now()   
        shortener.save()
        return HttpResponseRedirect(shortener.long_url)      
    except:
        raise Http404('Sorry this link is broken :(')
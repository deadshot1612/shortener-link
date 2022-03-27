from django.shortcuts import render 
from django.http import Http404, HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from asgiref.sync import sync_to_async
from django.utils import timezone

from short_link.models import Shortener
from short_link.forms import ShortenerForm

# Create your views here.

@login_required(login_url='login')
async def all_urls_view(request):
    all_urls = await sync_to_async(Shortener.objects.filter)(user=request.user)
    current_site = await sync_to_async(get_current_site)(request)
    return render(request, 'short_link/user_links.html', context={'domain': current_site.domain ,'all_urls': all_urls})

@login_required(login_url='login')
async def home_view(request):
    context = {}
    context['form'] = await sync_to_async(ShortenerForm)()
    if request.method == 'GET':
        return render(request, 'short_link/home.html', context)
    elif request.method == 'POST':
        used_form = await sync_to_async(ShortenerForm)(request.POST)
        if used_form.is_valid():
            shortened_object = await sync_to_async(used_form.save)()
            shortened_object.user = request.user
            await sync_to_async(shortened_object.save)()
            new_url = request.build_absolute_uri('/') + shortened_object.short_url
            long_url = shortened_object.long_url 
            context['new_url']  = new_url
            context['long_url'] = long_url
            return render(request, 'short_link/home.html', context)
        context['errors'] = used_form.errors
        return render(request, 'short_link/home.html', context)

@login_required(login_url='login')
async def delete(request,pk):
    if request.POST:
        url = sync_to_async(Shortener.objects.get)(pk=pk)
        if url.user == request.user:
            sync_to_async(url.delete)()
    return JsonResponse({"passed": True,})   

async def redirect_url_view(request, shortened_part):
    try:
        shortener = await sync_to_async(Shortener.objects.get)(short_url=shortened_part.lower())    
        shortener.used = sync_to_async(timezone.now)()   
        await sync_to_async(shortener.save)()
        return HttpResponseRedirect(shortener.long_url)      
    except:
        raise Http404('Sorry this link is broken :(')
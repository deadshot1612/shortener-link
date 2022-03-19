from django.contrib.auth import authenticate, login, logout
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib import messages
from django.urls import reverse
from .tasks import send_email_on_registration
from account.models import Account
from account.utils import generate_token
from .forms import RegistrationForm, UserForm




def log_user_in(request):
    if request.method == "POST":
        form = UserForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("all_quizes")
            else:
                messages.error(request,"Invalid username or password.")
                return HttpResponse(status=400)
        else:
            messages.error(request,"Invalid username or password.")
            return HttpResponse(status=400)
    else:
        form = UserForm()
    return render(request, 'accounts/login.html', context={'form':form})


def log_user_out(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('login')

  
def register(request):
    if request.user.is_authenticated:
        next_url = request.GET.get('next') or 'all_quizes'
        return redirect(next_url)
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            send_email_on_registration(current_site.domain, user.id)
            return redirect('all_quizes')
        else:
            return HttpResponse(status=400)
    else:
        form = RegistrationForm()
    return render(request, 'accounts/register.html', context={'form': form, 'next': request.GET.get('next') or 'all_quizes'})


def activate_user(request, uid, token):
    user = Account.objects.filter(id=uid).first()
    if user:
        if generate_token.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            return redirect(reverse('all_quizes'))
    return HttpResponse(content='Invalid activation link', status=401)
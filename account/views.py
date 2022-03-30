from django.contrib.auth import authenticate, login, logout
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.urls import reverse

from asgiref.sync import sync_to_async
from .tasks import send_email_on_login, send_email_on_registration
from .forms import LoginConfirmForm, RegistrationForm, UserForm
from account.models import Account, UserConfirmCode
from account.utils import create_random_code, generate_token


async def log_user_in(request):
    error_messages = None
    if request.method == "POST":
        form = await sync_to_async(UserForm, thread_sensitive=False)(data=request.POST)
        if form.is_valid():
            email  = await sync_to_async(form.cleaned_data.get, thread_sensitive=False)('email')
            password = await sync_to_async(form.cleaned_data.get, thread_sensitive=False)('password')
            user = await sync_to_async(authenticate)(username=email, password=password)
            if user is not None:
                    code = create_random_code()
                    UserConfirmCode.objects.create(user=user, code=code)
                    current_site = await sync_to_async(get_current_site)(request)
                    send_email_on_login(current_site.domain, user.id, code)
                    return redirect("login-confirm", pk=user.pk)
            else:
                error_messages = "Invalid email or password. If all correct Check your email to verify account "
        else:
            error_messages = "Invalid email or password."
    else:
        form = await sync_to_async(UserForm, thread_sensitive=False)(data=request.POST)
    return render(request, 'account/login.html', context={'form':form, 'error_message': error_messages})


async def log_user_out(request):
    if request.user.is_authenticated:
        await sync_to_async(logout)(request)
    return redirect('login')


async def register(request):
    next_url = await sync_to_async(request.GET.get, thread_sensitive=True)('next') or 'homepage'
    if request.user.is_authenticated:
        return redirect(next_url)
    if request.method == 'POST':
        form = await sync_to_async(RegistrationForm, thread_sensitive=False)(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            await sync_to_async(user.save, thread_sensitive=True)()
            current_site = await sync_to_async(get_current_site)(request)
            send_email_on_registration(current_site.domain, user.id)
            return redirect('login')
    else:
        form = await sync_to_async(RegistrationForm, thread_sensitive=False)()
    return render(request, 'account/register.html', context={'form': form, 'next': request.GET.get('next') or 'homepage'})


async def activate_user(request, uid, token):
    user = await sync_to_async(Account.objects.get, thread_sensitive=True)(id=uid)
    if user:
        if generate_token.check_token(user, token):
            user.is_active = True
            await sync_to_async(user.save)()
            return redirect(reverse('login'))
    return await HttpResponse(content='Invalid activation link', status=401)


async def login_confirm(request, pk):
    if request.user.is_authenticated:
        return redirect('homepage')
    if request.method == 'POST':
        form = await sync_to_async(LoginConfirmForm, thread_sensitive=False)(request.POST)
        if form.is_valid():
            user =  Account.objects.get(pk=pk)
            if UserConfirmCode.objects.filter(user=user, code=request.POST['code']).exists():
                login(request,user)
                await sync_to_async(UserConfirmCode.objects.filter(user=user, code=request.POST['code']).delete)()
                return redirect('homepage')
    else:
        form = await sync_to_async(LoginConfirmForm, thread_sensitive=False)()
    return render(request, 'account/login-confirm.html', context={'form': form , 'pk': pk})
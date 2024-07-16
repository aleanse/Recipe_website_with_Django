from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.http import Http404
from .forms import RegisterForm , Login_Form
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def register_view(request):

    form = RegisterForm(request.session.get('register_form_data'),None)
    form_action = 'authors:create_register'
    return render(request, 'authors/pages/register_view.html',context={'form':form,'form_action':form_action} )

def create_register(request):

    if not request.POST:
        raise Http404

    POST = request.POST
    request.session['register_form_data'] = POST
    form = RegisterForm(POST)
    if form.is_valid():
        user = form.save(commit=False)
        user.set_password(user.password)
        user.save()
        messages.success(request,'Your user is created, please log in')
        del (request.session['register_form_data'])
        return redirect('authors:login')
    return redirect('authors:register')

def login_view(request):
    form = Login_Form(request.session.get('create_login'),None)
    form_action = 'authors:create_login'

    return render(request,'authors/pages/login.html',context={'form':form,'form_action': form_action})

def create_login(request):
    if not request.POST:
        raise Http404

    request.session['create_login']  = request.POST
    form = Login_Form(request.POST)
    if form.is_valid():
        authenticated_user = authenticate(
            username = form.cleaned_data.get('username', ''),
            password = form.cleaned_data.get('password',''),
        )
        if authenticated_user is not None:
            messages.success(request,'Your are logged in')
            login(request,authenticated_user)

        else:
            messages.error(request, 'Invalid credentials')

    else:

        messages.error(request,'Invalid username or password')

    return redirect('authors:login')

@login_required(login_url='authors:login', redirect_field_name='next')
def logout_view(request):
    if not request.POST:
        return redirect('authors:login')
    if request.POST.get('username') != request.user.username:
        return redirect('authors:login')
    logout(request)
    return redirect('authors:login')




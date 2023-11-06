from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import forms, authenticate, login, logout, decorators
from . models import Content

def Landing(request):
    context = {}

    if request.user.is_authenticated:
        context['authenticated'] = True
        context['username'] = request.user

    return render(request, 'index.html', context)

def LoginSignup(request):
    loginForm = forms.AuthenticationForm()
    signupForm = forms.UserCreationForm()

    if request.method == "POST":
        if request.POST.get('formAction') == 'login':
            user = authenticate(request, username=request.POST.get('username'), password=request.POST.get('password'))

            if user:
                login(request, user)
                return redirect('homepage')

        elif request.POST.get('formAction') == 'signup':
            signupForm = forms.UserCreationForm(request.POST)
            if signupForm.is_valid():
                signupForm.save()
                return redirect('homepage')

    context = {'login':loginForm, 'signup':signupForm}

    return render(request, 'loginsignup.html', context)

def LogoutUser(request):
    logout(request)
    return redirect('loginsignuppage')

@decorators.login_required(login_url='loginsignuppage')
def Home(request):
    context = {}

    if request.user.is_authenticated:
        context['authenticated'] = True
        context['username'] = request.user

    context['content'] = Content.objects.all().values()
    return render(request, 'home.html', context)

def ManageContent(request):
    if request.method == 'POST':
        response = {
            'auth': False,
            'action': None,
            'target': None,
            'result': False,
            'reason': "Unknown",
        }

        if request.user.is_authenticated:
            response['auth'] = True
            if request.POST['action'] == 'Remove':
                response['action'] = 'Remove'

                if request.POST['target']:
                    response['target'] = request.POST['target']
                    #Try something here

                else:
                    response['reason'] = "No target selected."

            else:
                response['reason'] = "No such action."
        
        else:
            response['reason'] = "Unauthorized."

    return JsonResponse(response)
from django.shortcuts import render
from  django.http import HttpResponse
from userauths.forms import UserRegisterForm
from django .contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserChangeForm

User = settings.AUTH_USER_MODEL

def registration_page(request): 

    if request.method == "POST":
        form = UserRegisterForm(request.POST or None)
        if form.is_valid():
            new_user = form.save()    
            username = form.cleaned_data.get("username")    
            messages.success(request, f"Hi {username}, Your Account Was Created Successfullly.")
            new_user = authenticate(username = form.cleaned_data.get("email"),  
                                    password = form.cleaned_data.get("password1"))
            login(request, new_user)
            return redirect("core:index")
    else:
        print("Error registering User")
        form = UserRegisterForm()


    context = {
        'form': form
    }
    return render(request, 'authentication/sign-up.html', context)

def login_page(request):
    if not request.user.is_authenticated and 'next' in request.GET:
        messages.error(request, "You must be logged in to log out.")  # Error message for unauthorized logout attempt

    if request.user.is_authenticated:
        messages.warning(request, f"You are already logged in.")
        return redirect("core:index")  # Redirect if already authenticated

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, username=email, password=password)  # Authenticate using email

        if user is not None:
            login(request, user)
            messages.success(request, "Log in successful.")
            return redirect("core:index")
        else:
            # Assuming email is not found or password is incorrect
            messages.error(request, "Invalid email or password. Please try again.")

    context = {

    }
    return render(request, "authentication/sign-in.html")

@login_required(login_url='userauths:login_page')  # Redirects to login page if not logged in.
def logout_page(request):
    logout(request)
    messages.success(request, "Logged Out Successfully.")
    return redirect("userauths:login_page")

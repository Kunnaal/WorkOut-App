import random
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from WorkOutApp import settings
from django.core.mail import EmailMessage, send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from . tokens import generate_token

display_images = [1, 2, 3, 4, 5, 6, 7, 8, 9]
gradients = ["background-color: #8BC6EC;background-image: linear-gradient(135deg, #8BC6EC 0%, #9599E2 100%);",
"background-color: #4158D0;background-image: linear-gradient(43deg, #4158D0 0%, #C850C0 46%, #FFCC70 100%);",
"background-image: linear-gradient(to right top, #051937, #004d7a, #008793, #00bf72, #a8eb12);",
"background-color: #FFDEE9;background-image: linear-gradient(0deg, #FFDEE9 0%, #B5FFFC 100%);",
]

def signup(request):

    context = {
        'display_image' : "animations/"+str(random.choice(display_images))+".gif",
        'gradient' : gradients[random.choice([x for x in range(4)])],
    }

    if request.method == 'POST':
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if User.objects.filter(username = username):
            messages.error(request, 'Username already exists, please try another username...')
            return redirect('signup')
        
        if User.objects.filter(email = email):
            messages.error(request, 'Email already exists, please try another email...')
            return redirect('signup')


        if len(username) > 10:
            messages.error(request, 'Username must be under 10 chars!')
            return redirect('signup')
        elif not username.isalnum():
            messages.error(request, 'Username must be alphanumeric')
            return redirect('signup')

        if pass1 != pass2:
            messages.error(request, 'Passwords don\'t match')
            return redirect('signup')

        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname

        myuser.is_active = False
        myuser.save()

        messages.success(request, "Your account has been successfully created! Conform your account through email.")

        # Welcome email
        subject = 'Welcome to authenticator!'
        message = 'Hello '+myuser.first_name+'! \nWelcome to authenticator.\nThank you for using our website.\nAn conformation email is also sent to your account!\n\nThank You!!'
        
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)

        # Confirmation Mail
        current_site = get_current_site(request)
        subject = 'Conformation email - Authenticator.'
        message = render_to_string('authentication/email_confirmation.html', {
            'name': myuser.first_name,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
            'token': generate_token.make_token(myuser),
        })
        
        email = EmailMessage(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [myuser.email],
        )

        email.fail_silently = True
        email.send()

        return redirect('signin')

    
    return render(request, 'authentication/signup.html', context)

def signin(request):

    context = {
        'display_image' : "animations/"+str(random.choice(display_images))+".gif",
        'gradient' : gradients[random.choice([x for x in range(4)])],
    }

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username = username, password = password)

        if user is not None:
            login(request, user)
            
            return redirect('home:/index', fname=user.first_name)
            # return render(request, 'authentication/index.html', {'fname': user.first_name})

        else:
            messages.error(request, 'Bad Credentials')
            return redirect('signin')

    return render(request, 'authentication/signin.html', context)

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        myuser = None
    
    if myuser is not None and generate_token.check_token(myuser, token):
        myuser.is_active = True
        myuser.save()
        login(request, myuser)
        return redirect('home')
    else:
        return render(request, 'authentication/activation_failed.html')


def signout(request):
    logout(request)
    messages.success(request, 'Logged out successfully')
    return redirect('home')

[Create User Sign Up View](https://simpleisbetterthancomplex.com/tutorial/2017/02/18/how-to-create-user-sign-up-view.html)

A number of python files to modify in order to achieve the user sign-up / registration procedure. The idea is to the build on top of the inherent `User` model and expand it to include email address as well as sending email confirmation for account activation.

### settings.py
at the bottom of the settings file, make sure to add this for the dev environment
```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

### models.py
Set up the Profile model on top of the built-in `User` model.
```python
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from phone_field import PhoneField


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    organization = models.CharField(max_length=50, blank=True)
    email = models.EmailField(null=True, blank=True)
    telephone = PhoneField(null=True, blank=True)
    join_date = models.DateField(null=True, blank=True)
    email_confirmed = models.BooleanField(default=False)  # flag for activated account


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
```

### views.py
This one is trickier. We need a few views and pages for this:
*  `homepage` -- which is where login/account activation will be directed to
*  `signup` -- the signup form
*  `account_activation_sent` -- redirect page after signup form completed
*  `activate` -- the url provided in the email confirmation for account activation

```python
# these are needed for the signup form and Activation
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib.auth import login, authenticate
from etlapp.forms import SignUpForm
from etlapp.tokens import account_activation_token
from django.utils.encoding import force_text
from django.contrib.auth.models import User

# regular libraries
from django.shortcuts import render, redirect
import datetime


# homepage
def homepage(request):

    return render(request, 'pages/home.html')


# signing up for the website
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():

            # set the user to inactive until activated
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate Your Account'
            message = render_to_string('pages/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)

            # load the profile instance created by the signal
            user.refresh_from_db()

            # perform a separate save for the profile instance information
            user.profile.first_name = form.cleaned_data.get('first_name')
            user.profile.last_name = form.cleaned_data.get('last_name')
            user.profile.organization = form.cleaned_data.get('organization')
            user.profile.email = form.cleaned_data.get('email')
            user.profile.telephone = form.cleaned_data.get('telephone')
            user.profile.join_date = datetime.date.today()
            user.save()

            '''
            # check authentication -- not needed anymore due to account activation
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('homepage')
            '''

            return redirect('account_activation_sent')
    else:
        form = SignUpForm()
    return render(request, 'pages/signup.html', {'form': form})


# email activation email sent
def account_activation_sent(request):

    return render(request, 'pages/account_activation_sent.html')


# activate email
def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user)
        return redirect('homepage')
    else:
        return render(request, 'pages/account_activation_invalid.html')
```

### urls.py
Simply set the 4 views from above to their appropriate pages
```python
from django.contrib import admin
from django.urls import path, re_path

from etlapp import views as etl_views

urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^home', etl_views.homepage, name='homepage'),
    re_path(r'^signup/$', etl_views.signup, name='signup'),
    re_path(r'^account_activation_sent/$', etl_views.account_activation_sent, name='account_activation_sent'),
    re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        etl_views.activate, name='activate'),
]
```

### tokens.py
This file generates the token for the account activation email
```python
from django.contrib.auth.tokens import PasswordResetTokenGenerator
# from django.utils import six -- removed in django 3.0


class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            str(user.pk) + str(timestamp) +
            str(user.profile.email_confirmed)
        )


account_activation_token = AccountActivationTokenGenerator()
```

### forms.py
This form is on top of the built-in `UserCreationForm`.
```python
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from phone_field import PhoneFormField


# extends the base UserCreationForm
class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30)  # default is required
    last_name = forms.CharField(max_length=30)
    organization = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=254)
    telephone = PhoneFormField(required=True)

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2',
                  'first_name', 'last_name', 'organization', 'email', 'telephone')
```

## Dev Environment Email Sent
![image](/static/img/markdowns/user_registration1.png)

## Other Reference Links
[Extend Django User Model](https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html)  
[Create One Time Link](https://simpleisbetterthancomplex.com/tutorial/2016/08/24/how-to-create-one-time-link.html)  
[Send Email in Django](https://simpleisbetterthancomplex.com/tutorial/2016/06/13/how-to-send-email.html)
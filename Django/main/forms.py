from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import Profile
class RegistrationForm(forms.Form):
    email = forms.EmailField(max_length=25,label='Enter Email ID')
    username = forms.CharField(max_length=25,label='Enter Name')
    password1 = forms.CharField(widget=forms.PasswordInput,label='Enter password')
    password2 = forms.CharField(widget=forms.PasswordInput,label='Confirm password')

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('register', 'Register'))


class LoginForm(forms.Form):
    emailid = forms.EmailField(max_length=25,label='Enter Email ID')
    password = forms.CharField(widget=forms.PasswordInput,label='Enter password')

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('login', 'Login'))
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
class RegisterForm(forms.ModelForm):
    password2 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'placeholder': 'Repeat your password'}),
                                error_messages={'password2': {'required': 'password2 must not be empty',}},
                                label='Password2')
    first_name = forms.CharField(required=True,label='First name',widget=forms.TextInput(attrs={'placeholder':'First name'}),
                                 error_messages={'required': 'This field must not be empty'})
    last_name = forms.CharField(required=True, label='Last name', widget=forms.TextInput(attrs={'placeholder': 'Last name'}),
                                error_messages={'required': 'This field must not be empty'})
    username = forms.CharField(required=True,label='Username',widget=forms.TextInput(attrs={'placeholder': 'Username'}),
                               error_messages={'required':'This field must not be empty'})

    class Meta: # especifica o modelo e os campos do modelo que serão usados
        model = User
        fields = ['username','email','first_name','last_name','password']
        labels = {
            'email':'Email',
            'password':'Password'
        }
        help_texts = {
            'email':'The E-mail must be valid.',
            'password': 'Password must have at least one uppercase letter,one lowercase letter and one number.the length should be at'
                        'least 8 characters'
        }
        error_messages = {
            'password':{
                'required':'This field must not be empty',
            }
        }
        widgets = {
            'password': forms.PasswordInput(attrs={'placeholder': 'Type your password here'}),
            'email': forms.TextInput(attrs={'placeholder': 'Your E-mail'}),

        }
    def clean_password(self):
        data = self.cleaned_data.get('password')
        return data

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password != password2:
            raise ValidationError({
                'password': 'Password and Password 2 must be equal'
            })



    def clean_email(self):
        email = self.cleaned_data.get('email')
        exists = User.objects.filter(email=email).exists()
        if exists:
            raise ValidationError('User E-mail is already in use ', code='invalid', )

        return email
    def clean_username(self):
        username = self.cleaned_data.get('username')
        exists = User.objects.filter(username=username).exists()
        if exists:
            raise ValidationError('User Username is already in use ', code='invalid', )

        return username
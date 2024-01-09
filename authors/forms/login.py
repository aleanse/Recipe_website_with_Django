from django import forms

class Login_Form(forms.Form):
    username = forms.CharField(required=True,widget=forms.TextInput(attrs={'placeholder':'Username'}),error_messages={'invalid':'Email invalid'})
    password = forms.CharField(required=True,widget=forms.PasswordInput(attrs={'placeholder':'Password'}),error_messages={'invalid':'password invalid'})
from django import forms
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'input','maxlength':'100', 'placeholder':'Enter Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'input', 'maxlength':'100', 'placeholder':'Enter password'}))
    
    def clean_username(self):
        uname = self.cleaned_data.get('username')
        if len(uname) < 5:
            raise forms.ValidationError("Username is too short")
        return uname
    
    def clean_password(self):
        pwd = self.cleaned_data.get('password')
        if '&' not in pwd:
            raise forms.ValidationError("The password should must contain '&'.")
        return pwd

class RegisterForm(forms.Form):
    firstname = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'maxlength':'25', 'placeholder':'Enter your First Name'}))
    lastname = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'maxlength':'25','placeholder':'Enter your Last Name'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'maxlength':'25','placeholder':'Enter your Username'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'input', 'maxlength':'25','placeholder':'Enter your email'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input', 'maxlength':'25','placeholder':'Enter a password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input', 'maxlength':'25','placeholder':'Confirm password'}))
    
    class Meta:
        model = User
        fields = ['username', 'email', 'fullname', 'lastname']
    
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        
        return cleaned_data

    def save(self):
        # Get the cleaned data
        firstname = self.cleaned_data.get('firstname')
        lastname = self.cleaned_data.get('lastname')
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password1')


        # Create a new User object
        user = User.objects.create(
            username=username,
            email=email,
            firstname=firstname,
            lastname=lastname
        )
        
        # Set the user's password
        user.set_password(password)
        
        # Save the user to the database
        user.save()
        return user


    



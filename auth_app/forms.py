from django import forms
from django.contrib.auth.models import User
import re
import datetime
class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'input',
            'maxlength': '100',
            'placeholder': 'Enter Username'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'input',
            'maxlength': '100',
            'placeholder': 'Enter Password'
        })
    )

    def clean_username(self):
        uname = self.cleaned_data.get('username')
        if len(uname) < 5:
            raise forms.ValidationError("Username must be at least 5 characters long.")
        return uname

    def clean_password(self):
        pwd = self.cleaned_data.get('password')
        if '&' not in pwd:
            raise forms.ValidationError("Password must contain the '&' character.")
        return pwd
class RegisterForm(forms.Form):
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={ 'maxlength':'25', 'placeholder':'Enter your First Name'})
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={ 'maxlength':'25','placeholder':'Enter your Last Name'})
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={ 'maxlength':'25','placeholder':'Enter your Username'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={ 'maxlength':'25','placeholder':'Enter your email'})
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={ 'maxlength':'25','placeholder':'Enter a password'})
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={ 'maxlength':'25','placeholder':'Confirm password'})
    )

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if len(password1) < 8:
            raise forms.ValidationError("Password must be at least 8 characters long.")
        if not re.search('[A-Z]', password1):
            raise forms.ValidationError("Password must contain at least one uppercase letter.")
        if not re.search('[a-z]', password1):
            raise forms.ValidationError("Password must contain at least one lowercase letter.")
        if not re.search('[0-9]', password1):
            raise forms.ValidationError("Password must contain at least one digit.")
        return password1

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if not first_name.isalpha():
            raise forms.ValidationError("First name should only contain alphabetic characters.")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if not last_name.isalpha():
            raise forms.ValidationError("Last name should only contain alphabetic characters.")
        return last_name

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("An account with this email already exists.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data

    def save(self):
        first_name = self.cleaned_data["first_name"]
        last_name = self.cleaned_data["last_name"]
        email = self.cleaned_data["email"]
        password = self.cleaned_data["password1"]

        user = User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            email=email,
            username=email.split("@")[0],
            password=password,
        )
        return user


class TeacherForm(forms.Form):
    teacher = forms.ModelChoiceField(queryset=User.objects.exclude(is_superuser = True),widget=forms.Select(attrs={'class': 'teacher-list'}))
    address = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Enter Address'}))
    primary_number = forms.CharField(widget=forms.TextInput(attrs={'placholder':"Enter your primary number", 'maxlength':"10", 'minlength':'10'}))
    secondary_number = forms.CharField(widget = forms.TextInput(attrs={'placholder':"Enter your secondary number",'maxlength':'10', 'minlength':'10'}))
    dob = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    sex = forms.ChoiceField(choices=[('M','Male'), ('F','Female')], widget=forms.Select(attrs={'class':'teacher-details'}))
    image = forms.ImageField(widget=forms.FileInput(attrs={'class': 'choose-img', 'style': 'display:none'}))


    def clean_image(self):
        image = self.cleaned_data.get('image')

        if not image:
            raise forms.ValidationError("No image uploaded. Please upload an image.")
        
        if image:
            if image.size > 1024 * 1024:
                raise forms.ValidationError("Image size is too large. Please choose a smaller image")

            valid_content_types = ['image/jpg', 'image/jpeg', 'image/png']
            if image.content_type not in valid_content_types:
                raise forms.ValidationError("Please choose a valid image file")
        return image

    def clean_primary_number(self):
        primary_number = self.cleaned_data.get('primary_number')
        if len(primary_number) != 10:
            raise forms.ValidationError("Primary number should be 10 digits long")
        return primary_number
    
    def clean_secondary_number(self):
        secondary_number = self.cleaned_data.get('secondary_number')
        primary_number  = self.cleaned_data.get('primary_number')
        if len(secondary_number) != 10:
            raise forms.ValidationError("Secondary number should be 10 digits long")
        elif secondary_number == primary_number:
            raise forms.ValidationError("Secondary number should be different from primary number")
        return secondary_number
    
    def clean_dob(self):
        dob = self.cleaned_data.get('dob')
        if dob > datetime.date.today():
            raise forms.ValidationError("Date of birth should be less than today")
        return dob
    
    def clean_address(self):
        address = self.cleaned_data.get('address')
        if len(address) < 10:
            raise forms.ValidationError("Address should be at least 10 characters long")
        return address


from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,PasswordChangeForm,UserChangeForm,SetPasswordForm,PasswordResetForm
from django.contrib.auth.models import User

from .models import Address, Contact


class UserCreateForm(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','PlaceHolder':"password"}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','PlaceHolder':"password"}))
    class Meta:
        model = User
        fields = ['username','email','password1','password2']
        help_texts = {
            'username': None
        }

        widgets = {
            'username':forms.TextInput(attrs={'class':'form-control','PlaceHolder':"username"}),
            # 'first_name':forms.TextInput(attrs={'class':'form-control'}),
            # 'last_name':forms.TextInput(attrs={'class':'form-control'}),
            'email':forms.EmailInput(attrs={'class':'form-control','PlaceHolder':"email"}),
        }

class PassChangeForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Enter Your Old Password'}))
    new_password1 =forms.CharField(label='New Password',widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Enter New Password'}))
    new_password2 =forms.CharField(label='Confirm New Password',widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Enter Re-New Password'}))


class UserProfileChangeForm(UserChangeForm):
    password =None
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email']
        widgets = {
            
        'username':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Username'}),

        'first_name':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter First Name'}),

        'last_name':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Last Name'}),

        'email':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter E-Mail'}),

    }

# Password Reset TextBox With Registred E-Mail
class PassResetForm(PasswordResetForm):
    email = forms.CharField(widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'Enter Your Registered E-Mail'}))
    
# New Password Set Registred E-Mail Link
class SetNewPassForm(SetPasswordForm):
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Enter New Password'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Confirm New Password'}))



class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['name','lastname','address','phone_number','city']
        widgets = {
            
        'name':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter First name'}),

        'lastname':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Last Name'}),

        'address':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Address'}),

        'phone_number':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Phone Number'}),

        'city':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter City'}),

    }

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name','email','phone_number','subject']   
        widgets = {
            
        'name':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter First name'}),

        'email':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Email'}),

        'phone_number':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Phone Number'}),

        'subject':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Subject'}),

    } 

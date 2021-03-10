from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django import forms
from .models import Noticia, Perfil

class CreateUserForm(UserCreationForm):
    class Meta:
        model=User
        fields=['username','email','first_name','last_name','password1','password2']
        
    
    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].error_messages.update({
            'required': 'El campo nombre es obligatorio',
        })
        self.fields['last_name'].error_messages.update({
            'required': 'El campo apellido es obligatorio',
        })
        self.fields['password1'].error_messages.update({
            'required': 'Ingrese una contraseña correcta',
        })
        self.fields['password2'].error_messages.update({
            'required': 'Debe reingresar la contraseña',
        })
        

        for key in self.fields:
            self.fields[key].required = True 


class EditProfileForm(UserChangeForm):
    class Meta:
        model=User
        fields=['first_name', 'last_name', 'email', 'password']


class NoticiaForm(forms.ModelForm):
    title = forms.CharField( label='Título')
    body = forms.CharField(widget=forms.Textarea, label='Descripción')
    class Meta:
        model=Noticia
        fields=['title', 'body'] 

class ImagenPerfilForm(forms.ModelForm):
    class Meta:
        model=Perfil
        fields=['avatar']
        
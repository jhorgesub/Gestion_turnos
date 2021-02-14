from django import forms

from .models import Turno
from django.contrib.admin.widgets import AdminDateWidget,AdminTimeWidget,AdminSplitDateTime                                   




class TurnoForm(forms.ModelForm):
    
    
    class Meta:
        model=Turno
        fields=['date','usuario']



    #date_time_input = forms.DateField(widget=AdminSplitDateTime()) 


    
    
    
    


    
        


      
        
        




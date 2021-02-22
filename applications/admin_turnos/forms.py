from django import forms

from .models import Turno
from django.contrib.admin.widgets import AdminDateWidget,AdminTimeWidget,AdminSplitDateTime                                   




class TurnoForm(forms.ModelForm):
    date = forms.DateField(  required=True,input_formats=['%Y-%m-%d','%d/%m/%Y'])
    



    class Meta:
        model=Turno
        fields=['date']
    
    


    
    

    




    
    
    
    


    
        


      
        
        




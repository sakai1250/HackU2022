from django import forms
from django.forms import ModelForm, TextInput
from .models import Topic, Entry, City, Order

class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['text']
        labels = {'text':''}
        
class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['text']
        labels = {'text': ''}
        widgets = {'text':forms.Textarea(attrs={'cols':80})}
        
class CityForm(forms.ModelForm):
    class Meta:
        model = City
        fields = ['name']
        widgets = {'name': TextInput(attrs={'class' : 'input', 'placeholder' : 'City Name'}),} 
        

class OrderForm(forms.ModelForm):
    class Meta:
        model   = Order
        fields  = [ 'order' ]
        labels = {'order':''}
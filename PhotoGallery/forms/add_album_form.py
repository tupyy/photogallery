from datetime import datetime

from django import forms


class AddAlbumForm(forms.Form):
    album_name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control",
                                                               "placeholder": "Enter name"}),
                                 label='Album name',
                                 max_length=100)
    album_date = forms.DateField(widget=forms.DateInput(attrs={"class": "form-control"}),
                                 input_formats=['%d-%m-%Y', '%d/%m/%Y'],
                                 initial=datetime.now().strftime('%d-%m-%Y'))
    album_category = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control",
                                                                   "placeholder": "Enter category"}),
                                     label='Album category',
                                     max_length=100, initial='Photos')

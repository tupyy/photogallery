from datetime import datetime

from django import forms


class AddAlbumForm(forms.Form):
    album_name = forms.CharField(label='Album name', max_length=100)
    album_date = forms.DateField(input_formats=['%d-%m-%Y', '%d/%m/%Y'], initial=datetime.now().strftime('%d-%m-%Y'))
    album_category = forms.CharField(label='Album category', max_length=100, initial='Photos')
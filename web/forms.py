from django import forms


class UrlForm(forms.Form):
    url = forms.CharField(label="URL to crawl", max_length=100)

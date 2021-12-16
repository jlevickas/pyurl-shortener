from django.shortcuts import render
from django.shortcuts import redirect
from . import forms
from django.forms import URLField
from .models import *
import secrets
import string
# Create your views here.


def index(request):
    form = forms.URLForm()
    url = ''
    message = ''
    absolute = request.build_absolute_uri()

    if request.method == "POST":
        form = forms.URLForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data['url']
            isvalid = validate_url(url)
            if 'http' not in url or 'https not in url':
                url = 'https://' + url

            if isvalid:
                if URL.objects.filter(og_url=url).exists():
                    print('existe')
                    shorten_url = URL.objects.filter(
                        og_url=url).values_list('shorten_url', flat=True)[0]
                else:
                    shorten_url = create_shurl()
                    db_url = URL.objects.create(
                        og_url=url, shorten_url=shorten_url)
                absolute_url = absolute + shorten_url
                message = 'Your shorten URL is: ' + absolute_url
            else:
                message = 'Enter a valid URL.'

    return render(request, "urlshortener/index.html", {"urlInput": form, "statusMessage": message})


def validate_url(url):
    url_form_field = URLField()
    try:
        url = url_form_field.clean(url)
        return True
    except:
        return False


def create_shurl():
    random_code = ''.join(secrets.choice(
        string.ascii_letters + string.digits) for _ in range(6))
    return random_code


def redirect_url(request, shorten_url):
    og_url = URL.objects.filter(shorten_url=shorten_url).values_list(
        'og_url', flat=True)[0]
    print(og_url)
    return redirect(og_url, permanent=True)

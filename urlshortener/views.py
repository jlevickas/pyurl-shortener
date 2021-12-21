from django.shortcuts import render, redirect
from . import forms
from django.forms import URLField
from .models import *
import secrets
import string
# Create your views here.


def index(request):
    absolute = request.build_absolute_uri()
    absolute_url = ''
    form = forms.URLForm()

    if request.method == "POST":
        form = forms.URLForm(request.POST or None)
        if form.is_valid():
            url = form.cleaned_data['url']
            isvalid = validate_url(url)
            # Adds https if not in URL (IMPORTANT FOR DJANGO REDIRECT)
            if 'http' not in url:
                url = 'https://' + url

            if isvalid:
                absolute_url = get_url(url, absolute)
            else:
                absolute_url = None

    return render(request, "urlshortener/index.html", {"urlInput": form, "fullURL": absolute_url})


def get_url(url, absolute):
    # Check if URL is already en DB, if it is, gets the linked code
    if URL.objects.filter(og_url=url).exists():
        shorten_url = URL.objects.filter(
            og_url=url).values_list('shorten_url', flat=True)[0]
    else:
        shorten_url = create_shurl()
        db_url = URL.objects.create(
            og_url=url, shorten_url=shorten_url)
    absolute_url = absolute + shorten_url
    return absolute_url


def validate_url(url):
    """
    Uses Django's URLField form to check if the input is an URL.
    """
    url_form_field = URLField()
    try:
        url = url_form_field.clean(url)
        return True
    except:
        return False


def create_shurl():
    """
    Uses the python standard libraries Secrets and String to create a 6 digit random code.
    Includes numbers and letters (uppercase and lowercase)
    """
    random_code = ''.join(secrets.choice(
        string.ascii_letters + string.digits) for _ in range(6))
    return random_code


def redirect_url(request, shorten_url):
    """
    Takes the code from the url and searches in the database for a match.
    Then redirects to the original URL linked to that code.
    """
    try:
        og_url = URL.objects.filter(shorten_url=shorten_url).values_list(
            'og_url', flat=True)[0]
        return redirect(og_url, permanent=True)
    except IndexError:
        return redirect('index')

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

            # Adds https if not in URL (IMPORTANT FOR DJANGO REDIRECT)
            if 'http' not in url or 'https not in url':
                url = 'https://' + url

            if isvalid:
                # Check if URL is already en DB, if it is, gets the linked code
                if URL.objects.filter(og_url=url).exists():
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
    og_url = URL.objects.filter(shorten_url=shorten_url).values_list(
        'og_url', flat=True)[0]
    print(og_url)
    return redirect(og_url, permanent=True)

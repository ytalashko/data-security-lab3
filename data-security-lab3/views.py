from django.http import HttpResponse
from django.template import loader

__author__ = 'mamax'

def index(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render())
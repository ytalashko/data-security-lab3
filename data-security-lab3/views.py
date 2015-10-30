from django.http import HttpResponse
from django.template import loader


def index(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render())

def viewObjects(request):
    template = loader.get_template('viewObjects.html')
    return HttpResponse(template.render())
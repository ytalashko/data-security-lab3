from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def index(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render())

@csrf_exempt
def viewObjects(request):
    template = loader.get_template('viewObjects.html')
    return HttpResponse(template.render())
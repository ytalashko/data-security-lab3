import json
import random

from fs.fs import FileSystem
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

fs = FileSystem()
active = False
x = random.randint(1, 9)


@csrf_exempt
def get_x(request):
    global x
    x = random.randint(1, 9)
    return HttpResponse(json.dumps(x))


@csrf_exempt
def login(request):
    user_name = request.POST.get('username')
    password = request.POST.get('password')
    y = request.POST.get('y')
    result = fs.login(user_name, password, x, y)
    global active
    active = result
    return HttpResponse(json.dumps(result))


@csrf_exempt
def logged(request):
    return HttpResponse(json.dumps(active and fs.logged()))


@csrf_exempt
def logout(request):
    global active
    active = False
    return HttpResponse(json.dumps(True))


@csrf_exempt
def check_captcha(request):
    y = request.POST.get('y')
    result = fs.check_captcha(x, y)
    global active
    active = result
    return HttpResponse(json.dumps(result))


@csrf_exempt
def read(request, path):
    if not (active and fs.logged()):
        return HttpResponse(json.dumps(None))
    data = fs.read(path)
    if type(data) is list:
        result = [{'name': e.name, 'user': e.user_name,
                   'right': e.ao_right, 'type': e.get_type} for e in data]
    else:
        result = data
    return HttpResponse(json.dumps(result))


@csrf_exempt
def write(request, path):
    if not (active and fs.logged()):
        return HttpResponse(json.dumps(False))
    data = request.POST.get('data')
    result = fs.write(path, data)
    return HttpResponse(json.dumps(result))


@csrf_exempt
def execute(request, path):
    if not (active and fs.logged()):
        return HttpResponse(json.dumps(False))
    result = fs.execute(path)
    return HttpResponse(json.dumps(result))


@csrf_exempt
def delete(request, path):
    if not (active and fs.logged()):
        return HttpResponse(json.dumps(False))
    print('delete')
    result = fs.delete(path)
    return HttpResponse(json.dumps(result))

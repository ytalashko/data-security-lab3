from fs.fs import FileSystem
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json

fs = FileSystem()


class JsonHttpResponse(HttpResponse):
    def __init__(self, content=b'',type='primitive', *args, **kwargs):
        super(JsonHttpResponse, self).__init__(JsonHttpResponse.to_json(content, type))

    @staticmethod
    def to_json(object, type):
        if type == 'object':
            return json.dumps(object.__dict__)
        else:
            return  json.dumps(object)


@csrf_exempt
def login(request):
    user_name = request.POST.get('username')
    password = request.POST.get('password')
    x = request.POST.get('x')
    y = request.POST.get('y')
    result = fs.login(user_name, password, x, y)
    return JsonHttpResponse(result)


@csrf_exempt
def logged(request):
    result = fs.logged()
    return JsonHttpResponse(result)


@csrf_exempt
def logout(request):
    result = fs.logout()
    return JsonHttpResponse(result)


@csrf_exempt
def check_captcha(request):
    x = request.POST.get('x')
    y = request.POST.get('y')
    result = fs.check_captcha(x, y)
    return JsonHttpResponse(result)


@csrf_exempt
def read(request, path):
    result = fs.read(path)
    return JsonHttpResponse(result, 'object')


@csrf_exempt
def write(request, path):
    data = request.POST.get('data')
    result = fs.write(path, data)
    return JsonHttpResponse(result, 'object')


@csrf_exempt
def execute(request, path):
    result = fs.execute(path)
    return JsonHttpResponse(result)


@csrf_exempt
def delete(request, path):
    print('delete')
    result = fs.delete(path)
    return JsonHttpResponse(result)

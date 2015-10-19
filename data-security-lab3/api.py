from fs.fs import FileSystem
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

fs = FileSystem()

@csrf_exempt
def login(request):
    user_name = request.POST.get('username')
    password = request.POST.get('password')
    x = request.POST.get('x')
    y = request.POST.get('y')
    result = fs.login(user_name, password, x, y)
    return HttpResponse(result)

@csrf_exempt
def logged(request):
    result = fs.logged()
    return HttpResponse(result)

@csrf_exempt
def logout(request):
    result = fs.logout()
    return HttpResponse(result)

@csrf_exempt
def check_captcha(request):
    x = request.POST.get('x')
    y = request.POST.get('y')
    result = fs.check_captcha(x, y)
    return HttpResponse(result)

@csrf_exempt
def read(request, path):
    result = fs.read(path)
    return HttpResponse(result)

@csrf_exempt
def write(request, path):
    data = request.GET.get('data')
    result = fs.write(path, data)
    return HttpResponse(result)

@csrf_exempt
def execute(request, path):
    result = fs.execute(path)
    return HttpResponse(result)

@csrf_exempt
def delete(request, path):
    result = fs.delete(path)
    return HttpResponse(result)

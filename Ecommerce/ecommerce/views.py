from django.shortcuts import redirect, render
from django.contrib import auth, messages 
from . import models
# Create your views here.
def login(request):
    
    context = {  }
    if request.method == 'POST':
        print("post")
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username = username, password =password )
        if user is not None:
            print("valid")
            auth.login(request , user)
            return render(request,'lista_productos.html')    
        else:
            print("not valid")
            messages.error(request, 'invalid username or password')
            return redirect("/ecommerce/login")
        
    else:
        print("get")
        return render(request,"login.html", context)

def lista_productos(request):
    
    context = {  }
    if request.method == 'POST':
        pass
        return render(request, 'lista_productos.html', {'form': "invalid"})
    else:
        return render(request,"lista_productos.html", context)
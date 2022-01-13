from django.shortcuts import redirect, render
from django.contrib import auth, messages 
from .models import *
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .forms import *
from datetime import date
import pycurl
from io import BytesIO
import json
# Create your views here.
def signin(request):
    
    context = {  }
    if request.method == 'POST':
        if "signup" in request.POST:
            return redirect("/ecommerce/signup")
        else:
            print("post")
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username = username, password =password )
            if user is not None:
                
                auth.login(request , user)
                return render(request,'lista_productos.html')    
            else:
                
                messages.error(request, 'invalid username or password')
                return redirect("/ecommerce/signin")
            
    else:
        print("get")
        return render(request,"login.html", context)

def lista_productos(request): 
    if request.method == 'POST':
        pass
        return render(request, 'lista_productos.html', {'form': "invalid"})
    else:
        context = {'products':Producto.objects.all()}
        return render(request,"lista_productos.html", context)


def signup(request):
    if request.method == 'POST':
        print('post')
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/ecommerce/lista_productos')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def agregar_producto(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto Publicado')
            return redirect('/ecommerce/lista_productos')
    else:
        form= ProductForm()
        form.fields['usuario'].initial=request.user
        form.fields['estado'].initial=1
        form.fields['fecha_publicacion'].initial=date.today()
    return render(request, 'agregar_producto.html', {'form': form})

def comprar_producto(request,id): 
    if request.method == 'POST':
        dat = {"id": 52, "configuration": [{"virbr0": {"address": "192.168.122.1"}}]}
        res = curl_post("http://192.168.122.191:8000/authorization/estado/", json.dumps(dat), "virbr0")
        print(res)
        
    else:
        form = PagoForm()
        context = {'product':Producto.objects.get(id=id),
                    'form': form}
        return render(request,"comprar_producto.html", context)




def curl_post(url, data, iface=None):
    c = pycurl.Curl()
    buffer = BytesIO()
    c.setopt(pycurl.URL, url)
    c.setopt(pycurl.POST, True)
    c.setopt(pycurl.HTTPHEADER, ['Content-Type: application/json'])
    c.setopt(pycurl.TIMEOUT, 10)
    c.setopt(pycurl.WRITEFUNCTION, buffer.write)
    c.setopt(pycurl.POSTFIELDS, data)
    if iface:
        c.setopt(pycurl.INTERFACE, iface)
    c.perform()

    # Json response
    resp = buffer.getvalue().decode('UTF-8')

    #  Check response is a JSON if not there was an error
    try:
        resp = json.loads(resp)
    except json.decoder.JSONDecodeError:
        pass

    buffer.close()
    c.close()
    return resp


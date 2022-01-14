from django.shortcuts import redirect, render
from django.contrib import auth, messages 
from .models import *
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .forms import *
from datetime import date
from io import BytesIO
import json
import requests
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
        context = {'products':Producto.objects.order_by('-fecha_publicacion')}
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

def compras(request):
    if request.method == 'POST':
        pass
    else:
        context = {'transacciones':Transaccion.objects.filter(usuario_comprador=request.user)}
    return render(request, 'compras.html', context)

def comprar_producto(request,id): 
    if request.method == 'POST':
        form= PagoForm(request.POST or None)
        dat = {"id": 52, "configuration": [{"virbr0": {"address": "192.168.122.1"}}]}
        headers = {"Content-Type": "application/json; charset=utf-8"}
        data = {"no_tarjeta":form["no_tarjeta"].value(),
        "nombre_tarjeta":form["nombre_tarjeta"].value(),
        "cvv":form["cvv"].value(),
        "fecha_vencimiento":form["fecha_vencimiento"].value(),
        "id_producto":Producto.objects.get(id=id).id,
            "nombre_producto":Producto.objects.get(id=id).nombre,
            "usuario_comprador":request.user.username,
            "fecha_peticion":str(date.today()),
        }
        data2="\'"+str(data)+"\'"
        
        try:
            response = requests.post("http://192.168.122.191:8000/authorization/transaccion/", headers=headers, data=json.dumps(data))
            print(response.json())
            if response.status_code == 201:
                print("201")
                pago = form.save()
                producto=Producto.objects.get(id=id)
                if response.json()['estado'] == 1:
                    messages.success(request, 'Tu transferencia a sido aceptada')
                    producto.estado=2
                    producto.save()
                    tr=Transaccion(producto=producto, usuario_comprador=request.user,
                    estado=1,fecha_publicacion=date.today(),pago=pago)
                    tr.save()
                    return redirect("/ecommerce/compras")
                elif response.json()['estado'] == 2:
                    messages.error(request, 'Tu transferencia a sido rechazada')
                    tr=Transaccion(producto=producto, usuario_comprador=request.user,
                    estado=2,fecha_publicacion=date.today(),pago=pago)
                    tr.save()
                    return redirect("/ecommerce/lista_productos")
                else:
                    messages.error(request, 'Tu transferencia esta pendiente a revision')
                    producto.estado=3
                    producto.save()
                    tr=Transaccion(producto=producto, usuario_comprador=request.user,
                    estado=3,fecha_publicacion=date.today(),pago=pago)
                    tr.save()
                    return redirect("/ecommerce/lista_productos")
            else:
                print(response)
                messages.error(request, 'El servidor no se encuentra disponble, intente mas tarde')
                return redirect("/ecommerce/lista_productos") 
        except requests.exceptions.ConnectionError:
            messages.error(request, 'El servidor no se encuentra disponble, intente mas tarde')
            return redirect("/ecommerce/lista_productos") 
        

        
        
    else:
        form = PagoForm()
        context = {'product':Producto.objects.get(id=id),
                    'form': form}
        return render(request,"comprar_producto.html", context)







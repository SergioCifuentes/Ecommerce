from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator

from decimal import *

# Modelo para Productos
class Producto(models.Model):
    
    nombre = models.CharField(max_length=25)
    descripcion = models.CharField(max_length=500)
    precio = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    estado = models.IntegerField() #1 A la venta #2 Vendido #3 En transicion
    fecha_publicacion = models.DateField()

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'

    def __str__(self) -> str:
        return self.nombre

class Pago(models.Model):
    
    no_tarjeta= models.BigIntegerField(null=True)
    nombre_tarjeta= models.CharField(max_length=40)
    cvv= models.IntegerField() 
    fecha_vencimiento = models.DateField(null=True)
    

    class Meta:
        verbose_name = 'Pago'
        verbose_name_plural = 'Pagos'

    def __str__(self) -> str:
        return self.id+" "+self.nombre_tarjeta

class Transaccion(models.Model):
    
    producto= models.ForeignKey(Producto, on_delete=models.CASCADE)
    usuario_comprador= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    estado = models.IntegerField() #1 Pendiente #2 Rechazado #Aprobado 
    fecha_publicacion = models.DateField(null=True)
    pago= models.ForeignKey(Pago, on_delete=models.CASCADE,null=True)
    

    class Meta:
        verbose_name = 'Transaccion'
        verbose_name_plural = 'Transacciones'

    def __str__(self) -> str:
        return self.id



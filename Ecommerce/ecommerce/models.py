from django.db import models

# Create your models here.
class Usuario(models.Model):
    id = models.BigIntegerField(primary_key=True)
    username = models.CharField(max_length=25)
    password = models.CharField(max_length=25)
    nombre = models.CharField(max_length=25)
    apellido = models.CharField(max_length=25)
    email = models.EmailField()
    phone_number = models.BigIntegerField()

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def __str__(self) -> str:
        return self.nombre + ' ' + self.apellido

# Modelo para Productos
class Producto(models.Model):
    id = models.BigIntegerField(primary_key=True)
    nombre = models.CharField(max_length=25)
    descripcion = models.CharField(max_length=500)
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    estado = models.IntegerField() #1 A la venta #2 Vendido #3 En transicion
    fecha_publicacion = models.DateField()

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'

    def __str__(self) -> str:
        return self.nombre

class Pago(models.Model):
    id = models.BigIntegerField(primary_key=True)
    tipo= models.IntegerField() 
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
    id = models.BigIntegerField(primary_key=True)
    producto= models.ForeignKey(Producto, on_delete=models.CASCADE)
    usuario_comprador= models.ForeignKey(Usuario, on_delete=models.CASCADE)
    estado = models.IntegerField() #1 Pendiente #2 Rechazado #Aprobado 
    fecha_publicacion = models.DateField(null=True)
    pago= models.ForeignKey(Pago, on_delete=models.CASCADE,null=True)
    

    class Meta:
        verbose_name = 'Transaccion'
        verbose_name_plural = 'Transacciones'

    def __str__(self) -> str:
        return self.id

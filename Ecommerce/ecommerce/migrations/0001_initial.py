# Generated by Django 4.0.1 on 2022-01-07 17:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Pago',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('tipo', models.IntegerField()),
                ('no_tarjeta', models.BigIntegerField(null=True)),
                ('nombre_tarjeta', models.CharField(max_length=40)),
                ('cvv', models.IntegerField()),
                ('fecha_vencimiento', models.DateField(null=True)),
            ],
            options={
                'verbose_name': 'Pago',
                'verbose_name_plural': 'Pagos',
            },
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=25)),
                ('descripcion', models.CharField(max_length=500)),
                ('precio', models.DecimalField(decimal_places=2, max_digits=8)),
                ('estado', models.IntegerField()),
                ('fecha_publicacion', models.DateField()),
            ],
            options={
                'verbose_name': 'Producto',
                'verbose_name_plural': 'Productos',
            },
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=25)),
                ('password', models.CharField(max_length=25)),
                ('nombre', models.CharField(max_length=25)),
                ('apellido', models.CharField(max_length=25)),
                ('email', models.EmailField(max_length=254)),
                ('phone_number', models.BigIntegerField()),
            ],
            options={
                'verbose_name': 'Usuario',
                'verbose_name_plural': 'Usuarios',
            },
        ),
        migrations.CreateModel(
            name='Transaccion',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('estado', models.IntegerField()),
                ('fecha_publicacion', models.DateField(null=True)),
                ('pago', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='ecommerce.pago')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecommerce.producto')),
                ('usuario_comprador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecommerce.usuario')),
            ],
            options={
                'verbose_name': 'Transaccion',
                'verbose_name_plural': 'Transacciones',
            },
        ),
        migrations.AddField(
            model_name='producto',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecommerce.usuario'),
        ),
    ]

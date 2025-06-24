from django.db import models

class Afirmacion(models.Model):
    texto = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    activa = models.BooleanField(default=True)

    def __str__(self):
        return self.texto[:50]

class Comentario(models.Model):
    nombre_usuario = models.CharField(max_length=100, default='Anónimo')
    afirmacion_texto = models.TextField(default='')  # Valor por defecto vacío
    texto = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre_usuario}: {self.texto[:30]}"

class Voto(models.Model):
    VOTO_CHOICES = [
        ("positivo", "Positivo"),
        ("neutral", "Neutral"),
        ("negativo", "Negativo"),
    ]
    nombre_usuario = models.CharField(max_length=100, default='Anónimo')
    afirmacion_texto = models.TextField(default='')  # Valor por defecto vacío
    valor = models.CharField(max_length=10, choices=VOTO_CHOICES)
    fecha = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre_usuario} - {self.valor}"

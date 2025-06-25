from django.db import models

class Afirmacion(models.Model):
    texto = models.TextField(unique=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    activa = models.BooleanField(default=True)

    def __str__(self):
        return self.texto[:50]

class Comentario(models.Model):
    afirmacion = models.ForeignKey(Afirmacion, on_delete=models.CASCADE, related_name='comentarios')
    nombre_usuario = models.CharField(max_length=100, default='Anónimo')
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
    afirmacion = models.ForeignKey(Afirmacion, on_delete=models.CASCADE, related_name='votos')
    nombre_usuario = models.CharField(max_length=100, default='Anónimo')
    valor = models.CharField(max_length=10, choices=VOTO_CHOICES)
    fecha = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre_usuario} - {self.valor} en {self.afirmacion.texto[:20]}"

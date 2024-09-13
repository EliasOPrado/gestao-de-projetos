from django.db import models
from django.core.validators import RegexValidator


class Cliente(models.Model):
    phone_regex = RegexValidator(
        regex=r"^\+\d{9,20}$",
        message="Phone number must be entered in the format: '+999999999'. Up to 20 digits allowed.",
    )
    nome = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    telefone = models.CharField(
        validators=[phone_regex], max_length=20, blank=True, null=True
    )

    def __str__(self):
        return self.nome


class Projeto(models.Model):
    STATUS_CHOICES = [
        ("em_andamento", "Em Andamento"),
        ("concluido", "Concluído"),
        ("pausado", "Pausado"),
    ]
    nome = models.CharField(max_length=255)
    descricao = models.TextField(blank=True)
    cliente = models.ForeignKey(
        Cliente, on_delete=models.CASCADE, related_name="projetos"
    )
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="em_andamento"
    )

    def __str__(self):
        return self.nome


class Atividade(models.Model):
    projeto = models.ForeignKey(
        Projeto, on_delete=models.CASCADE, related_name="atividades"
    )
    descricao = models.TextField()
    data_criacao = models.DateTimeField(auto_now_add=True)
    prazo = models.DateField()

    def __str__(self):
        return f"{self.projeto.nome} - {self.descricao[:20]}"

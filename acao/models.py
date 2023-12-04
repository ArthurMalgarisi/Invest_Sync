from django.db import models
from django.utils import timezone
# Create your models here.
class Acao(models.Model): #outraapp
    id_acao = models.AutoField(primary_key=True, db_column='id_acao')
    nome_acao = models.CharField(max_length=255)
    preco_mais_baixo = models.FloatField()
    preco_mais_alto = models.FloatField()
    simbolo_acao = models.CharField(max_length=20)
    nome_empresa = models.CharField(max_length=150)
    data_acao = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'Acao'

    # def __str__(self):
    #     return "({}) {}" .format(self.id_acao, self.nome_acao ,self.preco_mais_baixo, self.preco_mais_alto, self.descricao_acao,self.simbolo_acao, self.pais_de_origem, self.nome_empresa)
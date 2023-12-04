from django.db import models
from acao.models import Acao
from carteira.models import Carteira

# Create your models here.
class Carteira_Acao(models.Model): #juntas
    id_carteira_acao = models.AutoField(primary_key=True, db_column='id_carteira_acao')
    lote_acao = models.IntegerField()
    data_insercao = models.DateTimeField(auto_now_add=True)#deixar invisível somente para ser visto no banco
    cotacao = models.FloatField()
    data_compra = models.DateField()
    id_acao = models.ForeignKey(Acao, on_delete=models.CASCADE, db_column='id_acao')
    id_carteira = models.ForeignKey(Carteira, on_delete=models.CASCADE, db_column='id_carteira')

    class Meta:
        db_table = 'Carteira_Acao'

    def __str__(self):
        return "({}) {}" .format(self.id_carteira_acao, self.lote_acao ,self.data_insercao, self.id_acao, self.id_carteira)
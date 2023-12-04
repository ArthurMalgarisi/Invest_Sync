from django.db import models
from portfolio.models import Portfolio

# Create your models here.
class Carteira(models.Model): #juntas
    id_carteira = models.AutoField(primary_key=True, db_column='id_carteira')
    nome_carteira = models.CharField(max_length=255)
    valor_total_carteira = models.FloatField()
    descricao_carteira = models.TextField()
    id_portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, db_column='id_portfolio')

    class Meta:
        db_table = 'Carteira'

    def __str__(self):
        return "({}) {}" .format(self.id_carteira, self.nome_carteira ,self.valor_total_carteira, self.descricao_carteira, self.id_portfolio)
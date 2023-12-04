from django.db import models
from usuario.models import Usuario

# Create your models here.
class Portfolio(models.Model): #outra app
    id_portfolio = models.AutoField(primary_key=True, db_column='id_portfolio')
    nome_portfolio = models.CharField(max_length=255)
    descricao_portfolio = models.TextField()
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, db_column='id_usuario')

    class Meta:
        db_table = 'Portfolio'

    def __str__(self):
        return "({}) {}" .format(self.id_portfolio, self.nome_portfolio ,self.descricao_portfolio, self.id_usuario)
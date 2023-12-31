# Generated by Django 4.2.6 on 2023-11-07 05:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('carteira', '0001_initial'),
        ('acao', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Carteira_Acao',
            fields=[
                ('id_carteira_acao', models.AutoField(db_column='id_carteira_acao', primary_key=True, serialize=False)),
                ('lote_acao', models.IntegerField()),
                ('data_insercao', models.DateTimeField(auto_now_add=True)),
                ('cotacao', models.FloatField()),
                ('data_compra', models.DateField()),
                ('id_acao', models.ForeignKey(db_column='id_acao', on_delete=django.db.models.deletion.CASCADE, to='acao.acao')),
                ('id_carteira', models.ForeignKey(db_column='id_carteira', on_delete=django.db.models.deletion.CASCADE, to='carteira.carteira')),
            ],
            options={
                'db_table': 'Carteira_Acao',
            },
        ),
    ]

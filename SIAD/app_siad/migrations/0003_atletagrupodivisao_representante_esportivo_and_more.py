# Generated by Django 4.2.14 on 2024-11-07 16:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_siad', '0002_grupo_representante_esportivo'),
    ]

    operations = [
        migrations.AddField(
            model_name='atletagrupodivisao',
            name='representante_esportivo',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='app_siad.representanteesportivo'),
        ),
        migrations.AlterField(
            model_name='divisao',
            name='tipo_divisao',
            field=models.CharField(choices=[('G', 'Grupo'), ('I', 'Individual')], default='', max_length=1),
        ),
        migrations.AlterField(
            model_name='modalidade',
            name='categoria',
            field=models.CharField(choices=[('Geral', 'Geral'), ('Masc.', 'Masculino'), ('Fem.', 'Feminino')], default='', max_length=5),
        ),
    ]
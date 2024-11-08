import os
from django.db.models.signals import post_migrate, post_delete
from django.contrib.auth.models import Group
from django.dispatch import receiver
from .models import Atleta


@receiver(post_migrate)
def create_default_groups(sender, **kwargs):
    group_name = ['Representante Esportivo', 'Administrador Esportivo']
    for names in group_name:
        Group.objects.get_or_create(name=names)
from django.db.models.signals import post_migrate
from django.contrib.auth.models import Group
from django.dispatch import receiver

@receiver(post_migrate)
def create_default_groups(sender, **kwargs):
    group_names = ['Representante Esportivo', 'Administrador Esportivo']
    for name in group_names:
        Group.objects.get_or_create(name=name)


@receiver(post_delete, sender=Atleta)
def delete_comprovante_matricula(sender, instance, **kwargs):
    """
    Apaga o arquivo de comprovante de matrícula quando o atleta é deletado.
    """
    if instance.comprovante_matricula:
        file_path = instance.comprovante_matricula.path
        if os.path.isfile(file_path):
            os.remove(file_path)
import os
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from recipes.models import Recipe


def delete_cover(instance):
    try:
        os.remove(instance.cover.path)
    except(ValueError, FileNotFoundError):
        ...

@receiver(pre_delete, sender=Recipe)  # envia um sinal sempre que um uma receita esta prestes a ser deletada rodando a função abaixo
def recipe_cover_delete(sender, instance, *args, **kwargs):
    old_instance = Recipe.objects.get(pk=instance.pk)
    delete_cover(old_instance)


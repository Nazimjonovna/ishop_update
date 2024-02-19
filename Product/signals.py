from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Costs

@receiver(post_save, sender=Costs)
def update_cre_narx(sender, instance, **kwargs):
    pass
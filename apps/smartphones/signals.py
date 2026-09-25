from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Chipset, Smartphone
from apps.recommendation.scoring import calculate_and_save_scores


@receiver(post_save, sender=Smartphone)
def score_new_or_updated_phone(sender, instance, created, **kwargs):
    if getattr(instance, "_skip_score_signal", False):
        return
    instance._skip_score_signal = True
    try:
        calculate_and_save_scores(instance)
    finally:
        instance._skip_score_signal = False


@receiver(post_save, sender=Chipset)
def rescore_phones_on_chipset_update(sender, instance, **kwargs):
    phones = list(instance.smartphones.select_related("chipset").all())
    if phones:
        from apps.recommendation.scoring import calculate_and_save_scores_bulk
        calculate_and_save_scores_bulk(phones)
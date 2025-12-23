"""
Signals for Users app
"""
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, FarmerProfile, FieldOfficerProfile


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Create role-specific profile when user is created"""
    if created:
        if instance.role == 'farmer' and not hasattr(instance, 'farmer_profile'):
            FarmerProfile.objects.get_or_create(
                user=instance,
                defaults={
                    'farm_size': 0,
                    'primary_crop': 'maize'
                }
            )
        elif instance.role == 'field_officer' and not hasattr(instance, 'field_officer_profile'):
            FieldOfficerProfile.objects.get_or_create(
                user=instance,
                defaults={
                    'employee_id': f'FO-{instance.id:06d}'
                }
            )

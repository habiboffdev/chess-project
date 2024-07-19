
from django.db import models
from django.utils import timezone
class BaseManager(models.Manager):
    """
    Our basic manager is used to order all child models of BaseLayer
    to be ordered by created time (descending), therefore it creates a LIFO order,
    causing the recent ones appear first in results.
    """
    use_for_related_fields = True

    def get_queryset(self):
        return super(BaseManager, self).get_queryset().order_by('-created_time')

class BaseLayer(models.Model):
    """
    This layer makes system-wide configurations which tend to be effective for every single model.
    It is used as a parent class for all other models.
    """

    # let's configure managers
    default_manager = BaseManager
    objects = BaseManager()
    all_objects = models.Manager()

    # all models are going to have following two fields
    created_time = models.DateTimeField(default=timezone.now)
    last_updated_time = models.DateTimeField(default=timezone.now)

    @classmethod
    def create(cls, *args, **kwargs):
        now = timezone.now()
        obj = cls(
            *args,
            **kwargs,
            created_time=now,
            last_updated_time=now
        )
        obj.save()
        return obj

    def save(self, *args, **kwargs):
        self.last_updated_time = timezone.now()
        return super(BaseLayer, self).save(*args, **kwargs)

    @classmethod
    def get(cls, *args, **kwargs):
        try:
            return cls.objects.get(*args, **kwargs)
        except cls.DoesNotExist:
            return None

    @classmethod
    def all(cls, *args, **kwargs):
        return cls.objects.all()

    @classmethod
    def filter(cls, *args, **kwargs):
        return cls.objects.filter(*args, **kwargs)

    class Meta:
        abstract = True
    
    
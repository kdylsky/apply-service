from django.db      import models

from core.models    import Region

class User(models.Model):
    name        = models.CharField(max_length=20)
    email       = models.CharField(max_length=50)
    password    = models.CharField(max_length=250)
    regions     = models.ForeignKey(Region, on_delete = models.CASCADE)

    class Meta:
        db_table = "users"
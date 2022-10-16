from django.db          import models

from users.models       import User
from companies.models   import Company

class Supprot_list(models.Model):
    user            = models.ForeignKey(User, on_delete = models.CASCADE)
    recruitment     = models.ForeignKey("Recruitment", on_delete = models.CASCADE)
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)

    class Meta:
        db_table    = "support_lists"

class Recruitment(models.Model):
    company      = models.ForeignKey(Company, on_delete = models.CASCADE)
    money        = models.IntegerField()
    descrtption  = models.TextField()
    position     = models.CharField(max_length = 50) 
    skills       = models.ManyToManyField("Skill", related_name="recruitmentofskill")
    
    class Meta:
        db_table = "recruitments"


class Skill(models.Model):
    name         = models.CharField(max_length = 20)
    
    class Meta:
        db_table = "skills"

from django.db          import models

from users.models       import User
from companies.models   import Company

class Apply(models.Model):
    user            = models.ForeignKey(User, on_delete = models.CASCADE)
    board           = models.ForeignKey("Board", on_delete = models.CASCADE)
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)

    class Meta:
        db_table    = "applies"

class Board(models.Model):
    company      = models.ForeignKey(Company, on_delete = models.CASCADE)
    money        = models.IntegerField()
    descrtption  = models.TextField()
    position     = models.CharField(max_length = 50) 
    skills       = models.ManyToManyField("Skill", related_name="board_of_skills")
    
    class Meta:
        db_table = "boards"


class Skill(models.Model):
    name         = models.CharField(max_length = 20)
    
    class Meta:
        db_table = "skills"

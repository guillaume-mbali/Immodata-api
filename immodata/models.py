from django.db import models

# Create your models here.
class Property(models.Model):

  Date_mutation = models.CharField(max_length=255)
  Annee_mutation = models.CharField(max_length=255)
  Nature_mutation = models.CharField(max_length=255)
  Valeur_fonciere = models.CharField(max_length=255)
  Type_local = models.CharField(max_length=255)
  Price_square_meter = models.CharField(max_length=255)
  Nombre_pieces_principales = models.CharField(max_length=255)
  Surface_reelle_bati = models.CharField(max_length=255)
  Surface_terrain = models.CharField(max_length=255)
  No_voie = models.CharField(max_length=255)
  Voie = models.CharField(max_length=255)
  Code_postal = models.CharField(max_length=255)
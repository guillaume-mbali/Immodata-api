from rest_framework import serializers
from immodata.models import Property

class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = ('id', 'Date_mutation','Annee_mutation','Nature_mutation','Valeur_fonciere','Type_local','Price_square_meter','Nombre_pieces_principales','Surface_reelle_bati','Surface_terrain','No_voie','Voie','Code_postal')
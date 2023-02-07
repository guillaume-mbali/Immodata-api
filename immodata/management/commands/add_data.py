import pandas as pd
from django.core.management.base import BaseCommand
from immodata.models import Property
import datetime
from django.conf import settings
from sqlalchemy import create_engine


class Command(BaseCommand):
  help = "A command to add data from an Excel file to the database"

  def handle(self, *args, **options):

    data=[]
    all_data=[]
    dictionnary = {
        '2019' : 'https://www.data.gouv.fr/fr/datasets/r/3004168d-bec4-44d9-a781-ef16f41856a2',
        '2018' : 'https://www.data.gouv.fr/fr/datasets/r/1be77ca5-dc1b-4e50-af2b-0240147e0346',
        '2017' : 'https://www.data.gouv.fr/fr/datasets/r/7161c9f2-3d91-4caf-afa2-cfe535807f04'
    }

    for year,url in dictionnary.items():
        data = pd.read_csv(url, sep="|")
        data = data.drop(['Reference document','1 Articles CGI','2 Articles CGI','3 Articles CGI','4 Articles CGI','5 Articles CGI','B/T/Q','Prefixe de section','No Volume','1er lot','Surface Carrez du 1er lot','2eme lot','Surface Carrez du 2eme lot','3eme lot','Surface Carrez du 3eme lot','4eme lot','Surface Carrez du 4eme lot','5eme lot','Surface Carrez du 5eme lot','Nature culture','Nature culture speciale'],axis=1)
        all_data.append(data)

    # Création du DataFrame
    df = pd.concat(all_data)


    # Création du DataFrame "Le Mans" (on récupére toutes les ventes sur la commune du Mans)
    df_Le_Mans = df[df['Commune'] =="LE MANS"]

    # Afin d'avoir les données les plus représentatives possibles, je regarde s'il y'a des valeurs nulles dans la colonne "Valeur fonciere"
    df_Le_Mans['Valeur fonciere'].isnull().values.any()

    # Suppression des lignes pour lesquelles la valeur foncière n'est pas renseignée
    df_Le_Mans = df_Le_Mans.dropna(subset=['Valeur fonciere'])

    # Sélection des maisons et appartements
    df_Le_Mans = df_Le_Mans[(df_Le_Mans['Type local'] == 'Maison') | (df_Le_Mans['Type local'] == 'Appartement')]

    # Remplaçement de la virgule par le point
    df_Le_Mans['Valeur fonciere'] = pd.Series(df_Le_Mans['Valeur fonciere']).str.replace(',','.')

    # Changement de typage  pour la colonne "Valeur fonciere" (object -> float)
    df_Le_Mans['Valeur fonciere'] = df_Le_Mans['Valeur fonciere'].astype(float)


    # Je récupére uniquement les ventes comprises entre 30 000 et 1 000 000 d'euros
    df_Le_Mans = df_Le_Mans[(df_Le_Mans['Valeur fonciere'] > 30000) & (df_Le_Mans['Valeur fonciere'] < 1000000)]

    # Création d'une colonne "Annee mutation"
    df_Le_Mans['Annee mutation'] = df_Le_Mans['Date mutation']


    #df_Le_Mans['Annee mutation'] = pd.to_datetime(df_Le_Mans['Annee mutation'])

    #df_Le_Mans['Annee mutation'] = df_Le_Mans['Annee mutation'].dt.strftime('%Y').astype(int)

    # Restructuration du DataFrame
    # columns = ['Date mutation','Annee mutation','Nature mutation','Valeur fonciere','Type local','Nombre pieces principales','Surface reelle bati','Surface terrain','No voie','Voie','Code postal']
    # df_Le_Mans = df_Le_Mans[columns]
    df_Le_Mans.rename(columns={'Date mutation': 'Date_mutation', 'Annee mutation': 'Annee_mutation', 'Nature mutation': 'Nature_mutation', 'Valeur fonciere': 'Valeur_fonciere', 'Type local': 'Type_local', 'Nombre pieces principales': 'Nombre_pieces_principales', 'Surface reelle bati': 'Surface_reelle_bati', 'Surface terrain': 'Surface_terrain', 'No voie': 'No_voie', 'Voie': 'Voie', 'Code postal': 'Code_postal'}, inplace=True)

    # # Création d'une colonne prix au mètre carré
    df_Le_Mans['Price_square_meter'] = df_Le_Mans['Valeur_fonciere'] / df_Le_Mans['Surface_reelle_bati']
    df_Le_Mans['Price_square_meter'] = df_Le_Mans['Price_square_meter'].round()

    # # Changement de typage pour la colonne "Price/square meter" (object -> int)
    df_Le_Mans['Price_square_meter'] = df_Le_Mans['Price_square_meter'].astype(int)

    # # Restructuration du DataFrame
    columns = ['Date_mutation','Annee_mutation','Nature_mutation','Valeur_fonciere','Type_local','Price_square_meter','Nombre_pieces_principales','Surface_reelle_bati','Surface_terrain','No_voie','Voie','Code_postal']
    df_Le_Mans = df_Le_Mans[columns]
    print(df_Le_Mans)


    # user = settings.DATABASES['default']['USER']
    # password = settings.DATABASES['default']['PASSWORD']
    # database_name = settings.DATABASES['default']['NAME']

    # # engine = create_engine('sqlite:///db.sqlite3')
    # database_url = 'mysql://root:root@8000/immodata_bdd'

    # engine = create_engine(database_url, echo=False)

    # df_Le_Mans.to_sql(Property._meta.db_table, if_exists='replace', con=engine, index=False)

    user = 'root'
    password = 'root'
    database_name = 'immo_bdd'

    database_url = 'mysql://{user}:{password}@127.0.0.1:3306/{database_name}'.format(
        user=user,
        password=password,
        database_name=database_name,
        host='/Applications/MAMP/tmp/mysql/mysql.sock'
    )
    # database_url = 'mysql://root:root@localhost:8889/immodata_bdd'

    engine = create_engine(database_url, echo=False)
    df_Le_Mans.to_sql(Property._meta.db_table, con=engine)
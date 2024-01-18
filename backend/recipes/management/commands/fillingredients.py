import csv

from django.core.management.base import BaseCommand
from recipes.models import Ingredient


CSV_PATH = './data/ingredients.csv'


def csv_import(csv_data, model):
    objs = []
    for row in csv_data:
        objs.append(model(**row))
    model.objects.bulk_create(objs)


class Command(BaseCommand):
    help = 'import data from csv files'

    def handle(self, *args, **kwargs):
        with open(
            CSV_PATH,
            newline='',
            encoding='utf8',
        ) as csv_file:
            csv_import(csv.DictReader(csv_file), Ingredient)

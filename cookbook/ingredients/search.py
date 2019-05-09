from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import (Document, Text, Date)
from django.apps import apps
import json
from elasticsearch import Elasticsearch
from django.core import serializers

from cookbook.ingredients import models
connections.create_connection()


class CategoryIndex(Document):
    
    name = Text()
    timestamp = Date()

    class Index:
        name = 'category-index'

    def save(self, **kwargs):
            # assign now if no timestamp given
        obj = CategoryIndex(
            _meta={'id': self.id, 'index': 'category-index'},
            name=self.name)
        index_document(document=obj, model_name='category')

        # override the index to go to Ethe proper timeslot
        kwargs['index'] = 'category-index'
        return super().save(**kwargs)


class IngredientIndex(Document):

    name = Text()
    category = Text()

    class Index:
        name = 'ingredient-index'

    def save(self, **kwargs):
        # override the index to go to the proper timeslot
        kwargs['index'] = 'ingredient-index'
        return super().save(**kwargs)


def bulk_indexing():
    # es.indices.create(index='category-index', ignore=400)
    # es.indices.create(index='ingredient-index', ignore=400)
    if not CategoryIndex._index.exists():
        CategoryIndex.init()

    if not IngredientIndex._index.exists():
        IngredientIndex.init()

    # index_object(models.Category.objects.all().iterator())
    index_models()
    # for b in models.Category.objects.all().iterator():
    #     index_object(b)
    #     es.index(body=b)

    # for b in models.Ingredient.objects.all().iterator():
    #     index_object(b)

    # categories = CategoryIndex._index.as_template('category-index')
    # categories.save()

    # ingredients = IngredientIndex._index.as_template('ingredients-index')
    # ingredients.save()

    # index_object(models.Category.objects.all().iterator()))
    # bulk(client=es, 
    # actions=index_object(models.Ingredient.objects.all().iterator()))

def index_object(b):

    return b.indexing()
        
def index_models():

    es = Elasticsearch()

    indexing_models = apps.get_app_config('ingredients').get_models()
    
    for model in indexing_models:

        for b in model.objects.all():
            data = serializers.serialize('json', [b,])
            struct = json.loads(data)
            data = json.dumps(struct[0])
            es.index(index=f'{model.__name__.lower()}-index',doc_type=f'{model.__name__.lower()}', id=b.id, body=data)

def index_document(document, model_name):
    
    es = Elasticsearch()
    # data = serializers.serialize('json', document)
    # struct = json.loads(data)
    # data = json.dumps(struct[0])
    es.index(index=f'{model_name.lower()}-index',doc_type=f'{model_name.lower()}', id=document._id, body=document)
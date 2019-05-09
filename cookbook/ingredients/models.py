from django.db import models
from cookbook.ingredients.search import CategoryIndex, IngredientIndex, index_document

class Category(models.Model):

    name = models.CharField(max_length=100)

    def indexing(self):

        obj = CategoryIndex(
            meta = {'_id': self.id, 'index': 'category-index'},
            name=self.name)

        return obj.to_dict(include_meta=True)

    def __str__(self):
    
        return self.name

    def indexing(self):
        
        obj = CategoryIndex(
            meta = {'_id': self.id, 'index': 'category-index'},
            name=self.name
            )
        obj.save()
        return obj.to_dict(include_meta=True)



class Ingredient(models.Model):

    name = models.CharField(max_length=100)
    notes = models.TextField()
    category = models.ForeignKey(
        Category, 
        related_name="ingredients", 
        on_delete=models.CASCADE
    )

    def __str__(self):

        return self.name

    def indexing(self):
    
        obj = IngredientIndex(
            meta = {'_id': self.id, 'index': 'ingredient-index'},
            name=self.name,
            category=self.category.name, 
            )
        obj.save()
        return obj.to_dict(include_meta=True)

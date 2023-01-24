from django.db import models


class Phone(models.Model):
    name = models.CharField(max_length=50)
    price = models.PositiveIntegerField()
    image = models.URLField(max_length=100)
    release_date = models.DateField(max_length=50)
    lte_exists = models.BooleanField()
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return f'{self.id}, {self.name}, {self.price}, {self.image}, {self.release_date}, {self.lte_exists}, {self.slug}'


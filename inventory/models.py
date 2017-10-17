from django.db import models
from datetime import date

PRODUCT_GRADES = (
    (5, 'A+'),
    (4.7, 'A'),
    (4.3, 'A-'),
    (4, 'B+'),
    (3.7, 'B'),
    (3.3, 'B-'),
    (3, 'C'),
    (2, 'D'),
    (1, 'F')
)

CATEGORIES = (
    ('base', 'Base'),
    ('eyes', 'Eyes'),
    ('brow', 'Brows'),
    ('lip', 'Lips'),
    ('chk', 'Cheeks'),
    ('sc', 'Skincare'),
    ('tool', 'Tools'),
    ('etc', 'Other')
)

class Brand(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class Type(models.Model):
    category = models.CharField(choices=CATEGORIES, max_length=50, default='base')

    def __str__(self):
        return dict(CATEGORIES)[self.category]

    def not_tool(self):
        return self.category != 'tool'

class Product(models.Model):
    MEASUREMENT = (
        ('g', 'g'),
        ('mL', 'mL'),
        ('oz', 'oz')
    )

    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, blank=True, null=True)
    use = models.ForeignKey(Type, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=50)
    shade = models.CharField(max_length=50, blank=True, null=True)
    date_obtained = models.DateField('Date Obtained', default=date.today)
    amount = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    unit = models.CharField(choices=MEASUREMENT, max_length=2, blank=True, null=True)
    rating = models.IntegerField(choices=PRODUCT_GRADES)
    notes = models.TextField(blank=True, null=True)
    def __str__(self):
        if self.shade:
            return self.brand.name+" "+self.name+" in "+self.shade
        else:
            return self.brand.name+" "+self.name

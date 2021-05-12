from django.db import models


class Category(models.Model):
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=255)
    image = models.ForeignKey('Image', null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    class Meta:
        verbose_name = 'Sub Category'
        verbose_name_plural = 'Sub Categories'

    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL, related_name='sub_categories')

    def __str__(self):
        return "{}".format(self.name)


class Image(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='media/')

    def __str__(self):
        return self.name


class Characteristic(models.Model):
    brand = models.CharField(max_length=255)
    weight = models.DecimalField(max_digits=20, decimal_places=2)
    description = models.TextField()
    packaging = models.CharField(max_length=255)
    manufacturer = models.CharField(max_length=255)

    def __str__(self):
        return self.brand


class Product(models.Model):
    class Meta:
        app_label = 'products'
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    TYPE = (
        (1, 'KG'),
        (2, 'UNITS')
    )

    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)
    sub_category = models.ForeignKey(SubCategory, null=True, on_delete=models.SET_NULL)
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    active = models.BooleanField()
    type = models.IntegerField(choices=TYPE)
    barcode = models.IntegerField()
    image = models.ManyToManyField(Image, null=True)
    characteristic = models.OneToOneField(Characteristic, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

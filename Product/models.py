from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum, Avg, Count

# Create your models here.


from django.utils.safestring import mark_safe


class Category(models.Model):
    status = (
        ('True', 'True'),
        ('False', 'False'),
    )
    parent = models.ForeignKey('self', related_name='children', blank=True, null=True, on_delete=models.CASCADE)
    title = models.CharField( max_length=200)
    keywords = models.CharField( max_length=200)
    image = models.ImageField(upload_to='category/', blank=True)
    status = models.CharField(max_length=50, choices=status)
    slug = models.SlugField(null=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Company(models.Model):
    status = (
        ('True', 'True'),
        ('False', 'False'),
    )
    catgory = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, blank=True, null=True)
    status = models.CharField(max_length=50, choices=status)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Product(models.Model):
    status = (
        ('True', 'True'),
        ('False', 'False'),
    )
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField( max_length=200)
    keywords = models.CharField( max_length=200)
    image = models.ImageField(upload_to='product/', blank=True)
    new_price = models.DecimalField(max_digits=15, decimal_places=2)
    old_price = models.DecimalField(max_digits=15, decimal_places=2)
    amount = models.IntegerField(default=0)
    min_amount = models.IntegerField(default=3)
    detail = models.TextField()
    status = models.CharField(max_length=50, choices=status)
    slug = models.SlugField(null=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def image_tag(self):
        return mark_safe('<img src="{}" height="70" width="60" />'.format(self.image.url))
    image_tag.short_description = 'Image'


    def average_review(self):
        reviews = Comment.objects.filter(product=self, status=True).aggregate(average = Avg('rate'))
        avg=0
        if reviews['average'] is not None:
            avg = float(reviews['average'])
            return avg
        else:
            return avg

    def total_review(self):
        reviews = Comment.objects.filter(product=self, status=True).aggregate(count = Count('id'))
        cnt = 0
        if reviews['count'] is not None:
            cnt = float(reviews['count'])
            return cnt
        else:
            return cnt
    
    def imageurl(self):
        if self.image:
            return self.image.url
        else:
            return ""
            
    def get_absolute_url(self):
        return reverse("product_element", kwargs={"slug": self.slug})
    


class Images(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    title = models.CharField( max_length=200)
    image = models.ImageField(upload_to='product/', blank=True)
    def __str__(self):
        return self.title

    def imageurl(self):
        if self.image:
            return self.image.url
        else:
            return ""
  


class Comment(models.Model):
    status = (
        ('New', 'New'),
        ('True', 'True'),
        ('False', 'False'),
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField( max_length=200, blank=True)
    comment = models.CharField( max_length=500, blank=True)
    rate = models.IntegerField(default=1)
    ip = models.CharField( max_length=200, blank=True)
    status = models.CharField(max_length=50, choices=status, default = True )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject

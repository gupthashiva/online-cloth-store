from django.db import models
from ckeditor.fields import RichTextField
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.contrib.auth.models import User
from django.urls import reverse
import datetime

# Create your models here.


DISCOUNT_DEAL = (
  ('HOT DEAL', 'HOT DEAL'),
  ('NEW ARRAIVELS', 'NEW ARRAIVELS'),
 )


class Slider(models.Model):
  Image = models.ImageField(upload_to='slider_imgs/')
  Discount_Deal = models.CharField(choices=DISCOUNT_DEAL,max_length=100)
  Sale = models.IntegerField()
  Brand_Name = models.CharField(max_length=200)
  Discount = models.IntegerField()
  Link = models.CharField(max_length=200)
  
  
  def __str__(self):
      return str(self.Brand_Name)  
    
class Banner_Area(models.Model):
  Image = models.ImageField(upload_to='slider_imgs/')
  Discount_Deal = models.CharField(max_length=100)
  Quote = models.CharField(max_length=100)
  Discount = models.IntegerField()
  Link = models.CharField(max_length=200 , null=True)
  def __str__(self):
      return str(self.Quote)  
    
class Main_Category(models.Model):
  name = models.CharField(max_length=100)
  
  def __str__(self):
    return str(self.name)

class Category(models.Model):
  main_category = models.ForeignKey(Main_Category, on_delete=models.CASCADE)
  name = models.CharField(max_length=100)
  
  def __str__(self):
    return str(self.name) + '--'+ self.main_category.name
   
class Sub_Category(models.Model):
  category = models.ForeignKey(Category, on_delete=models.CASCADE)
  name = models.CharField(max_length=100)
    
  def __str__(self):
      return str(self.category.main_category.name) +'--'+self.category.name + '--'+ self.name

class Section(models.Model):
  name = models.CharField(max_length=100)
  
  def __str__(self):
     return str(self.name)

class Color(models.Model):
  code = models.CharField(max_length=100)
  
  def __str__(self):
        return self.code
    
class Brand(models.Model):
  name = models.CharField(max_length=100)
   
  def __str__(self):
    return self.name
  
class Product(models.Model):
  total_quantity = models.IntegerField()
  availability= models.IntegerField()
  featured_Image = models.CharField(max_length=100)
  product_name = models.CharField(max_length=100)
  brand = models.ForeignKey(Brand, on_delete=models.CASCADE, null=True)
  price = models.IntegerField()
  discount = models.IntegerField()
  product_information = RichTextField()
  model_name = models.CharField(max_length=100)
  categories = models.ForeignKey(Category, on_delete=models.CASCADE)
  color = models.ForeignKey(Color, on_delete=models.CASCADE, null=True)
  tags = models.CharField(max_length=100)
  description = RichTextField()
  section = models.ForeignKey(Section, on_delete=models.CASCADE)
  slug = models.SlugField(default='', max_length=500, null=True, blank=True)
  quantity = models.PositiveIntegerField(default=1)
  tax=models.IntegerField(null=True)
  packing_cost=models.IntegerField(null=True)
  
  
  def __str__(self):
    return str(self.product_name)
  

  @staticmethod
  def get_products_by_id(ids):
    return Product.objects.filter(id__in =ids)

  @staticmethod
  def get_all_products():
    return Product.objects.all()

  def get_absolute_url(self):
        return reverse("product_detail", kwargs={'slug': self.slug})

  class Meta:
    db_table = "app_Product"

def create_slug(instance, new_slug=None):
    slug = slugify(instance.product_name)
    if new_slug is not None:
        slug = new_slug
    qs = Product.objects.filter(slug=slug).order_by('-id')
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" % (slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug

def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

pre_save.connect(pre_save_post_receiver, Product)

class Product_Image(models.Model):
  product = models.ForeignKey(Product, on_delete=models.CASCADE)
  Image_url = models.CharField(max_length=100)
  
  def __str__(self):
    return str(self.product)
  
class Additional_Information(models.Model):
  product = models.ForeignKey(Product, on_delete=models.CASCADE)
  specification = models.CharField(max_length=100)
  detail = models.CharField(max_length=100)

  def __str__(self):
    return str(self.product)
  

  
#add to cart functionalitya
    
@staticmethod
def get_customer_by_email(email):
    try:
        return User.objects.get(email=email)
    except:
        return False
      
def isExists(self):
    if User.objects.filter(email = self.email):
        return True

    return  False 
     
class Order(models.Model):
  product=models.ForeignKey(Product, on_delete=models.CASCADE)
  customer=models.ForeignKey(User, on_delete=models.CASCADE)
  quantity=models.IntegerField(default=1)
  price=models.IntegerField()
  address=models.CharField(max_length=100,default='1', blank=True)
  phone=models.CharField(max_length=100,default='', blank=True)
  date=models.DateField(default=datetime.datetime.today)
  status=models.BooleanField(default=False)
  
  def __str__(self):
    return str(self.customer)
  
  def Place_Order(self):
        self.save()
  
  @staticmethod
  def get_orders_by_cutomer(customer_id):
    return Order.objects.filter(customer=customer_id).order_by('-date')
  
class Payment_Get_Way(models.Model):
  name = models.CharField(max_length=100)
  amount = models.CharField(max_length=100)
  order_id = models.CharField(max_length=100, blank=True)
  razorpay_payment_id = models.CharField(max_length=100, blank=True)
  paid = models.BooleanField(default=1)

  
  def __str__(self):
    return str(self.name)
  
  
  
  
  
  
  
  
  
'''
#coupon model

class Coupon(models.Model):
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    coupon_code = models.CharField(max_length=10)
    is_expired =models.BooleanField(default=False)
    discount_price =models.IntegerField(default=100)
    minimum_amount =models.IntegerField(default=500)
    
    

    def __str__(self):
      return str(self.coupon_code)
  
class Coupon_Code(models.Model):
  product=models.ForeignKey(Product, on_delete=models.CASCADE)
  coupon_code = models.CharField(max_length=6)
  is_expired =models.BooleanField(default=False)
  discount_price =models.IntegerField(default=0)
  minimum_amount =models.IntegerField(default=500)

  def __str__(self):
      return str(self.coupon_code)
'''  




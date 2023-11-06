from django.contrib.auth import get_user_model
from django.conf import settings
import json
from django.db.models.signals import post_save,pre_delete,pre_save
from django.dispatch import receiver
from django.core.mail import send_mail
from email.message import EmailMessage
from django.contrib import messages
import ssl
import random
import smtplib
from django.urls import reverse
from django.db import models

User = get_user_model()

class Category(models.Model):
    name = models.CharField(max_length=50,unique=True)
    class Meta:
        verbose_name = ("Category")
        verbose_name_plural = ("Categories")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Category_detail", kwargs={"pk": self.pk})



class Product(models.Model):
    title = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.IntegerField()
    image = models.ImageField()
    description = models.TextField()
    new_product = models.BooleanField(default=True)
    date = models.DateTimeField(auto_now=True)


    class Meta:
        ordering = ['date']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('products:product_detail', kwargs={'pk':self.pk})


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    destination = models.CharField(max_length=200)
    paid = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    @property
    def total_amount(self):
        return sum([item.total_amount for item in self.orderitem_set.all()])

    def __str__(self):
        return f"{self.user} {self.created.date()}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    @property
    def total_amount(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.product} x{self.quantity}"

class Stock(models.Model):
    title = models.CharField(max_length=50,unique=True)
    quantity = models.PositiveIntegerField(default=1)
    threshold = models.PositiveIntegerField(default=1)
    reorder = models.BooleanField(default=False)

    def save_model(self,request,obj,form,change):
        obj.save()
        messages.add_message(request,messages.DANGER,'stock level is low , please reorder')

    class Meta:
        verbose_name = ("Stock")
        verbose_name_plural = ("Stocks")

    def __str__(self):
        return self.title



class StockItem(models.Model):
    item = models.ForeignKey(Stock, on_delete=models.CASCADE)
    req = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    class Meta:
        verbose_name = ("StockRequest")
        verbose_name_plural = ("StockRequests")


class OrderCount(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    orders = models.IntegerField(default=0)
    coupon = models.IntegerField(default=0)


@receiver(post_save, sender=OrderCount)
def send_coupon(sender,instance=None,created=False,**kwargs):
    if created:
        #generate coupon
        count = OrderCount.objects.filter(pk=instance.pk).count()
        order = OrderCount.objects.get(pk=instance.pk)
        if count > 5:
            coupon = random.random(1,10)
            order.coupon = coupon
            order.save()

            #send email
            resp = OrderCount.objects.filter(user=instance.user)
            sender_email = settings.EMAIL_HOST_USER
            password = settings.EMAIL_HOST_PASSWORD
            subject = "Coupon"
            body = f"Hello our happy client , you have been rewarded a coupon  {coupon}"
            em = EmailMessage()
            em['From'] = sender_email
            em['To'] = instance.user.email
            em['Subject'] = subject
            em.set_content(body)

            context = ssl.create_default_context()

            with smtplib.SMTP_SSL('smtp.gmail.com',465,context=context) as smtp:
                smtp.login(sender_email, password)
                smtp.sendmail(sender_email,instance.user, em.as_string())
        else:
            pass


@receiver(pre_save, sender=StockItem)
def is_available(sender,instance,*args, **kwargs):
    stock = Stock.objects.get(pk=instance.item.pk)
    print(stock.quantity)
    if stock.quantity >= stock.threshold and instance.quantity <= stock.quantity:
        stock.quantity = stock.quantity - instance.quantity
        stock.save()
    else:
        stock.reorder = True
        stock.save()

pre_save.connect(is_available,sender=StockItem)


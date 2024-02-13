from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class products(models.Model):
    pname = models.CharField(max_length = 40)
    pbrand = models.CharField(max_length = 40)
    price = models.IntegerField()
    discount = models.IntegerField()
    image = models.ImageField(upload_to='image')
    category = models.CharField(max_length = 40)
    description = models.CharField(max_length=200, default='ab')
    totalsells = models.IntegerField(default=1)
    @property
    def disprice(self):
        """
        Computed property to calculate the discounted price.
        """
        discount_amount = (self.discount / 100) * self.price
        disprice = self.price - discount_amount
        return int(disprice)



class cart(models.Model):
    pid=models.ForeignKey(products, on_delete=models.CASCADE, db_column='empid')
    uid=models.ForeignKey(User, on_delete=models.CASCADE, db_column='userid')
    quantity = models.IntegerField(default=1)


class userextrainfo(models.Model):
    uid = models.ForeignKey(User, on_delete=models.CASCADE, db_column='uid')
    address = models.CharField(max_length = 200)
    phonenum = models.CharField(max_length = 10)
    profilepic = models.ImageField(upload_to='image')

class orders(models.Model):
    orderid = models.IntegerField()
    uid = models.ForeignKey(User, on_delete=models.CASCADE, db_column='userid')
    pid = models.ForeignKey(products, on_delete=models.CASCADE, db_column='pid')
    quantity = models.IntegerField()

class wishlist(models.Model):
    pid=models.ForeignKey(products, on_delete=models.CASCADE, db_column='empid')
    uid=models.ForeignKey(User, on_delete=models.CASCADE, db_column='userid')


class history(models.Model):
    orderid = models.IntegerField()
    uid = models.ForeignKey(User, on_delete=models.CASCADE, db_column='userid')
    pid = models.ForeignKey(products, on_delete=models.CASCADE, db_column='pid')
    quantity = models.IntegerField()


class RegistrationData(models.Model):
    fname = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=100)
    otp = models.CharField(max_length=6)


# for contact page
class ContactPage(models.Model):
    uid = models.ForeignKey(User, on_delete=models.CASCADE, db_column='userid')
    messege = models.CharField(max_length=400)
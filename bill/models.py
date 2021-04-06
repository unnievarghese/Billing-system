from django.db import models

class product(models.Model):
    product_name=models.CharField(max_length=150,unique=True)

    def __str__(self):
        return self.product_name

class purchase(models.Model):
    product=models.ForeignKey(product,on_delete=models.CASCADE)
    quantity=models.IntegerField(null=False)
    purchase_price=models.FloatField(null=False)
    selling_price=models.FloatField(null=False)
    purchase_date=models.DateField(auto_now=True)

    def __str__(self):
        return str(self.quantity)

class order(models.Model):
    bill_number=models.CharField(max_length=12,unique=True)
    bill_date=models.DateField(auto_now=True)
    customer_name=models.CharField(max_length=60)
    phone_number=models.CharField(max_length=12)
    bill_total=models.IntegerField(default=50)

    def __str__(self):
        return str(self.bill_number)

class ordelines(models.Model):
    bill_number=models.ForeignKey(order,on_delete=models.CASCADE)
    product_name=models.ForeignKey(product,on_delete=models.CASCADE)
    product_qty=models.FloatField()
    amount=models.FloatField()

    def __str__(self):
        return str(self.bill_number)
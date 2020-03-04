

# Create your models here.
stat=(
    ("Active","Active"),
    ("Inactive","Inactive")
)

class Restaurant(models.Model):
    name=models.CharField(max_length=100,blank=False,null=False)
    address=models.CharField(max_length=200,blank=False,null=False)
    lat = models.CharField(max_length=31, null=True)
    long = models.CharField(max_length=31, null=True)
    status = models.CharField(max_length=11,choices=stat,default="Active")
    #


class Menu(models.Model):
    name=models.CharField(max_length=100,blank=False,null=False)
    course=models.CharField(max_length=50,blank=False,null=False)
    price=models.CharField(max_length=10,blank=False,null=False)
    description=models.CharField(max_length=200,blank=False,null=False)
    restaurant=models.ForeignKey(Restaurant, blank=False, null=False, on_delete=models.CASCADE,
                             default=1)

class Tables(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    restaurant = models.ForeignKey(Restaurant, blank=False, null=False, on_delete=models.CASCADE,
                                   default=1)
    availability_status = models.BooleanField(default=True)

class User(models.Model):
    username = models.CharField(max_length=61, blank=True, null=True)
    password = models.CharField(max_length=50, null=True, blank=True)
    email = models.CharField(max_length=50, null=True, blank=True)
    phone_number = models.CharField(unique=True, null=True, blank=True, max_length=17)

amount_status= (

    ("Success", "Success"),
    ("Failed","Failed"))
class Booking(models.Model):
    user = models.ForeignKey(User, max_length=11, on_delete=models.CASCADE, blank=False, null=False)
    table = models.ForeignKey(Tables, max_length=11,related_name='booking_table', on_delete=models.CASCADE, blank=False, null=False)
    menu = models.ForeignKey(Tables, max_length=11, related_name='booking_menu', on_delete=models.CASCADE, blank=False, null=False)
    total=models.CharField(max_length=50, null=True, blank=True)
    paid_amount = models.CharField(max_length=31, null=True)
    payment_id=models.CharField(max_length=50, null=True, blank=True)
    payment_status = models.CharField(max_length=11,choices=amount_status,default="Success")
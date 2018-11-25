from django.db import models
from django.db.models.signals import pre_save
from django.conf import settings
from django.utils.text import slugify
from django.urls import reverse
from transliterate import translit


def pre_save_tour_category_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(translit(str(instance.name), reversed=True))


# table TourCategory
class TourCategory(models.Model):
    name = models.CharField(max_length=30)
    slug = models.SlugField(unique=True, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'category_slug': self.slug})


pre_save.connect(pre_save_tour_category_slug, sender=TourCategory)


def image_upload_path(instance, filename):
    filename = instance.slug + '.' + filename.split('.')[-1]
    return '{0}/{1}/{2}'.format(instance.__class__.__name__.lower(), instance.slug, filename)


# # make checkbox "available" in Tour working
# class TourManager(models.Manager):
#     def all(self, *args, **kwargs):
#         return super(TourManager, self).get_queryset().filter(available=True)


# table Tour
class Tour(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    image = models.ImageField(upload_to=image_upload_path)
    price = models.DecimalField(max_digits=17, decimal_places=5)
    available = models.BooleanField(default=True)
    category = models.ForeignKey(
        TourCategory,
        related_name='tours',
        on_delete=models.CASCADE
    )
    # objects = TourManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('tour_detail', kwargs={'tour_slug': self.slug})


class Cart(models.Model):
    items = models.ManyToManyField(Tour, blank=True)
    cart_total = models.DecimalField(max_digits=30, decimal_places=5, default=0)

    def __str__(self):
        return str(self.id)

    def add_to_cart(self, tour_slug):
        cart = self
        tour = Tour.objects.get(slug=tour_slug)
        if tour not in cart.items.all():
            cart.items.add(tour)
            cart.save()

    def remove_from_cart(self, tour_slug):
        cart = self
        tour = Tour.objects.get(slug=tour_slug)
        for cart_tour in cart.items.all():
            if cart_tour == tour:
                cart.items.remove(tour)
                cart.save()

    def update_total_price(self):
        cart = self
        cart_total = 0.0
        for item in cart.items.all():
            cart_total += float(item.price)
        cart.cart_total = cart_total
        cart.save()


ORDER_STATUS_CHOICES = (
    ('Received', 'Received'),
    ('In progress', 'In progress'),
    ('Paid', 'Paid'),
)


class Order(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    tours = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE
    )
    total_price = models.DecimalField(max_digits=30, decimal_places=5, default=0)
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(blank=True)
    status = models.CharField(max_length=120, choices=ORDER_STATUS_CHOICES, default=ORDER_STATUS_CHOICES[0][0])

    def __str__(self):
        return 'Order number: {0}'.format(str(self.id))

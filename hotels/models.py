from django.db import models

class MenuItem(models.Model):
    CATEGORY_CHOICES = [
        ("starter", "Starters"),
        ("main", "Main Course"),
        ("dessert", "Desserts"),
        ("beverage", "Beverages"),
    ]

    name = models.CharField(max_length=120)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default="main")
    short_description = models.CharField(max_length=200)
    full_description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    emoji = models.CharField(max_length=8, default="🍽️", help_text="Emoji used as the dish visual")
    image = models.ImageField(upload_to="menu/", blank=True, null=True)
    prep_time_minutes = models.PositiveIntegerField(default=20)
    spice_level = models.CharField(
        max_length=20,
        choices=[("mild", "Mild"), ("medium", "Medium"), ("hot", "Hot"), ("none", "N/A")],
        default="mild",
    )
    is_chef_special = models.BooleanField(default=False)

    class Meta:
        ordering = ["category", "name"]

    def __str__(self):
        return self.name


class Order(models.Model):
    item = models.ForeignKey(MenuItem, on_delete=models.CASCADE, related_name="orders")
    placed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.pk} - {self.item.name}"


class ContactMessage(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField()
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} <{self.email}>"
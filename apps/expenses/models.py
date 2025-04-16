from django.db import models

from apps.accounts.models import User
from apps.common.models import BaseModel

from autoslug import AutoSlugField


def slugify_name(self):
    return f"{self.name}"

class Category(BaseModel):
    name=models.CharField(max_length=30)
    slug  = AutoSlugField(populate_from=slugify_name, null=True, blank=True, always_update=True, unique=True)
    limit = models.DecimalField(max_digits=20, decimal_places=2,default="00.00")
    owner = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Expense(BaseModel):
    category = models.ForeignKey(Category, models.CASCADE, default=1, related_name="expenses")
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    description = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.description[:50]
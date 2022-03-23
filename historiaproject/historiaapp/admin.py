from django.contrib import admin
from .models import *

# Register your models here.
# The goal is tu update or access database
# from the admin panel. If you do not have
# a superuser yet, you need to create one.

admin.site.register(Card)
admin.site.register(Quiz)

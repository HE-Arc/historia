from django.contrib import admin
from .models import *

# Register ours models here to access database from the admin panel.
# Create a superuser to access the database.

admin.site.register(Card)
admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Ranking)
admin.site.register(Category)
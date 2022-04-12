################################################################################
#                                                                              #
# Description : This file contains all models available in the admin panel     #
# Authors     : Simon Meier, Alex Mozerski and Yasmine Margueron               #
# Date        : 14.04.2022                                                     #
#                                                                              #
################################################################################

from django.contrib import admin
from .models import *

# Register ours models here to access database from the admin panel.
# Create a superuser to access the database.

admin.site.register(Card)
admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Ranking)
admin.site.register(Category)
from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'email', 'ip', 'date_added', 'date_uploaded')
    readonly_fields = ["date_added", "date_uploaded"]


admin.site.register(Customer, CustomerAdmin)
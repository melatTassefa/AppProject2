from django.contrib import admin
from .models import AboutUs,Home,CustomUser, College_List, College_Requirements, College_Fields
# Register your models here.

admin.site.register(AboutUs)
admin.site.register(Home)
admin.site.register(CustomUser)
admin.site.register(College_List)
admin.site.register(College_Requirements)
admin.site.register(College_Fields)

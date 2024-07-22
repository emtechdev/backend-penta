from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(AdminProfile)
admin.site.register(DoctorProfile)
admin.site.register(StaffProfile)
admin.site.register(Room)
admin.site.register(Task)
admin.site.register(Assign)
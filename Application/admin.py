from django.contrib import admin
from Application.models import User, Leave

# Register your models here.

class User_Admin(admin.ModelAdmin):
    list_display = ['UID','Name','Role','Password','Total_Leave','Created_Date']

    class Meta:
        model = User

class Leave_Admin(admin.ModelAdmin):
    list_display = ['LID','UID','Start_Date','End_Date','Description','Leave_Status','Seen_By_Manager','Created_Date']

    class Meta:
        model = Leave

admin.site.register(User, User_Admin)
admin.site.register(Leave, Leave_Admin)
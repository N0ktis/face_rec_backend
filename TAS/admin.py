from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Register your models here.
#from .forms import AddUserForm, ChangeUserForm
from .models import User, TimeTracking, Device, Department


"""class AdminUser(UserAdmin):
    add_form = AddUserForm
    form = ChangeUserForm
    model = User
    inlines = (User,)
    list_display = ['email', 'full_name', ]"""


admin.site.register(User)
admin.site.register(TimeTracking)
admin.site.register(Department)
admin.site.register(Device)

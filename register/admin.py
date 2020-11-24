from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


from .forms import UserAdminCreationForm, UserAdminChangeForm
from .models import User


class UserAdmin(BaseUserAdmin):
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    list_display = ('username', 'email', 'admin',
                    'active', 'password_expiration')
    list_filter = ('admin', 'active')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal info', {
         'fields': ('first_name', 'last_name', 'date_of_birth', 'address', 'zip_code', 'city', 'state')}),
        ('Permissions', {'fields': ('admin', 'active', 'user_type')}),
        ('Dates', {'fields': ('password_expiration',
                              'deactive_time_start', 'deactive_time_end')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(User, UserAdmin)

admin.site.unregister(Group)

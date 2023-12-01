from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext, gettext_lazy as _
from .models import Permission, User

import django
django.utils.translation.ugettext = gettext


class PermissionAdmin(admin.ModelAdmin):
    list_display = ('id', 'code', 'name',)
    list_editable = ('code', 'name',)
    ordering = ['name']

admin.site.register(Permission, PermissionAdmin)


class MyUserAdmin(UserAdmin):
	def get_queryset(self, request):
		qs = super(UserAdmin, self).get_queryset(request)
		if not request.user.is_superuser:
			return qs.filter(is_superuser=False)
		return qs

	def get_fieldsets(self, request, obj=None):
		if not obj:
			return self.add_fieldsets
		
		if request.user.is_superuser:
			perm_fields = ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')

			return [(None, {'fields': ('username', 'password',)}),
				(_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'permission')}),
				(_('Permissions'), {'fields': perm_fields}),
				(_('Important dates'), {'fields': ('last_login', 'date_joined')})]
		else:
			perm_fields = ('is_active', 'is_staff')

			return [(None, {'fields': ('username', 'password',)}),
				(_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
				(_('Permissions'), {'fields': perm_fields})]
				
admin.site.register(User, MyUserAdmin)

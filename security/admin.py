from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Permission

from django.utils.translation import gettext, gettext_lazy as _
from .models import User, Menu, UserMenus

import django
django.utils.translation.ugettext = gettext
# --------------------------------------------------------------------------------------------------
class PermissionAdmin(admin.ModelAdmin):
	list_display = ('id', 'name', 'content_type', 'codename', 'menu')
	list_editable = ('name', 'content_type', 'codename', 'menu')
	list_filter = ['menu', 'content_type']

admin.site.register(Permission, PermissionAdmin)
# --------------------------------------------------------------------------------------------------
class MenuAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'url', 'menu_padre', 'is_link')
    list_editable = ('name', 'url', 'is_link')

admin.site.register(Menu, MenuAdmin)
# --------------------------------------------------------------------------------------------------
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
				(_('Personal info'), {'fields': ('first_name', 'last_name', 'email',)}),
				(_('Permissions'), {'fields': perm_fields}),
				(_('Important dates'), {'fields': ('last_login', 'date_joined')})]
		else:
			perm_fields = ('is_active', 'is_staff')

			return [(None, {'fields': ('username', 'password',)}),
				(_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
				(_('Permissions'), {'fields': perm_fields})]
				
admin.site.register(User, MyUserAdmin)
# --------------------------------------------------------------------------------------------------
admin.site.register(UserMenus)

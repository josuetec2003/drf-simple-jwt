from django.db import models
from django.contrib.auth.models import Permission as AuthPermission
from django.contrib.auth.models import AbstractUser

# Este modelo ya no va ------------------------------------------------------------------------------------
class Permission(models.Model):
    code = models.CharField(max_length=3)
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name
# ---------------------------------------------------------------------------------------------------------
class User(AbstractUser):
	permission = models.ManyToManyField(Permission, blank=True)

# ---------------------------------------------------------------------------------------------------------
class Menu(models.Model):
    name = models.CharField(max_length=20)
    url = models.CharField(max_length=100, null=True, blank=True)
    menu_padre = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    is_link = models.BooleanField(default=True)
    # icon

    def __str__(self):
        if self.menu_padre:
            return f'{self.menu_padre} / {self.name}'
        else:
            return self.name

# ---------------------------------------------------------------------------------------------------------
if not hasattr(AuthPermission, 'menu'):
    application_id = models.ForeignKey(Menu, db_column='menu', on_delete=models.CASCADE, blank=True, null=True)
    application_id.contribute_to_class(AuthPermission, 'menu')

# ---------------------------------------------------------------------------------------------------------
class UserMenus(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} - {f"{self.menu.menu_padre} /" if self.menu.menu_padre else ""} {self.menu.name}'





from django.contrib.auth import get_user_model

from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.state import token_backend
from security.models import Menu, UserMenus

'''
Función recursiva para generar toda la jerarquía de menús desde el hijo
hasta el último padre y almacenarla en el modelo UserMenus.
Este modelo es de apoyo para generar la estructura de menús al que tendrá
acceso el usuario.
'''
def add_parents(menu, user):
    if menu:
        if not UserMenus.objects.filter(user=user, menu=menu).exists():
            UserMenus.objects.create(user=user, menu=menu)

        add_parents(menu.menu_padre, user)
    else:
        return None

'''
Función recursiva para construir la estructura de menús desde los padres
hasta los últimos hijos de forma aninada. También agrega las acciones a las
que tiene permiso el usuario en cada menú.
'''
def build_menu(menus, user, perms):
    nodes = []
    for menu in menus:
        if UserMenus.objects.filter(user=user, menu=menu).exists():
            temp_menu = {}
            temp_menu['id'] = menu.id
            temp_menu['name'] = menu.name
            temp_menu['url'] = menu.url
            temp_menu['children'] = build_menu(menu.menu_set.all(), user, perms)
            temp_menu['actions'] = []

            for perm in perms:
                if perm.menu.id == menu.id:
                    temp_menu['actions'].append(perm.codename)

            nodes.append(temp_menu)
    
    return nodes


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    default_error_messages = {
        'no_active_account': 'Username or Password does not matched.'
    }

    def validate(self, attrs):
        # data contiene el access y refresh token
        data = super(MyTokenObtainPairSerializer, self).validate(attrs)
        
        # Obtener los permisos individuales
        perms = [p for p in self.user.user_permissions.all()]

        # Obtener los permisos asignados en los grupos y agregarlos a la lista perms
        for group in self.user.groups.all():
            permissions = group.permissions.all()
            perms.extend( [p for p in permissions] )
        
        # Eliminar permisos duplicados (en caso de agregar uno individual que ya esté en un grupo)
        perms = list(set(perms))
        
        # Obtener los menus desde los permisos
        menus = []
        for perm in perms:
            menus.append(perm.menu)

        # Eliminar los menus duplicados
        menus = list(set(menus))

        # Recorrer cada menu para guardarlo a él y a todos sus padres
        UserMenus.objects.filter(user=self.user).delete()
        for menu in menus:
            # Guardar el menú
            UserMenus.objects.create(user=self.user, menu=menu)

            # Llamando a la función recursiva para guardar toda la jerarquía de menús
            add_parents(menu, self.user)
        
        # Obtener solo los menús que no tienen padre (menús de primer nivel)
        top_menus = UserMenus.objects.filter(user=self.user, menu__menu_padre=None).order_by('id')

        # Construcción de la estructura de menús desde los padres hasta los últimos hijos
        authorizations = []
        for mnu in top_menus:
            authorizations.append({
                'id': mnu.menu.id,
                'name': mnu.menu.name,
                'url': mnu.menu.url,
                'actions': [],
                'children': build_menu(mnu.menu.menu_set.all(), self.user, perms)
            })
        
        data.update({'user': {'id': self.user.id, 'username': self.user.username}})
        data.update({'authorizations': authorizations})
        return data        
    
    # @classmethod
    # def get_token(cls, user):
    #     token = super().get_token(user)

    #     claims = [perm.code for perm in user.permission.all()]

    #     #token['full_name'] = user.get_full_name() or 'SysAdmin'
    #     #token['claims'] = claims
    #     #token['is_admin'] = True

    #     return Response({"tokens": token})

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


# ------

class MyTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        
        data = super(MyTokenRefreshSerializer, self).validate(attrs)
        decoded_payload = token_backend.decode(data['access'], verify=True)
        user_uid=decoded_payload['user_id']
        #data.update({'custom_field': 'custom_data'})        
        return data

class MyTokenRefreshView(TokenRefreshView):
    serializer_class = MyTokenRefreshSerializer

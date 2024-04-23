#python manage.py shell

from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

from user.models import CustomUser


# Benötigte Berechtigungen für das CustomUser-Modell
permissions = ['add_customuser', 'change_customuser', 'delete_customuser', 'view_customuser']

# Überprüfe, ob die Berechtigungen in der Datenbank vorhanden sind
for permission in permissions:
    try:
        permission_obj = Permission.objects.get(codename=permission, content_type=ContentType.objects.get_for_model(CustomUser))
        print(f"{permission}: {permission_obj}")
    except Permission.DoesNotExist:
        print(f"{permission}: Berechtigung existiert nicht")

from django.contrib import admin
from main import models
# Register your models here.

admin.site.register([
    models.Document,
    models.File,
    models.Tag,
    models.Group,
    models.FileUserPermission,
    models.FileGroupPermission,
    models.FileVersion
])

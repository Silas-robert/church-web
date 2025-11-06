from django.apps import apps
from django.contrib import admin

app = apps.get_app_config('ministry')  # your app name
for model_name, model in app.models.items():
    admin.site.register(model)

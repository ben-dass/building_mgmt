from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from .models import ContentView


@admin.register(ContentView)
class ContentViewAdmin(admin.ModelAdmin):
    list_display = ("content_object", "user", "viewer_ip", "last_viewed")


class ContentViewInline(GenericTabularInline):
    model = ContentView
    # No new/extra empty forms will be displayed in the admin portal for adding new ContentViews. Only existing ones will be displayed.
    extra = 0
    readonly_fields = ("user", "viewer_ip", "created_at")

from django.contrib import admin

from .models import Column, Dataset, Schema


@admin.register(Schema)
class SchemaAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "author", "created_at", "updated_at")
    list_display_links = ("id", "title")
    list_filter = ("author", "created_at", "updated_at")
    search_fields = ("title", "author__username")
    raw_id_fields = ("author",)
    list_select_related = ("author",)
    list_per_page = 25


@admin.register(Column)
class ColumnAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "type", "schema", "order")
    list_display_links = ("id", "name", "schema")
    list_filter = ("schema", "type")
    search_fields = ("name", "schema__title", "type")
    raw_id_fields = ("schema",)
    list_select_related = ("schema",)
    list_per_page = 25


@admin.register(Dataset)
class DatasetAdmin(admin.ModelAdmin):
    list_display = ("id", "__str__", "author", "schema", "status", "created_at")
    list_display_links = ("id", "__str__", "author", "schema")
    list_filter = ("author", "schema", "status")
    search_fields = ("author__username", "schema__title", "status")
    raw_id_fields = ("author", "schema")
    list_select_related = ("author", "schema")
    list_per_page = 25

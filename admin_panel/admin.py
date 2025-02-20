from django.contrib import admin
from .models import Section, Page

@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_at', 'updated_at')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'section', 'slug', 'created_at', 'updated_at')
    list_filter = ('section',)
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'section__name')

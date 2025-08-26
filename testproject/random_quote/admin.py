from django.contrib import admin
from .models import Quote

@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = ('get_short_text', 'source', 'source_type', 'weight', 'likes', 'dislikes', 'watches', 'created_at')
    list_filter = ('source_type', 'created_at', 'weight')
    search_fields = ('quote_text', 'source')
    ordering = ('-likes', '-weight', '-watches')
    readonly_fields = ('watches', 'created_at', 'updated_at')

    fieldsets = (
        ('Основная информация', {
            'fields': ('quote_text', 'source', 'source_type', 'weight')
        }),
        ('Статистика', {
            'fields': ('watches', 'likes', 'dislikes'),
            'classes': ('collapse',)
        }),
        ('Системная информация', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def get_short_text(self, obj):
        return obj.get_short_text(50)
    get_short_text.short_description = 'Текст цитаты'

    def get_queryset(self, request):
        return super().get_queryset(request).select_related()

admin.site.site_header = "Администрирование цитат"
admin.site.site_title = "Цитаты Admin"
admin.site.index_title = "Добро пожаловать в панель управления цитатами 🤩"
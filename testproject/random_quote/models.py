from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

class Quote(models.Model):
    MOVIE = "Ф"
    BOOK = "К"
    SERIES = "С"
    PEOPLE = "Ч"
    SOURCE_CHOICES = (
        (MOVIE, 'Фильм'),
        (BOOK, 'Книга'),
        (SERIES, 'Сериал'),
        (PEOPLE, 'Известный человек'),
    )

    quote_id = models.AutoField(primary_key=True)
    quote_text = models.TextField(help_text="Текст цитаты (минимум 10 символов)")
    source = models.CharField(max_length=100, help_text="Источник цитаты (минимум 2 символа)")
    source_type = models.CharField(
        max_length=1,
        choices=SOURCE_CHOICES,
        default=PEOPLE,
        help_text="Тип источника цитаты"
    )
    weight = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], default=1,
                                 help_text="Вес цитаты (влияет на частоту показа)")
    watches = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.quote_text

    class Meta:
        ordering = ['-likes', '-weight', '-watches']
        indexes = [
            models.Index(fields=['weight']),
            models.Index(fields=['likes']),
            models.Index(fields=['source']),
        ]

    @property
    def total_reactions(self):
        """Общее количество реакций (лайки + дизлайки)"""
        return self.likes + self.dislikes

    @property
    def like_percentage(self):
        """Процент лайков от всех реакций"""
        if self.total_reactions == 0:
            return 0
        return round((self.likes / self.total_reactions) * 100, 1)

    @property
    def popularity_score(self):
        """Комплексный показатель популярности"""
        return (self.likes * 3) + (self.watches * 0.1) + (self.weight * 0.5) - (self.dislikes * 1)

    def get_short_text(self, max_length=100):
        """Получить сокращенный текст цитаты"""
        if len(self.quote_text) <= max_length:
            return self.quote_text
        return self.quote_text[:max_length-3] + "..."


    @classmethod
    def get_quotes_by_source_count(cls, source):
        """Получить количество цитат для источника"""
        return cls.objects.filter(source__iexact=source).count()
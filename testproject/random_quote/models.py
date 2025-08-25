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
    quote_text = models.TextField()
    source = models.CharField(max_length=100)
    source_type = models.CharField(
        max_length=1,
        choices=SOURCE_CHOICES,
        default=PEOPLE,
    )
    weight = models.IntegerField()
    watches = models.IntegerField()
    likes = models.IntegerField()
    dislikes = models.IntegerField()

    def __str__(self):
        return self.quote_text
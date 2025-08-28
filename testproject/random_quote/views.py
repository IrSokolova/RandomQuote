"""Views для приложения цитат.

Содержит:
- форму создания цитаты (CBV),
- показ случайной цитаты с взвешенным выбором и учётом просмотров,
- обработчики лайков/дизлайков,
- топ-10 по лайкам,
- дашборд со сводной статистикой и аналитикой по типам источников.
"""

import random

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, ListView, DetailView
from django.views.decorators.http import require_POST
from django.db.models import F, Count, Sum, Avg, Case, When, Value, CharField
from django.db.models.functions import Coalesce
from .models import Quote
from .forms import QuoteForm


class QuoteCreateView(CreateView):
    """
    Форма создания новой цитаты.

    Шаблон: ``quote_form.html``.
    Форма: ``QuoteForm``.
    После успешного сохранения — редирект на страницу случайной цитаты.
    """
    template_name = "quote_form.html"
    form_class = QuoteForm
    success_url = reverse_lazy("random_quote")

"""
Показ случайной цитаты с учётом веса.

Алгоритм:
1) Загружаем все цитаты.
2) Если пусто — возвращаем шаблон без цитаты.
3) Если суммарный вес > 0, используем взвешенный выбор по полю ``weight``.
   Иначе — равновероятный выбор.
4) Инкрементируем счётчик ``watches`` через F-выражение и обновляем объект.
Контекст шаблона:
- ``quote``: выбранная цитата или ``None``.
    """
def random_quote_view(request):
    quotes = list(Quote.objects.all())
    if not quotes:
        return render(request, "random.html", {"quote": None})

    weights = [max(0, q.weight) for q in quotes]
    if sum(weights) > 0:
        chosen = random.choices(quotes, weights=weights, k=1)[0]
    else:
        chosen = random.choice(quotes)

    Quote.objects.filter(pk=chosen.pk).update(watches=F("watches") + 1)
    chosen.refresh_from_db(fields=["watches"])

    return render(request, "random.html", {"quote": chosen})


"""
Обработчик лайка для цитаты (POST).

Действия:
    - Увеличивает ``likes`` на 1.
    - Повышает ``weight`` (но не выше 100).
    - Сохраняет только изменённые поля.
    - Редиректит на показ случайной цитаты.

Args:
    pk (int): первичный ключ цитаты.
"""
@require_POST
def like_quote(request, pk: int):
    quote = get_object_or_404(Quote, pk=pk)
    quote.likes += 1
    quote.weight = min(quote.weight + 1, 100)
    quote.save(update_fields=['likes', 'weight'])
    return redirect(random_quote_view)

"""
Обработчик дизлайка для цитаты (POST).

Действия:
    - Увеличивает ``dislikes`` на 1.
    - Понижает ``weight`` (но не ниже 0).
    - Сохраняет только изменённые поля.
    - Редиректит на показ случайной цитаты.

Args:
    pk (int): первичный ключ цитаты.
"""
@require_POST
def dislike_quote(request, pk: int):
    quote = get_object_or_404(Quote, pk=pk)
    quote.dislikes += 1
    quote.weight = max(quote.weight - 1, 0)
    quote.save(update_fields=['dislikes', 'weight'])
    return redirect(random_quote_view)


class Top10ByLikesView(ListView):
    """
    Список топ-10 цитат по лайкам.

    Шаблон: ``top10.html``.
    Имя контекста: ``quotes``.
    Сортировка: по лайкам ↓, затем по весу ↓ и просмотрам ↓.
    """
    model = Quote
    template_name = "top10.html"
    context_object_name = "quotes"

    """Вернуть QuerySet из 10 самых «сильных» цитат по заданному порядку."""
    def get_queryset(self):
        return Quote.objects.order_by("-likes", "-weight", "-watches")[:10]


def dashboard_view(request):
    """
    Дашборд с общей статистикой и аналитикой.

    Считает агрегаты по всем цитатам и формирует срезы:
        - ``stats``: суммарные просмотры/лайки/дизлайки, количество цитат и средний вес.
        - ``source_stats``: группировка по типу источника (с человекочитаемой меткой),
          количества цитат, лайков и просмотров (Coalesce -> 0 для None).
        - ``top_sources``: топ-5 источников по сумме лайков.
        - ``recent_quotes``: 5 последних добавленных цитат.

    Рендерит шаблон ``dashboard.html`` с соответствующим контекстом.
    """
    stats = {
        'total_quotes': Quote.objects.count(),
        'total_views': Quote.objects.aggregate(Sum('watches'))['watches__sum'] or 0,
        'total_likes': Quote.objects.aggregate(Sum('likes'))['likes__sum'] or 0,
        'total_dislikes': Quote.objects.aggregate(Sum('dislikes'))['dislikes__sum'] or 0,
        'avg_weight': Quote.objects.aggregate(Avg('weight'))['weight__avg'] or 0,
    }

    source_stats = (
        Quote.objects.values('source_type')
        .annotate(
            source_type_label=Case(
                When(source_type=Quote.MOVIE, then=Value('Фильм')),
                When(source_type=Quote.BOOK, then=Value('Книга')),
                When(source_type=Quote.SERIES, then=Value('Сериал')),
                When(source_type=Quote.PEOPLE, then=Value('Известный человек')),
                default=Value('Неизвестно'),
                output_field=CharField(),
            ),
            count=Count('quote_id'),
            total_likes=Coalesce(Sum('likes'), 0),
            total_views=Coalesce(Sum('watches'), 0),
        )
        .order_by('-count')
    )

    top_sources = Quote.objects.values('source').annotate(
        count=Count('quote_id'),
        total_likes=Sum('likes')
    ).order_by('-total_likes')[:5]

    recent_quotes = Quote.objects.order_by('-created_at')[:5]

    context = {
        'stats': stats,
        'source_stats': source_stats,
        'top_sources': top_sources,
        'recent_quotes': recent_quotes,
    }

    return render(request, 'dashboard.html', context)
import random
from collections import Counter

from django.db.models import F
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, ListView, DetailView
from django.views.decorators.http import require_POST
from django.db.models import Avg, Sum, Count
from .models import Quote
from .forms import QuoteForm


class QuoteCreateView(CreateView):
    template_name = "quote_form.html"
    form_class = QuoteForm
    success_url = reverse_lazy("random_quote")


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


@require_POST
def like_quote(request, pk: int):
    quote = get_object_or_404(Quote, pk=pk)
    quote.likes += 1
    quote.weight = min(quote.weight + 1, 100)
    quote.save(update_fields=['likes', 'weight'])
    return redirect(random_quote_view)


@require_POST
def dislike_quote(request, pk: int):
    quote = get_object_or_404(Quote, pk=pk)
    quote.dislikes += 1
    quote.weight = max(quote.weight - 1, 0)
    quote.save(update_fields=['dislikes', 'weight'])
    return redirect(random_quote_view)


class Top10ByLikesView(ListView):
    model = Quote
    template_name = "top10.html"
    context_object_name = "quotes"

    def get_queryset(self):
        return Quote.objects.order_by("-likes", "-weight", "-watches")[:10]


def dashboard_view(request):
    """Дашборд с общей статистикой"""
    stats = {
        'total_quotes': Quote.objects.count(),
        'total_views': Quote.objects.aggregate(Sum('watches'))['watches__sum'] or 0,
        'total_likes': Quote.objects.aggregate(Sum('likes'))['likes__sum'] or 0,
        'total_dislikes': Quote.objects.aggregate(Sum('dislikes'))['dislikes__sum'] or 0,
        'avg_weight': Quote.objects.aggregate(Avg('weight'))['weight__avg'] or 0,
    }

    # Статистика по типам источников
    source_stats = Quote.objects.values('source_type').annotate(
        count=Count('quote_id'),
        total_likes=Sum('likes'),
        total_views=Sum('watches')
    ).order_by('-count')

    # Топ источники
    top_sources = Quote.objects.values('source').annotate(
        count=Count('quote_id'),
        total_likes=Sum('likes')
    ).order_by('-total_likes')[:5]

    # Последние добавленные цитаты
    recent_quotes = Quote.objects.order_by('-created_at')[:5]

    context = {
        'stats': stats,
        'source_stats': source_stats,
        'top_sources': top_sources,
        'recent_quotes': recent_quotes,
    }

    return render(request, 'dashboard.html', context)

def quotes_by_source_view(request, source_type=None):
    """Просмотр цитат по типу источника"""
    quotes = Quote.objects.all()

    if source_type:
        quotes = quotes.filter(source_type=source_type)
        title = f"Цитаты из категории: {dict(Quote.SOURCE_CHOICES).get(source_type, source_type)}"
    else:
        title = "Все цитаты"

    quotes = quotes.order_by('-likes', '-weight')

    context = {
        'quotes': quotes,
        'title': title,
        'source_type': source_type,
        'source_choices': Quote.SOURCE_CHOICES,
    }

    return render(request, 'quotes_by_source.html', context)
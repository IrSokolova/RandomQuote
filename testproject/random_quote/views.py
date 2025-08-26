import random
from django.db.models import F
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, ListView
from django.views.decorators.http import require_POST
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
    Quote.objects.filter(pk=pk).update(likes=F("likes") + 1)
    Quote.objects.filter(pk=pk).update(weight=F("weight") + 1)
    return redirect(random_quote_view)


@require_POST
def dislike_quote(request, pk: int):
    Quote.objects.filter(pk=pk).update(dislikes=F("dislikes") + 1)
    Quote.objects.filter(pk=pk).update(weight=max(F("weight") - 1, 0))
    return redirect(random_quote_view)


class Top10ByLikesView(ListView):
    model = Quote
    template_name = "top10.html"
    context_object_name = "quotes"

    def get_queryset(self):
        return Quote.objects.order_by("-likes", "-weight", "-watches")[:10]
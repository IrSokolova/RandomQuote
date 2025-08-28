"""
URLConf приложения цитат.

Содержит маршруты:
- Главная: показ случайной цитаты (взвешенный рандом).
- Создание цитаты (CBV).
- Лайк/дизлайк по первичному ключу (ожидается POST; view делает редирект).
- Топ-10 по лайкам (ListView).
- Дашборд со сводной статистикой.

Имена маршрутов используются в reverse()/reverse_lazy и в шаблонах.
"""

from django.urls import path
from .views import (
    QuoteCreateView,
    random_quote_view,
    like_quote,
    dislike_quote,
    Top10ByLikesView,
    dashboard_view
)

urlpatterns = [
    # Главная страница приложения: показ случайной цитаты с учётом "веса".
    # name="random_quote" используется для редиректов из форм/обработчиков.
    path("", random_quote_view, name="random_quote"),

    # Страница создания новой цитаты (class-based view).
    # После успешного сохранения QuoteCreateView редиректит на random_quote.
    path("quotes/add/", QuoteCreateView.as_view(), name="quote_add"),

    # Лайк конкретной цитаты по её первичному ключу (pk).
    # View ожидает POST и по завершении редиректит на random_quote.
    path("quotes/<int:pk>/like/", like_quote, name="quote_like"),

    # Дизлайк конкретной цитаты по её первичному ключу (pk).
    # Аналогично обработчику лайка: POST + редирект на random_quote.
    path("quotes/<int:pk>/dislike/", dislike_quote, name="quote_dislike"),

    # Список топ-10 цитат по лайкам (доп. сортировка по weight и watches).
    path("quotes/top/", Top10ByLikesView.as_view(), name="quotes_top"),

    # Дашборд со сводной статистикой и аналитикой по типам источников/лайкам/просмотрам.
    path("quotes/dashboard/", dashboard_view, name="dashboard")
]
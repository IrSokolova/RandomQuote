from django import forms
from django.core.exceptions import ValidationError
from .models import Quote

class QuoteForm(forms.ModelForm):
    """
    Форма для ввода/редактирования цитаты.

    Основана на модели :class:`Quote`. Управляет отображением полей,
    подписями/подсказками и прикладной валидацией (ограничения длины,
    уникальность пары «текст+источник», лимит количества цитат для одного источника,
    корректность и обязательность веса).
    """

    class Meta:
        """
        Мета-настройки формы.

        Определяет используемую модель и набор полей, а также человекочитаемые
        подписи (labels), подсказки (help_texts) и виджеты ввода (widgets).
        """
        model = Quote
        fields = ["quote_text", "source", "source_type", "weight"]

        labels = {
            "quote_text": "Текст цитаты",
            "source": "Источник",
            "source_type": "Тип источника цитаты",
            "weight": "Вес цитаты",
        }
        help_texts = {
            "quote_text": "Минимум 10 символов.",
            "source": "Минимум 2 символа.",
            "weight": "Влияет на частоту показа.",
        }
        widgets = {
            "quote_text": forms.Textarea(attrs={"rows": 6, "placeholder": "Введите текст цитаты…"}),
            "source": forms.TextInput(attrs={"placeholder": "Книга, фильм, интервью…"}),
            "source_type": forms.Select(),
            "weight": forms.NumberInput(attrs={"min": 0}),
        }

    """
    Комплексная валидация формы и наполнение ошибок полей.

    Логика:
        1) Нормализуем значения (strip).
        2) Проверяем обязательность и минимальную длину:
           - ``quote_text`` ≥ 10 символов,
           - ``source`` ≥ 2 символов.
        3) Глобальная уникальность сочетания (case-insensitive):
           (``quote_text``, ``source``) — при нарушении добавляем non-field error.
        4) Ограничение: для одного ``source`` допускается не более 3 цитат.
        5) ``weight`` обязателен и не может быть отрицательным.

    Возвращает:
        dict: очищенные данные (``cleaned``) для дальнейшей обработки.
    """
    def clean(self):
        cleaned = super().clean()
        qt = (cleaned.get("quote_text") or "").strip()
        source = (cleaned.get("source") or "").strip()

        if not qt:
            self.add_error("quote_text", "Текст цитаты не может быть пустым.")
        elif len(qt) < 10:
            self.add_error("quote_text", "Цитата должна содержать минимум 10 символов.")

        if Quote.objects.filter(quote_text__iexact=qt, source__iexact=source).exists():
            self.add_error(None, "Такая цитата уже существует.")

        if not source:
            self.add_error("source", "Источник не может быть пустым.")
        elif len(source) < 2:
            self.add_error("source", "Название источника должно содержать минимум 2 символа.")

        if Quote.objects.filter(source__iexact=source).count() >= 3:
            self.add_error("source", "У одного источника нельзя хранить больше трёх цитат.")

        weight = cleaned.get("weight")
        if weight is None:
            self.add_error("weight", "Укажите вес.")
        elif weight < 0:
            self.add_error("weight", "Вес должен быть неотрицательным целым числом.")

        return cleaned


    """
    Сохранить объект Quote, гарантируя корректные значения счётчиков.

    Перед сохранением инициализирует ``watches``, ``likes`` и ``dislikes``
    нулями, если они по какой-то причине оказались ``None`` (страховка при
    частичных обновлениях/миграциях).

    Args:
        commit (bool): если True — сохраняет объект в БД сразу.

    Returns:
        Quote: сохранённый экземпляр модели.
    """
    def save(self, commit=True):
        obj = super().save(commit=False)

        if obj.watches is None:
            obj.watches = 0
        if obj.likes is None:
            obj.likes = 0
        if obj.dislikes is None:
            obj.dislikes = 0

        if commit:
            obj.save()
        return obj
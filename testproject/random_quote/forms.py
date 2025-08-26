from django import forms
from django.core.exceptions import ValidationError
from .models import Quote

class QuoteForm(forms.ModelForm):
    class Meta:
        model = Quote
        fields = ["quote_text", "source", "source_type", "weight"]

    def clean(self):
        cleaned = super().clean()
        qt = (cleaned.get("quote_text") or "").strip()
        source = (cleaned.get("source") or "").strip()

        if not qt:
            raise ValidationError("Текст цитаты не может быть пустым.")

        if not source:
            raise ValidationError("Источник не может быть пустым.")

        if len(qt) < 10:
            raise ValidationError("Цитата должна содержать минимум 10 символов.")

        if len(source) < 2:
            raise ValidationError("Название источника должно содержать минимум 2 символа.")

        if Quote.objects.filter(quote_text__iexact=qt, source__iexact=source).exists():
            raise ValidationError("Такая цитата уже существует.")

        if Quote.objects.filter(source__iexact=source).count() >= 3:
            raise ValidationError("У одного источника нельзя хранить больше трёх цитат.")

        w = cleaned.get("weight")
        if w is None or w < 0:
            raise ValidationError("Вес должен быть неотрицательным целым числом.")

        return cleaned

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
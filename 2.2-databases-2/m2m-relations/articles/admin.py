from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet

from .models import Article, Tags, Scope


class ScopeInlineFormset(BaseInlineFormSet):
    def clean(self):
        counter = 0

        for form in self.forms:
            if 'is_main' in form.cleaned_data:
                if form.cleaned_data['is_main']:
                    counter += 1

        if counter == 0:
            raise ValidationError('Нужно указать основной тэг')
        elif counter >= 2:
            raise ValidationError('Основной тэг может быть только один')

        return super().clean()


class ScopeInline(admin.TabularInline):
    model = Scope
    extra = 3
    formset = ScopeInlineFormset


@admin.register(Tags)
class TagsAdmin(admin.ModelAdmin):
    inlines = (ScopeInline,)


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [ScopeInline,]

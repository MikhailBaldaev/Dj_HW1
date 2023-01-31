from django.db import models


class Tags(models.Model):
    name = models.CharField(max_length=256)

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

    def __str__(self):
        return str(self.name)


class Article(models.Model):

    title = models.CharField(max_length=256, verbose_name='Название')
    text = models.TextField(verbose_name='Текст')
    published_at = models.DateTimeField(verbose_name='Дата публикации')
    image = models.ImageField(null=True, blank=True, verbose_name='Изображение')
    tag = models.ManyToManyField(Tags, through='Scope', related_name='articles', verbose_name='Тэг')

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ['-published_at']

    def __str__(self):
        return str(self.title)


class Scope(models.Model):
    is_main = models.BooleanField(default=False, verbose_name='ОСНОВНОЙ')
    tag = models.ForeignKey(Tags, on_delete=models.CASCADE, related_name='scopes')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, null=True, related_name='scopes',)

    class Meta:
        verbose_name = 'Связь'
        verbose_name_plural = 'Связи'

    def __str__(self):
        return str(self.tag)

from django.db import models
from django.contrib.auth import get_user_model


class BaseModel(models.Model):
    title = models.CharField(
        verbose_name='Заголовок',
        max_length=256,
        null=False
    )
    is_published = models.BooleanField(
        verbose_name='Опубликовано',
        default=True,
        null=False,
        help_text='Снимите галочку, чтобы скрыть публикацию.'
    )
    created_at = models.DateTimeField(
        verbose_name='Добавлено',
        auto_now_add=True,
        null=False
    )

    class Meta:
        abstract = True


User = get_user_model()


class Location(BaseModel):
    name = models.CharField(
        verbose_name='Название места',
        max_length=256,
        null=False
    )

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'


class Category(BaseModel):
    description = models.TextField(
        verbose_name='Описание',
        null=False
    )
    slug = models.SlugField(
        verbose_name='Идентификатор',
        unique=True,
        null=False,
        help_text=(
            'Идентификатор страницы для URL; разрешены символы '
            'латиницы, цифры, дефис и подчёркивание.'
        )
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'


class Post(BaseModel):
    text = models.TextField(
        verbose_name='Текст',
        null=False
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата и время публикации',
        null=False,
        help_text=(
            'Если установить дату и время в будущем — '
            'можно делать отложенные публикации.'
        )
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор публикации',
        on_delete=models.CASCADE,
        null=False
    )
    location = models.ForeignKey(
        Location,
        verbose_name='Местоположение',
        on_delete=models.SET_NULL,
        null=True
    )
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        on_delete=models.SET_NULL,
        blank=False,
        null=True
    )
    image = models.ImageField(
        verbose_name='Изображение',
        upload_to='post_images',
        blank=True,
    )

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    text = models.TextField(verbose_name='Комментарий')
    created_at = models.DateTimeField(auto_now_add=True)

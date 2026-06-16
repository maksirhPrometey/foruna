from django.db import models


class Lead(models.Model):
    SOURCE_CHOICES = [
        ('contact', 'Контакти'),
        ('marking', 'Маркування'),
        ('quality', 'Контроль якості'),
        ('labeling', 'Етикетування'),
    ]
    name = models.CharField('Ім\'я', max_length=120)
    phone = models.CharField('Телефон', max_length=30)
    message = models.TextField('Повідомлення', blank=True)
    source = models.CharField('Джерело', max_length=20, choices=SOURCE_CHOICES, default='contact')
    created = models.DateTimeField('Дата', auto_now_add=True)
    is_read = models.BooleanField('Прочитано', default=False)

    class Meta:
        ordering = ['-created']
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'

    def __str__(self) -> str:
        return f'{self.name} — {self.phone} ({self.created:%d.%m.%Y %H:%M})'

from django.db import models


class ProfileStudent(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    user_id = models.CharField(
        verbose_name='ID пользователя', max_length=70, unique=True, 
        blank=False
    )
    name = models.CharField(
        verbose_name='Обращение', max_length=15, default='Студент', 
        blank=True, null=True
    )
    faculties = models.CharField(
        verbose_name='Название факультатива/института', max_length=60, 
        blank=True, null=True
    )
    course = models.IntegerField(
        verbose_name='Курс', blank=True, null=True
    )
    year_start_learn = models.IntegerField(
        verbose_name='Год начала обучения', blank=True, null=True
    )
    form_of_learn = models.CharField(
        verbose_name='Форма обучения', max_length=2, blank=True, 
        null=True
    )
    direction = models.CharField(
        verbose_name='Направление', max_length=3, blank=True, null=True
    )
    group = models.IntegerField(
        verbose_name='Направление', blank=True, null=True
    )
    state = models.CharField(
        verbose_name='Состояние сессии', max_length=10, default='Free', 
        blank=True, null=True
    )

    def __str__(self):
        return f'Profile <{self.name}>, {self.year_start_learn}-'  \
            f'{self.form_of_learn}-{self.direction}{self.group}'

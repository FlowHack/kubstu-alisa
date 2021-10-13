from django.db import models

class ProfileStudent(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.CharField(
        verbose_name='ID пользователя', max_length=70, unique=True, 
        blank=False
    )
    name = models.CharField(
        verbose_name='Обращение', max_length=15, default='Студент', 
        blank=False
    )
    faculties = models.CharField(
        verbose_name='Название факультатива/института', max_length=60, 
        blank=False
    )
    course = models.IntegerField(verbose_name='Курс', blank=False)
    year_start_learn = models.IntegerField(
        verbose_name='Год начала обучения', blank=False
    )
    form_of_learn = models.CharField(
        verbose_name='Форма обучения', max_length=2, blank=False
    )
    direction = models.CharField(
        verbose_name='Направление', max_length=3, blank=False
    )
    group = models.IntegerField(verbose_name='Направление', blank=False)

    def __str__(self):
        return f'Profile <{self.name}>, {self.year_start_learn}-'  \
            f'{self.form_of_learn}-{self.direction}{self.group}'

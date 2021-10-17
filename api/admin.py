from django.contrib import admin

from .models import ProfileStudent


@admin.register(ProfileStudent)
class ProfileStudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'year_start_learn', 'form_of_learn', 'direction', 'group', 'state')
    search_fields = ('user', 'year_start_learn', 'form_of_learn', 'direction', 'group')
    empty_value_display = '-пусто-'

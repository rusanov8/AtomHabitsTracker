from django.contrib import admin

from habits.models import Habit


# Register your models here.
@admin.register(Habit)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'action', 'owner', 'periodicity', 'is_pleasant', 'is_public')
    list_filter = ('periodicity', 'is_pleasant', 'is_public')
    search_fields = ('action', )
    ordering = ('-id',)

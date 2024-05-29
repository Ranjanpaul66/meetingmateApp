from django.apps import AppConfig


class CalendarappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'calendarapp'

    def ready(self):
        # import calendarapp.periodic_tasks
        # calendarapp.periodic_tasks.create_periodic_task()
        import calendarapp.signals
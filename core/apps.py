from django.apps import AppConfig

class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        """Django app yuklanganda stollar va boshqa ma'lumotlarni initialize qilish"""
        from core import views
        ts = views.table_service
        if not ts.get_all_tables():
            for i in range(1, 11):
                capacity = 2 if i <= 4 else (4 if i <= 7 else 6)
                location = "Main Hall" if i <= 7 else "VIP Area"
                ts.add_table(i, capacity, location)

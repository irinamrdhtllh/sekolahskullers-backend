from django.apps import AppConfig


class SekolahConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'sekolah'

    def ready(self):
        import sekolah.signals

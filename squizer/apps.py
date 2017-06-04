from django.apps import AppConfig

class SquizerConfig(AppConfig):
    name = 'squizer'

    def ready(self):
        import squizer.signals

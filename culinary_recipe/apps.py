from django.apps import AppConfig


class CulinaryRecipeConfig(AppConfig):
    name = 'culinary_recipe'

    def ready(self):
        import culinary_recipe.signals

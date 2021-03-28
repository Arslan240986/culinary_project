from django.contrib import admin
from django.utils.safestring import mark_safe
from mptt.admin import MPTTModelAdmin

from .models import (Country, Category, Step,
                     Dish, Ingredient, Measure,
                     DishComment, SubCategory,
                     Device, Occasion, Technology, DishLike,
                     Complexity, Vegeterian)


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Occasion)
class OccasionAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Complexity)
class OccasionAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Vegeterian)
class OccasionAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Technology)
class TechnologyAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    fields = ('name', 'slug', 'poster')
    list_display = ('id', 'name', 'slug', 'poster')
    prepopulated_fields = {'slug': ('name',)}


class ReviewInlines(admin.TabularInline):
    model = DishComment
    extra = 1
    fields = ('parent', 'meal', 'id')


class StepsInlines(admin.TabularInline):
    model = Step
    readonly_fields = ('get_image',)
    extra = 1

    def get_image(self, obj):
        return mark_safe(f"<img src={obj.image.url}, width='100' height='100'>")

    get_image.short_description = 'Изображение'


class IngrediengtsInlines(admin.TabularInline):
    model = Ingredient

    def get_image(self, obj):
        return mark_safe(f"<img src={obj.image.url}, width='100' height='100'>")

    get_image.short_description = 'Изображение'
    extra = 1


@admin.register(Dish)
class MealAdmin(admin.ModelAdmin):
    list_display = ('title', 'id', 'sub_category', 'slug', 'draft', 'moderator')
    list_filter = ('category', 'sub_category')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'category__name',)
    inlines = [StepsInlines, IngrediengtsInlines, ReviewInlines, ]
    save_on_top = True
    save_as = True
    list_editable = ('draft', 'moderator')
    readonly_fields = ('get_image',)
    fieldsets = (
        (None, {
            'fields':(('title', 'slug', 'draft'),)
        }),
        (None, {
            'fields':(('description', 'poster', 'get_image'),)
        }),
        (None, {
            'fields':(('author','country', 'category', 'sub_category'),)
        }),
        (None, {
            'fields': (('likes', 'is_liked', 'dish_added'),)
        }),
        (None, {
            'fields': (('preparation_time_hour', 'preparation_time_minute', 'cooking_time_hour', 'cooking_time_minute'),)
        }),
        (None, {
            'fields': (('complexity', 'vegetarian', 'technology', 'device'),)
        }),
        (None, {
            'fields': (('calorie', 'protein', 'fat', 'carbohydrate'),)
        }),
    )

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.poster.url}, width="100" height="100"')


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    fields = ('name', 'quantity', 'measure', 'note',)
    list_display = ('id', 'name', 'quantity', 'measure', 'note',)


admin.site.register(Measure)
admin.site.register(Step)
admin.site.register(DishLike)


@admin.register(DishComment)
class ReviewAdmin(MPTTModelAdmin):
    list_display = ('id', 'text', 'author', 'status', 'meal',)
    list_editable = ('status',)


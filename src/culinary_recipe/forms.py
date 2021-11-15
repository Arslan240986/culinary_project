from django import forms
from ckeditor.widgets import CKEditorWidget
from nested_formset import nestedformset_factory

from .models import (DishComment, Dish, Category,
                     Step, IngredientList, SubCategory,
                     Technology, IngredientTitle)
from django.forms.models import BaseInlineFormSet, inlineformset_factory


class SearchField(forms.Form):
    search = forms.CharField(max_length=200, label='', label_suffix='',
                             widget=forms.TextInput(
                                 attrs={'class':'font-oswald',
                                        'placeholder': 'Поиск'}))


class DishCommentForm(forms.ModelForm):
    """Форма отзывов"""
    class Meta:
        model = DishComment
        fields = ('text',)
        widgets = {
            'text': forms.Textarea(attrs={'rows': 2})
        }


class IngredientTitleForm(forms.ModelForm):
    class Meta:
        model = IngredientTitle
        fields = ('name',)


class StepsForm(forms.ModelForm):

    class Meta:
        model = Step
        fields = ('description', 'image')


class DishForm(forms.ModelForm):
    title = forms.CharField(error_messages={'required': 'Укажите название рецепта'}, label='Название рецепта')
    poster = forms.ImageField(label_suffix='*', error_messages={'required': 'Загрузить обязательно'}, label='Постер',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['sub_category'].queryset = SubCategory.objects.none()

        if 'category' in self.data:
            try:
                category_id = int(self.data.get('category'))
                self.fields['sub_category'].queryset = SubCategory.objects.filter(category_id=category_id).order_by('name')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['sub_category'].queryset = self.instance.category.sub_category.all()

    class Meta:
        model = Dish
        exclude = ['created', 'updated', 'count',
                   'likes', 'is_liked',
                   'slug', 'author', 'dish_added']
        localized_fields = ('title', 'poster')
        widgets = {
            'preparation_time_hour': forms.NumberInput(attrs={'placeholder': 'часы'}),
            'preparation_time_minute': forms.NumberInput(attrs={'placeholder': 'минуты'}),
            'cooking_time_hour': forms.NumberInput(attrs={'placeholder': 'часы'}),
            'cooking_time_minute': forms.NumberInput(attrs={'placeholder': 'минуты'}),
            'servings': forms.TextInput(attrs={'style': 'width: 100%;'}),
            'technology': forms.SelectMultiple(attrs={'multiple':"",
                                                      'class':"ui fluid dropdown",
                                                      'placeholder': 'Не выбрано'}),
            'device': forms.SelectMultiple(attrs={'multiple': "",
                                                  'class': "ui fluid dropdown",
                                                  'placeholder': 'Не выбрано'}),
            'occasion': forms.SelectMultiple(attrs={'multiple': "",
                                                  'class': "ui fluid dropdown",
                                                  'placeholder': 'Не выбрано'}),
            'category': forms.Select(attrs={'class': "ui fluid dropdown",
                                              'placeholder': 'Не выбрано'}),
            'sub_category': forms.Select(attrs={'class': "ui fluid dropdown",
                                            'placeholder': 'Не выбрано'}),
            'country': forms.Select(attrs={'class': "ui fluid dropdown",
                                              'placeholder': 'Не выбрано'}),
            'complexity': forms.Select(attrs={'class': "ui fluid dropdown",
                                              'placeholder': 'Не выбрано'}),
            'vegetarian': forms.Select(attrs={'class': "ui fluid dropdown",
                                              'placeholder': 'Не выбрано'}),
        }


class IngredientForm(forms.ModelForm):

    class Meta:
        model = IngredientList
        fields = ('name', 'quantity', 'measure', 'note',)
        widgets = {
            'note': forms.Textarea(attrs={'cols': 6, 'rows': 3,
                                          'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control dish_ingredient_name',
                                           'autocomplete': 'off'}),
            'measure': forms.Select(attrs={'class': 'ui my_dropdow'}),
            'quantity': forms.TextInput(attrs={'class': 'form-control'}),

        }


IngredientNestedFormSetCreate = nestedformset_factory(
    Dish,
    IngredientTitle,
    nested_formset=inlineformset_factory(
        IngredientTitle,
        IngredientList,
        form=IngredientForm,
        extra=1,
    ),
    extra=0,
)

IngredientNestedFormSet = nestedformset_factory(
    Dish,
    IngredientTitle,
    nested_formset=inlineformset_factory(
        IngredientTitle,
        IngredientList,
        form=IngredientForm,
        extra=0,
        min_num=1,
        validate_min=True,
    ),
    extra=0,
    min_num=1,
    validate_min=True,
)


InstructionFormSet = inlineformset_factory(Dish, Step,
                                           fields=('description', 'image'),
                                           can_delete=True, can_order=True,
                                           extra=0, min_num=1, validate_min=True,
                                           widgets={
                                               'description': forms.Textarea(attrs={'class': 'form-control m-2', 'rows':5}),
                                           })


from django import forms
from django.forms import HiddenInput, BaseInlineFormSet
from django.forms.formsets import BaseFormSet
from django.forms.models import inlineformset_factory
from .models import DishComment, Dish, Category, Step, Ingredient, SubCategory, Technology


class DishCommentForm(forms.ModelForm):
    """Форма отзывов"""
    class Meta:
        model = DishComment
        fields = ('text',)
        widgets = {
            'text': forms.Textarea(attrs={'rows': 2})
        }


class StepsForm(forms.ModelForm):
    class Meta:
        model = Step
        fields = ('description', 'image')


class DishForm(forms.ModelForm):
    title = forms.CharField(error_messages={'required': 'Укажите название рецепта'}, label='Название рецепта')
    poster = forms.ImageField(error_messages={'required': 'Загрузить обязательно'}, label='Постер',
                              help_text='Загрузите качественную фотографию блюда так как это главное фотография')

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
            'servings': forms.NumberInput(attrs={'style': 'width: 100%;'}),
            'technology': forms.SelectMultiple(attrs={'multiple':"",
                                                      'class':"ui fluid dropdown",
                                                      'placeholder': 'Не выбрано'}),
            'device': forms.SelectMultiple(attrs={'multiple': "",
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
    quantity = forms.DecimalField(error_messages={'invalid': 'это поле только для числового значения'},
                                  max_digits=1000, decimal_places=2, label_suffix="*",
                                  label="hernya"),

    class Meta:
        model = Ingredient
        fields = ('name', 'quantity', 'measure', 'note',)
        widgets = {
            'note': forms.Textarea(attrs={'cols': 6, 'rows': 3,
                                          'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control dish_ingredient_name',
                                           'autocomplete': 'off'}),
            'measure': forms.Select(attrs={'class': 'ui my_dropdow'}),
            'quantity': forms.TextInput(attrs={'class': 'form-control'}),

        }


class BaseArticleFormSet(BaseInlineFormSet):
    ordering_widget = HiddenInput


IngredientFormSet = inlineformset_factory(Dish, Ingredient, IngredientForm, formset=BaseArticleFormSet,
                                          extra=0, min_num=2, validate_min=True, can_delete=True, can_order=True)

InstructionFormSet = inlineformset_factory(Dish, Step, formset=BaseArticleFormSet,
                                           fields=('description',
                                                   'image'),
                                           can_delete=True, can_order=True,
                                           extra=0, min_num=1, validate_min=True,
                                           widgets={
                                               'description': forms.Textarea(attrs={'class': 'form-control m-2', 'rows':5}),
                                           })


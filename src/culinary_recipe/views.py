from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator

from django.views.generic.base import View
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from hitcount.views import HitCountDetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Dish, Country, Category, SubCategory, DishLike, Ingredient, Step
from culinary_post.models import CulinaryPost
from .forms import DishCommentForm, DishForm, IngredientFormSet, InstructionFormSet
from .utils import getMonth
# from .tasks import comment_add
from contact.models import UserProfile


class CategoryViewList(ListView):
    """Вывод категорий"""
    model = Category
    template_name = 'home.html'
    context_object_name = 'categories'
    extra_context = {
        'countries': Country.objects.all(),
        'posts': CulinaryPost.objects.all().order_by('-created')[:6],
    }


def get_sub_category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    sub_category = SubCategory.objects.filter(category=category)
    context = {
        'sub_categories': sub_category,
        'category': category
    }
    return render(request, 'culinary_recipe/recipe_categories.html', context)


class GetItems(View):
    """Вывод под категорий"""
    def get(self, request, slug=None):
        meal = Dish.objects.filter(draft=False, moderator=True)

        category_name = None
        if slug:
            meal = meal.filter(sub_category__slug=slug, moderator=True, draft=False)
            category_name = get_object_or_404(SubCategory, slug=slug)
        paginator = Paginator(meal, 2)

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {
            'meals': page_obj,
            'category': category_name,
            'page_obj': page_obj
        }
        return render(request, 'culinary_recipe/dishes_list.html', context)


class DishByCountry(View):
    """Вывод блюд по Странам"""
    def get(self, request, slug):
        country = get_object_or_404(Country, slug=slug)
        meals = Dish.objects.filter(country=country)
        return render(request, 'culinary_recipe/dishes_list.html', {'meals': meals, 'country': country})


class Search(ListView):
    template_name = 'culinary_recipe/dishes_list.html'

    def get_queryset(self):
        q = self.request.GET.get('q')
        meals = Dish.objects.filter(
            Q(ingredient__name__icontains=q) | Q(title__icontains=q)).distinct()
        return meals

    def get_context_data(self,  *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['meals'] = self.get_queryset()
        return context


class MealDetailView(HitCountDetailView):
    """Вывод деталей рецепта"""
    model = Dish
    count_hit = True
    template_name = 'culinary_recipe/meal_detail.html'

    def get(self, request, *args, **kwargs):
        meal = get_object_or_404(Dish, slug=self.kwargs.get('slug'), id=self.kwargs.get('pk'))
        meal_ings_list = set(meal.ingredient_set.all().values_list('name', flat=True))
        similar_meals = Dish.objects.filter(ingredient__name__in=meal_ings_list, moderator=True, draft=False).exclude(id=self.kwargs.get('pk'))[:3]
        form = DishCommentForm()
        comments = meal.comments.filter(status=False)
        comment_size = len(comments)
        context = dict()
        try:
            upper = self.kwargs['number']
            if upper:
                low = upper - 5
                comments_number = list(reversed(comments.values('id', 'parent_id', 'author_id', 'created', 'text', 'level')))[low:upper]
                if not comments_number[-1]['level'] == 0:
                    while not comments_number[-1]['level'] == 0:
                        upper += 1
                        comments_number = list(reversed(comments.values('id', 'parent_id', 'author_id', 'created', 'text', 'level')))[low:upper]
                for comment in comments_number:
                    date_time = str(comment['created']).split(' ')
                    date = date_time[0].split('-')
                    time = date_time[1].split(':')
                    comment['created'] = f'{date[2]} {getMonth(date[1])} {date[0]} г. {time[0]}:{time[1]}'
                    comment['user_name'] = UserProfile.objects.get(user_id=comment['author_id']).first_name
                    comment['user_avatar'] = UserProfile.objects.get(user_id=comment['author_id']).avatar.url
                    comment['user_personal_page'] = UserProfile.objects.get(user_id=comment['author_id']).get_user_profile_detail_absolute_url()

                context['load_more'] = False if upper >= comment_size else True;
            return JsonResponse({'new_data': comments_number, 'load_more': context}, safe=False)
        except:
            first_num = 5
            ne = list(reversed(comments))[:first_num]
            new_comments = list(reversed(ne))
            if new_comments:
                while not new_comments[0].level == 0:
                    first_num += 1
                    ne = list(reversed(comments))[:first_num]
                    new_comments = list(reversed(ne))
        if request.user.is_authenticated:
            user = get_object_or_404(User, id=request.user.id)
            boolean = user.profile.dishes.filter(id=meal.id).exists()
            if boolean:
                meal.dish_added = True
                meal.save()
            else:
                meal.dish_added = False
        context = {'meal': meal,
                   'form': form,
                   'pag_comments': new_comments,
                   'similar_meals': similar_meals,
                   'load_more': False if len(new_comments) >= comment_size else True,
                   }
        return render(request, self.template_name, context)


class AddCommentToDish(View):
    """Добавления коментарии к блюде"""
    def post(self, request, pk):
        context = {'status': False}
        form = DishCommentForm(request.POST)
        meal = get_object_or_404(Dish, id=pk)
        user_id = request.user.id
        if form.is_valid():
            form = form.save(commit=False)
            form.author = get_object_or_404(User, id=user_id)
            if request.POST.get('parent', None):
                form.parent_id = int(request.POST.get('parent'))
            form.meal = meal
            form.save()
            context = {
                'status': True
            }
        return JsonResponse(context, safe=False)


@login_required
def like_unlike_post(request):
    user = request.user
    if request.method == 'POST':
        dish_id = request.POST.get('dish_id')
        dish_obj = get_object_or_404(Dish, id=dish_id)
        user = get_object_or_404(User, id=user.id)
        if user in dish_obj.likes.all():
            dish_obj.likes.remove(user)
            dish_obj.is_liked = False
        else:
            dish_obj.likes.add(user)
            dish_obj.is_liked = True
        like, created = DishLike.objects.get_or_create(user=user, dish_id=dish_id)
        if not created:
            if like.value == 'Unlike':
                like.value = 'Like'
            else:
                like.value = 'Unlike'
        else:
            like.value = 'Like'
        dish_obj.save()
        like.save()
        data = {
            'is_liked': like.value,
            'form': dish_obj.likes.all().count()
        }
        return JsonResponse(data, safe=False)
    return redirect('/')


class DishCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = 'culinary_recipe/add_recipe.html'
    form_class = DishForm

    def get(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        ingredient_form = IngredientFormSet()
        instruction_form = InstructionFormSet()
        return self.render_to_response(
            self.get_context_data(form=form,
                                  ingredient_form=ingredient_form,
                                  instruction_form=instruction_form,
                                  )
        )

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        ingredient_form = IngredientFormSet(self.request.POST)
        instruction_form = InstructionFormSet(self.request.POST, self.request.FILES)
        if form.is_valid() and ingredient_form.is_valid() and instruction_form.is_valid():
            return self.form_valid(form, ingredient_form, instruction_form)
        else:
            messages.error(request, 'Исправте ниже указанные ошибки')
            return self.form_invalid(form, ingredient_form, instruction_form)

    def form_valid(self, form, ingredient_form, instruction_form):
        user = get_object_or_404(User, id=self.request.user.id)
        form.instance.author = user
        self.object = form.save()
        ingredient_form.instance = self.object
        ingredient_form.save()
        instruction_form.instance = self.object
        instruction_form.save()
        if form.instance.draft:
            return HttpResponseRedirect(user.profile.get_personal_absolute_url())
        messages.success(self.request, 'Спасибо за участие! Ваш рецепт будет добавлен на сайт после прохождения модерации.')
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, ingredient_form, instruction_form):
        return self.render_to_response(
            self.get_context_data(
                                  ingredient_form=ingredient_form,
                                  instruction_form=instruction_form)
        )


class DishUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Dish
    template_name = 'culinary_recipe/update_recipe.html'
    form_class = DishForm

    def get_context_data(self, **kwargs):
         self.object = self.get_object()
         context = super(DishUpdateView, self).get_context_data(**kwargs)
         if self.request.POST:
             context['form'] = DishForm(self.request.POST, self.request.FILES, instance=self.object)
             context['ingredient_form'] = IngredientFormSet(self.request.POST, instance=self.object)
             context['instruction_form'] = InstructionFormSet(self.request.POST, self.request.FILES, instance=self.object)
         else:
             if not self.request.user == self.object.author:
                 context['error_message'] = "Ты не можешь изменять рецепты чужих пользователей"
             else:
                context['form'] = DishForm(instance=self.object)
                context['ingredient_form'] = IngredientFormSet(instance=self.object)
                context['instruction_form'] = InstructionFormSet(instance=self.object)
         return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        ingredient_form = IngredientFormSet(self.request.POST)
        instruction_form = InstructionFormSet(self.request.POST, self.request.FILES)
        ingredient_id = ''
        for item, value in self.request.POST.items():
            if 'on' in value:
                if 'ingredient' in item and not ingredient_form.deleted_forms:
                    new_arr = item.split('-')
                    ingredient_id = new_arr[0]+'-'+new_arr[1]
            if item == f'{ingredient_id}-id':
                try:
                    ingredient_to_obj_delete = get_object_or_404(Ingredient, id=int(value))
                    ingredient_to_obj_delete.delete()
                except:
                    pass
        instruction_id = ''
        for item, value in self.request.POST.items():
            if 'on' in value:
                if 'step' in item and not instruction_form.deleted_forms:
                    new_arr = item.split('-')
                    instruction_id = new_arr[0] + '-' + new_arr[1]
            if item == f'{instruction_id}-id':
                try:
                    instruction_to_obj_delete = get_object_or_404(Step, id=int(value))
                    instruction_to_obj_delete.image.delete()
                    instruction_to_obj_delete.delete()
                except:
                    pass
        # Deleting old image from data when adding new one
        if self.request.FILES:
            for files in list(self.request.FILES):
                if files == 'poster':
                    self.object.poster.delete()
                elif 'step' in files:
                    for steps in [form.cleaned_data for form in instruction_form.ordered_forms]:
                        if steps['image']:
                            try:
                                step = self.object.step_set.get(id=steps['id'].id)
                                step.image.delete()
                            except: pass
        if [form.cleaned_data for form in instruction_form.deleted_forms]:
            for steps in [form.cleaned_data for form in instruction_form.deleted_forms]:
                try:
                    step = self.object.step_set.get(id=steps['id'].id)
                    step.image.delete()
                except:
                    pass
        if form.is_valid() and ingredient_form.is_valid() and instruction_form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form, ingredient_form, instruction_form)

    def form_valid(self, form):
        user = get_object_or_404(User, id=self.request.user.id)
        self.object = self.get_object()
        contex = self.get_context_data()
        base_form = contex['form']
        ingredient_form = contex['ingredient_form']
        instruction_form = contex['instruction_form']
        if base_form.is_valid() and ingredient_form.is_valid() and instruction_form.is_valid():
            base_form.save()
            ingredient_form.save()
            instruction_form.save()
            if base_form.instance.draft:
                return HttpResponseRedirect(user.profile.get_personal_absolute_url())
            messages.success(self.request,'Спасибо за участие! Ваш рецепт будет добавлен на сайт после прохождения модерации.')
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self)

    def form_invalid(self, form, ingredient_form, instruction_form):
        messages.error(self.request, 'Исправте ниже указанные ошибки')
        return self.render_to_response(
            self.get_context_data(form=form,
                                  ingredient_form=ingredient_form,
                                  instruction_form=instruction_form)
        )


class DishDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Dish
    template_name = 'culinary_recipe/recipe_delete.html'

    def get_success_url(self):
        return self.request.user.profile.get_personal_absolute_url()


def get_ajax_response_category(request):
    category_id = request.GET.get('category_id')
    sub_category = SubCategory.objects.filter(category_id=category_id)
    return JsonResponse(list(sub_category.values('id', 'name')), safe=False)


def ingredient_list_view(request):
    ings = set(list(Ingredient.objects.all().values_list('name', flat=True)))
    return JsonResponse(list(ings), safe=False)
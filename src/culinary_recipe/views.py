from PIL import Image
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q, Count
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator

from django.views.generic.base import View
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from hitcount.models import HitCount
from hitcount.views import HitCountMixin
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Dish, Country, Category, SubCategory, DishLike, IngredientList, Step, IngredientTitle
from culinary_post.models import CulinaryPost
from .forms import DishCommentForm, DishForm, InstructionFormSet, IngredientNestedFormSet
from .utils import getMonth
from contact.models import UserProfile


def watermark_photo(input_image_path,
                    output_image_path,
                    watermark_image_path,
                    position):
    base_image = Image.open(input_image_path)
    watermark = Image.open(watermark_image_path)
    width, height = base_image.size
    transparent = Image.new('RGB', (width, height), (0,0,0,0))
    transparent.paste(base_image, (0,0))
    transparent.paste(watermark, position, mask=watermark)
    transparent.save(f'{settings.MEDIA_ROOT}/{output_image_path}')


class CategoryViewList(ListView):
    """Вывод категорий"""
    model = Category
    template_name = 'home.html'
    context_object_name = 'categories'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        country = Country.objects.annotate(cnt=Count('dish'))
        has_dish_country = []
        for con in country:
            if con.dish_set.filter(moderator=True):
                has_dish_country.append(con)
        context['countries'] = has_dish_country
        context['posts'] = CulinaryPost.objects.all().filter(moderator=True).order_by('-created')[:8]
        context['popular_meals'] =  Dish.objects.order_by('-hit_count_generic__hits').filter(moderator=True, draft=False)[:12]
        return context


def get_sub_category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    sub_category = SubCategory.objects.filter(category=category).annotate(cnt=Count('dish'))
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
        paginator = Paginator(meal, 10)

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
    def get(self, request, slug, pk):
        # countr = Country.objects.prefetch_related('dish_set').get(slug=slug, id=pk)
        country = get_object_or_404(Country, slug=slug, id=pk)
        meals = Dish.objects.filter(country=country, moderator=True, draft=False)
        return render(request, 'culinary_recipe/dishes_list.html', {'meals': meals, 'country': country})


class Search(ListView):
    template_name = 'culinary_recipe/dishes_list.html'

    def get_queryset(self):
        q = self.request.GET.get('q')
        meals = Dish.objects.filter(
            Q(ingredienttitle__ingredientlist__name__icontains=q) | Q(title__icontains=q)).distinct()
        return meals

    def get_context_data(self,  *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['meals'] = self.get_queryset()
        return context


class MealDetailView(DetailView):
    """Вывод деталей рецепта"""
    model = Dish
    template_name = 'culinary_recipe/meal_detail.html'

    def get(self, request, *args, **kwargs):
        meal = get_object_or_404(Dish, slug=self.kwargs.get('slug'), id=self.kwargs.get('pk'))
        hit_count = HitCount.objects.get_for_object(meal)
        hit_count_response = HitCountMixin.hit_count(request, hit_count)
        meal_ings_list = []
        for ingredient in meal.ingredienttitle_set.all():
            meal_ings_list += set(ingredient.ingredientlist_set.all().values_list('name', flat=True))
        similar_meals = Dish.objects.filter(ingredienttitle__ingredientlist__name__in=meal_ings_list, moderator=True, draft=False).exclude(id=self.kwargs.get('pk')).distinct()[:8]
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
                   'popular_meals': Dish.objects.order_by('-hit_count_generic__hits').filter(moderator=True, draft=False)[:8]
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
        ingredient_title_form = IngredientNestedFormSet()
        instruction_form = InstructionFormSet()
        return self.render_to_response(
            self.get_context_data(form=form,
                                  ingredient_title_form=ingredient_title_form,
                                  instruction_form=instruction_form,
                                  )
        )

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        ingredient_title_form=IngredientNestedFormSet(self.request.POST)
        instruction_form = InstructionFormSet(self.request.POST, self.request.FILES)
        if form.is_valid() and ingredient_title_form.is_valid() and instruction_form.is_valid():
            return self.form_valid(form, ingredient_title_form, instruction_form)
        else:
            # messages.error(request, 'Исправте ниже указанные ошибки')
            return self.form_invalid(form, ingredient_title_form, instruction_form)

    def form_valid(self, form, ingredient_title_form, instruction_form):
        user = get_object_or_404(User, id=self.request.user.id)
        form.instance.author = user
        self.object = form.save()
        ingredient_title_form.instance = self.object
        ingredient_title_form.save()
        instruction_form.instance = self.object
        instruction_form.save()
        watermark_photo(form.instance.poster, str(form.instance.poster), 'static/image/logo_header.png', position=(10, 10))
        for steps_image in instruction_form:
            if steps_image.instance.image:
                watermark_photo(steps_image.instance.image, str(steps_image.instance.image), 'static/image/logo_header.png', position=(10, 10))
        if form.instance.draft:
            return HttpResponseRedirect(user.profile.get_personal_absolute_url())
        messages.success(self.request, 'Спасибо за участие! Ваш рецепт будет добавлен на сайт после прохождения модерации.')
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, ingredient_title_form, instruction_form):
        return self.render_to_response(
            self.get_context_data(form=form, ingredient_title_form=ingredient_title_form,
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
             context['ingredient_title_form'] = IngredientNestedFormSet(self.request.POST, instance=self.object)
             context['instruction_form'] = InstructionFormSet(self.request.POST, self.request.FILES, instance=self.object)
         else:
             if not self.request.user == self.object.author:
                 context['error_message'] = "Ты не можешь изменять рецепты чужих пользователей"
             else:
                context['form'] = DishForm(instance=self.object)
                context['ingredient_title_form'] = IngredientNestedFormSet(instance=self.object)
                context['instruction_form'] = InstructionFormSet(instance=self.object)
         return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        ingredient_nested_form = IngredientNestedFormSet(self.request.POST, instance=self.object)
        instruction_form = InstructionFormSet(self.request.POST, self.request.FILES, instance=self.object)
        if form.is_valid() and ingredient_nested_form.is_valid() and instruction_form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form, ingredient_nested_form, instruction_form)

    def form_valid(self, form):
        user = get_object_or_404(User, id=self.request.user.id)
        self.object = self.get_object()
        contex = self.get_context_data()
        base_form = contex['form']
        ingredient_nested_form = contex['ingredient_title_form']
        instruction_form = contex['instruction_form']
        if base_form.is_valid() and ingredient_nested_form.is_valid() and instruction_form.is_valid():
            base_form.save()
            ingredient_nested_form.save()
            instruction_form.save()
            if self.request.FILES:
                if 'poster' in self.request.FILES:
                    watermark_photo(base_form.instance.poster, str(base_form.instance.poster), 'static/image/logo_header.png',
                                    position=(10, 10))

                for value, items in self.request.FILES.items():
                    if 'step' in value:
                        for steps_image in instruction_form:
                            if steps_image.instance.image:
                                watermark_photo(steps_image.instance.image, str(steps_image.instance.image), 'static/image/logo_header.png',
                                        position=(10, 10))
            if base_form.instance.draft:
                return HttpResponseRedirect(user.profile.get_personal_absolute_url())
            messages.success(self.request, 'Спасибо за участие! Ваш рецепт будет добавлен на сайт после прохождения модерации.')
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self)

    def form_invalid(self, form, ingredient_nested_form, instruction_form):
        messages.error(self.request, 'Исправте ниже указанные ошибки')
        return self.render_to_response(
            self.get_context_data(form=form,
                                  ingredient_title_form=ingredient_nested_form,
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
    ings = set(list(IngredientList.objects.all().values_list('name', flat=True)))
    return JsonResponse(list(ings), safe=False)


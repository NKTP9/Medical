from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import Http404
from django.shortcuts import redirect, render

from .forms import ProfileForm, UserForm
# Create your views here.
from .models import *


def archive(request):
    return render(request, 'archive.html', {"posts": Article.objects.all()})

def main(request):
    return render(request, 'main.html')

def profile(request):
    return render(request, 'profile.html')

def doctors(request):
    return render(request, 'doctors.html')

def hospitals(request):
    return render(request, 'hospitals.html')

def get_article(request, article_id):
    try:
        post = Article.objects.get(id=article_id)
        return render(request, 'article.html', {"post": post})
    except Article.DoesNotExist:
        raise Http404


def create_post(request):
    # if not request.user.is_anonymous():
    if request.user.is_authenticated:
        # Здесь будет основной код представления
        if request.method == "POST":
            # обработать данные формы, если метод POST
            form = {
                'text': request.POST["text"], 'title': request.POST["title"]
            }
            # в словаре form будет храниться информация, введенная пользователем
            if form["text"] and form["title"] and not Article.objects.filter(title=form["title"]).exists():
                # если поля заполнены без ошибок
                Article.objects.create(text=form["text"], title=form["title"], author=request.user)
                return redirect('get_article', article_id=Article.objects.get(text=form["text"], title=form["title"],
                                                                              author=request.user).id)
                # перейти на страницу поста
            else:
                # если введенные данные некорректны
                if Article.objects.filter(title=form["title"]).exists() and not (form["text"] and form["title"]):
                    form['errors'] = u"Название статьи не уникально!\nНе все поля заполнены!"
                elif Article.objects.filter(title=form["title"]).exists():
                    form['errors'] = u"Название статьи не уникально!"
                else:
                    # print(form['errors'])
                    form['errors'] = u"Не все поля заполнены!"
                # print(Article.objects.filter(title='dsfsf').exists())
                return render(request, 'create_post.html', {'form': form})
        else:
            # просто вернуть страницу с формой, если метод GET
            return render(request, 'create_post.html', {})
    else:
        raise Http404


def registerPage(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        user_form = UserForm()
        profile_form = ProfileForm()
        if request.method == 'POST':
            user_form = UserForm(request.POST, instance=request.user)
            profile_form = ProfileForm(request.POST, instance=request.user.profile)
            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                profile_form.save()
                user = user_form.cleaned_data.get('username')
                return redirect('login')
            else:
                messages.error(request, "Неудачная регистрация. Неверная информация")

    context = {'user_form': user_form, 'profile_form': profile_form}
    return render(request, 'register.html', context)


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                messages.info(request, 'Имя пользователя или пароль неверны!')

        context = {}
        return render(request, 'login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')


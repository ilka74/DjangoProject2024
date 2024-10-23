# В этом файле определены функции представления Django, содержащие логику обработки запросов пользователя

# Первый блок - импорты библиотек и форм из других модулей:
from django.shortcuts import render, redirect  # для визуализации шаблонов и перенаправления пользователей на разные страницы
from board.models import Advertisement  # модель, представляющая рекламные объявления в базе данных
from board.forms import AdvertisementForm, SignUpForm  # формы для создания/редактирования рекламных объявлений и регистрации пользователей
from django.contrib.auth.decorators import login_required  # встроенный декоратор Django.
# Он используется для ограничения доступа к представлениям и требует, чтобы пользователь прошел аутентификацию.
# Если пользователь не вошел в систему, он будет перенаправлен на страницу входа.

from django.contrib.auth import login, logout, authenticate  # функции для обработки аутентификации пользователей.
from django.shortcuts import get_object_or_404  # вспомогательная функция, используется для получения запроса
# из базы данных. Если объект не найден, автоматически выдается ошибка 404 (применяется для упрощения кода).


def logout_view(request):  # Выход пользователя из системы и перенаправление на домашнюю страницу
    logout(request)
    return redirect('home')


def signup(request):
    """
    Функция для управления регистрацией пользователей.
    Если метод запроса — POST, он обрабатывает отправленную форму.
    Если форма действительна, она сохраняет пользователя, авторизует его и перенаправляет на страницу доски.
    Если метод запроса — GET, отображается пустая форма регистрации
    """
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/board')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form}) # возвращает страницу регистрации с формой


def home(request):
    # функция для отображения домашней страницы
    return render(request, 'home.html')


def advertisement_list(request):
    # Функция для отображения списка всех рекламных объявлений
    advertisements = Advertisement.objects.all()
    return render(request, 'board/advertisement_list.html', {'advertisements': advertisements})


def advertisement_detail(request, pk):
    # Функция для отображения деталей конкретного объявления (первичный ключ объявления и подробности рекламы)
    advertisement = Advertisement.objects.get(pk=pk)
    return render(request, 'board/advertisement_detail.html', {'advertisement': advertisement})


@login_required
# Данный декоратор гарантирует, что доступ к этому представлению получат только аутентифицированные пользователи
def add_advertisement(request):
    """
    Функция позволяет добавлять новое объявление.
    Если метод запроса - "POST", то он обрабатывает отправленную форму.
    Если форма действительна, она связывает рекламу с текущим пользователем и сохраняет ее.
    После сохранения перенаправляет на список объявлений.
    Если метод запроса — "GET", то отображается пустая форма.
    """
    if request.method == "POST":
        form = AdvertisementForm(request.POST)
        if form.is_valid():
            advertisement = form.save(commit=False)
            advertisement.author = request.user
            advertisement.save()
            return redirect('board:advertisement_list')
    else:
        form = AdvertisementForm()
    return render(request, 'board/add_advertisement.html', {'form': form})


@login_required
def edit_advertisement(request, pk):
    advertisement = get_object_or_404(Advertisement, pk=pk)
    # Извлекает объявление с заданным первичным ключом или возвращает ошибку 404, если оно не найдено.
    if advertisement.author != request.user:
        # Проверяет, является ли текущий пользователь автором объявления.
        return redirect('board:advertisement_list')
        # Если нет, перенаправляет на список объявлений.

    if request.method == 'POST':
        form = AdvertisementForm(request.POST, instance=advertisement)
        # Создает форму с данными из запроса и существующим объявлением.
        if form.is_valid():
            form.save()
            return redirect('board:advertisement_detail', pk=advertisement.pk)
    else:
        form = AdvertisementForm(instance=advertisement)
        # Если метод запроса не POST, инициализирует форму с данными объявления.

    return render(request, 'board/edit_advertisement.html', {'form': form})

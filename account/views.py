import os

from datetime import date

from django.db.models import Q
from django.forms.utils import ErrorList
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.utils import timezone
from django.contrib.auth import authenticate
from django.views.decorators.http import require_GET, require_POST

from .models import CustomUser, Wall, Message, File
from .forms import RegistrationForm, AuthForm, WallForm, MessageForm, FileForm, AvatarForm, UserIdForm, FileIdForm


def user_auth(request):
    token = request.headers.get('Authorisation')
    user = CustomUser.objects.filter(id=token).first()
    request.user = user


@require_POST
def login_action(request):
    form = AuthForm(request.POST)
    form_data = form.data.dict()
    if form.is_valid():
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        user = authenticate(email=email, password=password)
        if user is not None:
            return JsonResponse({'success': True, 'token': user.id, 'avatar_url': user.avatar_url()})
        form.add_error("", "Введён неправильный логин или пароль.")
        return JsonResponse({'success': False, 'form': form_data, 'validate_errors': form.errors})
    return JsonResponse({'success': False, 'form': form_data, 'validate_errors': form.errors})


@require_POST
def registration(request):
    form = RegistrationForm(request.POST)
    form_data = form.data.dict()
    if form.is_valid():
        birthday = form.cleaned_data['birthday']
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        errors = {}
        is_user_adult = (timezone.now().date() - birthday).days / 365 > 12

        if not is_user_adult:
            errors['birthday'] = ErrorList(['Вам должно быть не меньше 12 лет'])

        is_email_exist = CustomUser.objects.filter(email=email).exists()
        if is_email_exist:
            errors['email'] = ErrorList(['Пользователь с таким адресом почты уже зарегистрирован'])

        if not is_email_exist and is_user_adult:
            user = CustomUser(first_name=form.cleaned_data['first_name'], last_name=form.cleaned_data['last_name'],
                              middle_name=form.cleaned_data['middle_name'],
                              birthday=birthday,
                              email=email, password=password, sex=form.cleaned_data['sex'])
            user.set_password(password)
            user.save()
            return JsonResponse({'success': True, 'token': user.id})

        data = {'success': False, 'form': form_data, 'validate_errors': form.errors, 'errors': errors}
        return JsonResponse(data)
    else:
        return JsonResponse({'success': False, 'form': form_data, 'validate_errors': form.errors})


@require_GET
def account(request):
    user_auth(request)
    if not request.user.is_authenticated:
        return JsonResponse({'success': False})
    else:
        return JsonResponse({'success': True, 'user': request.user.dict()})


@require_POST
def account_exit(request):
    return JsonResponse({'success': True})


@require_POST
def wall_entries_list(request):
    user_auth(request)
    if not request.user.is_authenticated:
        return JsonResponse({'success': False})

    form = UserIdForm(request.POST)
    if not form.is_valid():
        return JsonResponse({'success': False})

    u = CustomUser.objects.get(pk=form.cleaned_data['user_id'])
    entries = u.wall_set.all()
    wall_c = []
    for entry in entries:
        wall_c.append(entry.dict())
    if len(entries) == 0:
        return JsonResponse({'success': False, 'empty': True})

    return JsonResponse({'success': True, 'entries': wall_c})


@require_POST
def wall_add_entry(request):
    user_auth(request)
    if not request.user.is_authenticated:
        return JsonResponse({'success': False})

    form = WallForm(request.POST)
    if form.is_valid():
        title = form.cleaned_data['title']
        text = form.cleaned_data['text']
        sender = request.user
        n_wall = Wall(title=title, text_message=text, sender=sender)
        n_wall.save()
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'form': form.data.dict(), 'validate_errors': form.errors})


@require_GET
def friends_list(request):
    user_auth(request)
    if not request.user.is_authenticated:
        return JsonResponse({'success': False})
    else:
        user = CustomUser.objects.get(pk=request.user.id)
        friends_c = []
        for friend in user.friends.all():
            friends_c.append(friend.dict())
        return JsonResponse({'success': True, 'friends': friends_c})


@require_GET
def friends_potential_list(request):
    user_auth(request)
    if not request.user.is_authenticated:
        return JsonResponse({'success': False})
    else:
        user = CustomUser.objects.get(pk=request.user.id)
        potential_friends = []
        for users in CustomUser.objects.exclude(id__in=user.friends.values('id')).exclude(id=user.id):
            potential_friends.append(users.dict())
        return JsonResponse({'success': True, 'users': potential_friends})


@require_POST
def friends_add_user(request):
    user_auth(request)
    if not request.user.is_authenticated:
        return JsonResponse({'success': False})
    else:
        form = UserIdForm(request.POST)
        if not form.is_valid():
            return JsonResponse({'success': False})
        user = CustomUser.objects.get(pk=request.user.id)
        friend = CustomUser.objects.get(pk=form.cleaned_data['user_id'])
        user.friends.add(friend)
        friend.friends.add(user)
        return JsonResponse({'success': True})


@require_POST
def friends_delete_user(request):
    user_auth(request)
    if not request.user.is_authenticated:
        return JsonResponse({'success': False})
    else:
        form = UserIdForm(request.POST)
        if not form.is_valid():
            return JsonResponse({'success': False})
        user = CustomUser.objects.get(pk=request.user.id)
        friend = CustomUser.objects.get(pk=form.cleaned_data['user_id'])
        user.friends.remove(friend)
        friend.friends.remove(user)
        return JsonResponse({'success': True})


class MessagesList:
    def __init__(self, messages: list, messages_date: date):
        self.messages = messages
        self.date = messages_date

    def append(self, message: Message):
        self.messages.append(message)

    def dict(self):
        return {
            'messages': [m.dict() for m in self.messages],
            'date': self.date
        }


@require_POST
def get_messages(request):
    user_auth(request)
    if not request.user.is_authenticated:
        return JsonResponse({'success': False})

    form = UserIdForm(request.POST)
    if not form.is_valid():
        return JsonResponse({'success': False})

    sender = CustomUser.objects.get(pk=request.user.id)
    recipient = CustomUser.objects.get(pk=form.cleaned_data['user_id'])
    messages = Message.objects.filter(
        Q(sender_id=sender.id, recipient_id=recipient.id) | Q(recipient_id=sender.id,
                                                              sender_id=recipient.id)).order_by('message_date')
    messages_list = []
    if len(messages) > 0:
        f_date = messages.first().message_date.date()
    else:
        f_date = None
    date_list = MessagesList([], f_date)
    for i in messages:
        if i.message_date.date() == f_date:
            date_list.append(i)
        else:
            messages_list.append(date_list)
            f_date = i.message_date.date()
            date_list = MessagesList([], f_date)
            date_list.append(i)
    messages_list.append(date_list)

    return JsonResponse({'success': True, 'messages': [ml.dict() for ml in messages_list]})


@require_POST
def send_messages(request):
    user_auth(request)
    if not request.user.is_authenticated:
        return JsonResponse({'success': False})

    form_user_id = UserIdForm(request.POST)
    if not form_user_id.is_valid():
        return JsonResponse({'success': False})

    form_message = MessageForm(request.POST)
    if form_message.is_valid():
        text = form_message.cleaned_data['text']
        n_message = Message(text_message=text, recipient_id=form_user_id.cleaned_data['user_id'],
                            sender_id=request.user.id)
        n_message.save()
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'validate_errors': form_message.errors})


@require_GET
def get_files(request):
    user_auth(request)
    if not request.user.is_authenticated:
        return JsonResponse({'success': False})

    user = CustomUser.objects.get(pk=request.user.id)
    files = user.file_set.all()
    files_c = []
    for i in files:
        files_c.append(i.dict())
    if len(files) == 0:
        return JsonResponse({'success': False, 'empty': True})

    return JsonResponse({'success': True, 'files': files_c})


@require_POST
def upload_file(request):
    user_auth(request)
    if not request.user.is_authenticated:
        return JsonResponse({'success': False})

    form = FileForm(request.POST, request.FILES)
    if form.is_valid():
        name = form.cleaned_data['name']
        n_file = File(name=name, file=request.FILES['new_file'], owner_id=request.user.id,
                      content_type=request.FILES['new_file'].content_type, is_image=False)
        n_file.save()
        file_extension = n_file.file.name.split(".")[-1]
        extension = {'png', 'jpg', 'gif', 'bmp'}

        if file_extension in extension:
            n_file.is_image = True
            n_file.save(update_fields=["is_image"])
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'validate_errors': form.errors})


@require_GET
def download_file(request, file_id):
    # user_auth(request)
    # if not request.user.is_authenticated:
    #     return JsonResponse({'success': False})

    file = File.objects.get(id=file_id)
    c_t = file.content_type
    response = HttpResponse(open("./media/" + file.file.name, 'rb').read(), content_type=c_t)
    response['Content-Disposition'] = 'attachment; filename=' + file.pure_name
    return response


@require_POST
def delete_file(request):
    user_auth(request)
    if not request.user.is_authenticated:
        return JsonResponse({'success': False})

    form_file_id = FileIdForm(request.POST)
    if not form_file_id.is_valid():
        return JsonResponse({'success': False})

    file = File.objects.get(id=form_file_id.cleaned_data['file_id'])
    os.remove("./media/" + str(file.file))
    file.delete()
    return JsonResponse({'success': True})


@require_POST
def change_avatar(request):
    user_auth(request)
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/')

    form = AvatarForm(request.POST, request.FILES)
    if form.is_valid():
        user = CustomUser.objects.get(pk=request.user.id)
        user.avatar = request.FILES['new_avatar']
        user.save(update_fields=["avatar"])
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'validate_errors': form.errors})

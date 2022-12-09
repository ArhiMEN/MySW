from django import forms

from django.core.exceptions import ValidationError
from django.forms.utils import ErrorList
from django.utils.translation import gettext_lazy as _


def validate_string(value):
    if not all(map(str.isalpha, value)):
        raise ValidationError(
            _('Введены недопустимые символы.')
        )


class RegistrationForm(forms.Form):
    first_name = forms.CharField(max_length=20, validators=[validate_string])
    last_name = forms.CharField(max_length=20, validators=[validate_string])
    middle_name = forms.CharField(max_length=25, required=False, validators=[validate_string])
    birthday = forms.DateField()
    email = forms.EmailField()
    password = forms.CharField(max_length=20)
    password2 = forms.CharField(max_length=20)
    sex = forms.CharField(max_length=7)

    def password_matched(self):
        if self.data['password'] != self.data['password2']:
            self.errors['password'] = ErrorList(['Пароли не совпадают'])
            return False
        else:
            return True

    def is_valid(self):
        valid = super(RegistrationForm, self).is_valid()
        password_matched = self.password_matched()
        if valid and password_matched:
            return True
        else:
            return False


class AuthForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(max_length=20)


class WallForm(forms.Form):
    title = forms.CharField(max_length=30)
    text = forms.CharField(widget=forms.Textarea)


class MessageForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea)


class FileForm(forms.Form):
    name = forms.CharField(max_length=30)
    new_file = forms.FileField()


class AvatarForm(forms.Form):
    new_avatar = forms.FileField()


class UserIdForm(forms.Form):
    user_id = forms.IntegerField(min_value=1)


class FileIdForm(forms.Form):
    file_id = forms.IntegerField(min_value=1)

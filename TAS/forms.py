from django.contrib.auth.forms import UserCreationForm

from .models import User

"""
class AddUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email')

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'email')
"""


class AddUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email',
                  'password1',
                  'password2',
                  'full_name',
                  'pernr',
                  'document_id',
                  'position',
                  'is_boss',
                  'avatar']


class ChangeDataUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['password1',
                  'password2',
                  'full_name',
                  'user_phone_num',
                  'birth_date']

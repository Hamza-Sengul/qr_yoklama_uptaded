from django.contrib.auth.forms import UserCreationForm
from .models import AcademicUser

class AcademicUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = AcademicUser
        fields = ('username', 'email')
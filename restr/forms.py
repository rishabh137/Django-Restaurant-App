from django.forms import ModelForm
from zxcvbn import zxcvbn
from django.contrib.auth.forms import UserCreationForm
from django.core import validators

# from django import forms
from django.contrib.auth.models import User
from django import forms


def validate_password(password1):
    pass
    # result = int(zxcvbn(password1)["score"])
    # if result > 0:
    #     review = "Laura ka password hai"
    #     print(result["score"])
    #     print(review)


# class CreateUserForm(forms.Form, forms.ModelForm):
# username = forms.CharField(min_length=4)
# email = forms.EmailField()
# password1 = forms.CharField(
#     widget=forms.PasswordInput, min_length=4, validators=[validate_password]
# )


# password2 = forms.CharField(
#     widget=forms.PasswordInput, min_length=4, validators=[validate_password]
# )
class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    # def clean(self):
    #     password = self.cleaned_data.get("password1")

    #     if password:
    #         score = zxcvbn(password)["score"]

    #     # return self.cleaned_data[score]

    # def clean_email(self):
    #     # print(self.cleaned_data)
    #     return self.cleaned_data["email"].lower()

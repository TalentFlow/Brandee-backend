from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django import forms
from .models import User



class UserCreationForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput())
    confirm_password=forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('email',)

    def clean(self):
        cleaned_data = super(UserCreationForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError(
                "password and confirm_password does not match"
            )

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class CustomUserAdmin(UserAdmin):
    # The forms to add and change user instances
    add_form = UserCreationForm
    list_display = ("email",)
    search_fields=['email',]
    ordering = ("email",)

    fieldsets = (
        (None, {'fields': ('email',  'first_name', 'last_name', 'password', 'is_superuser', 'is_staff', 'is_active')}),
        )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email','first_name', 'last_name', 'password','confirm_password',  'is_superuser', 'is_staff', 'is_active')}
            ),
        )

    filter_horizontal = ()



admin.site.register(User, CustomUserAdmin)



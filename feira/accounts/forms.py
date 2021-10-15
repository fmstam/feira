from django.contrib.auth.signals import user_logged_in
from django.core.exceptions import ValidationError
from django.forms import EmailField, fields
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User



class BasicRegistrationForm(UserCreationForm):
    """
        A typical basic registration form
    """

    email = EmailField(required=True, label='Your email address')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    
    def save(self, commit=True):
        # create but do not save
        new_user =   super(BasicRegistrationForm, self).save(commit=False)
        # add the email address field
        new_user.email = self.cleaned_data["email"]
        # commit?
        if commit:
            new_user.save()

        return new_user

class BasicAuthenticationForm(AuthenticationForm):
    
    """
        A typical basic registration form
    """
    def confirm_login_allowed(self, user):
        """
        Allow active users only
        """
        if not user.is_active:
            raise ValidationError(("This account is inactive."),
                code='inactive',)
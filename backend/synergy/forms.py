from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _
from .models import CustomUser, Product, Request, Business


# Custom fields

class NameField(forms.CharField):

    def to_python(self, value):
        """ Remove extra spaces in input. """

        if value not in self.empty_values:
            value = str(value)

            if self.strip:
                value = value.strip()

            if '  ' in value:
                value = normalize_spaces(value)

        if value in self.empty_values:
            return self.empty_value

        return value


# Forms

class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ['name', 'quantity', 'cost']

    name = NameField(max_length=30)


class RequestForm(forms.ModelForm):

    class Meta:
        model = Request
        fields = ['name', 'quantity', 'min_budget', 'max_budget',
                  '_min_quality']
        labels = {'_min_quality': 'Min quality'}

    name = NameField(max_length=30)


class RegistrationForm(UserCreationForm):
    """ Form for account registration. """

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)

        self.fields['email'].label = 'Email'
        self.fields['password1'].help_text = None

        self.fields['first_name'].widget.attrs = {'id': 'first-name',
                                                  'placeholder': 'First Name'}
        self.fields['last_name'].widget.attrs = {'id': 'last-name',
                                                 'placeholder': 'Last Name'}
        self.fields['email'].widget.attrs = {'placeholder': 'Email Address'}
        self.fields['password1'].widget.attrs = {'placeholder': 'Password'}

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email')

    first_name = NameField()  # Default max_length of 30
    last_name = NameField(max_length=45)
    password2 = None  # Disable second password field


class InfoForm(ModelForm):
    """ Form for filling out additional user information. """

    def __init__(self, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)

        for field in ('website', 'postal_code'):
            self.fields[field].required = False

        for field in ('industry', 'name', 'country'):
            self.fields[field].label_suffix = '*'

        self.fields['name'].label = 'Company name'
        self.fields['website'].label = 'Company website'

    class Meta:
        model = Business
        fields = ('name', 'country', 'industry', 'postal_code', 'website')

    job_title = forms.CharField(
        max_length=30,
        label_suffix='*'
    )

    job_function = forms.ChoiceField(
        choices=CustomUser.JOB_FUNCTION_CHOICES,
        label_suffix='*'
    )


class LoginForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Email Address'
        self.fields['password'].widget.attrs['placeholder'] = 'Password'

    error_messages = {
        'invalid_login': _(
            'Wrong password. Try again.'
        ),
    }


# Misc. functions

def normalize_spaces(text: str) -> str:

    if '  ' not in text:
        return text

    else:

        while '  ' in text:
            text = text.replace('  ', ' ')

        return text

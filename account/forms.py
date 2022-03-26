from dataclasses import field
import email
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.utils.translation import gettext_lazy as _
from django.forms import EmailInput
from django import forms


from account.models import Account, UserConfirmCode


class RegistrationForm(UserCreationForm, forms.ModelForm):
	username = forms.CharField(
		label=_("User Name"),
		error_messages={'required': 'Please let us know what to call you!'},
		help_text='Required',
	)
	email = forms.EmailField(
		label=_("Email"),
		required=True,
		error_messages = {'required': _('Email is might be already exist.')},
		widget=EmailInput(attrs={'autocomplete': 'new-password'}),
	)
	password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
		error_messages={'required': 'Your password is not passed validation!'},
	)
	password2 = forms.CharField(
		label=_("Password confirmation"),
		strip=False,
		widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
		error_messages={'required': 'Your password should be the same as before!'},
	)

	class Meta(UserCreationForm.Meta):
		model = Account
		fields = ('username', 'email', 'password1', 'password2')

	def __init__(self, *args, **kwargs) -> None:
		super(RegistrationForm, self).__init__(*args, **kwargs)
		self.fields['username'].widget.attrs.update({'class':'login__input','placeholder':'Enter Username'})
		self.fields['email'].widget.attrs.update({'class':'login__input','placeholder':'Enter email'})
		self.fields['password1'].widget.attrs.update({'class':'login__input','placeholder':'Enter password'})
		self.fields['password2'].widget.attrs.update({'class':'login__input','placeholder':'Enter password confirmation'})


class UserForm(AuthenticationForm):
	email = forms.CharField(widget=forms.TextInput(attrs={ "autofocus": True}))

	password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}),
    )

	error_messages = {
        'invalid_login': _(
            "Please enter a correct %(email)s and password. Note that both "
            "fields may be case-sensitive."
        ),
        'inactive': _("This account is inactive."),
    }
	class Meta:
		model = Account
		fields = ('email', 'password')
	def __init__(self, *args, **kwargs):
		super(UserForm,self).__init__(*args,**kwargs)
		self.fields.pop('username')
		self.fields['email'].widget.attrs.update({'class':'login__input','placeholder':'Email or Username'})
		self.fields['password'].widget.attrs.update({'class':'login__input','placeholder':'Password'})

class LoginConfirmForm(forms.Form):

	code = forms.IntegerField(
		label=_("Input your code"),
        widget=forms.NumberInput(),
	)
	field=('code')
	
	def __init__(self, *args, **kwargs):
			super(LoginConfirmForm,self).__init__(*args,**kwargs)
			self.fields['code'].widget.attrs.update({'class':'login__input','placeholder':'Code'})
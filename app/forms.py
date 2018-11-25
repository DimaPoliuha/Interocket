from django import forms
from django.utils import timezone
from django.contrib.auth.models import User


class RegistrationForm(forms.ModelForm):
    password_check = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password',
        ]
        labels = {
            'username': 'Username',
            'password': 'Password',
            'first_name': 'First name',
            'last_name': 'Last name',
            'email': 'Email',
        }
        help_texts = {
            'username': '',
        }
        widgets = {
            'password': forms.PasswordInput(),
        }

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['password_check'].label = 'Repeat password'

    def clean(self):
        username = self.cleaned_data['username']
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']
        password_check = self.cleaned_data['password_check']

        if not password == password_check:
            raise forms.ValidationError({
                'password': '',
                'password_check': "Passwords don't match"},
                code='passwords do not match')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError({
                'username': 'User exists'},
                code='user exists')
        if User.objects.filter(email=email).exists() and email:
            raise forms.ValidationError({
                'email': 'Email exists'},
                code='email exists')


class LoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = [
            'username',
            'password',
        ]
        labels = {
            'username': 'Username',
            'password': 'Password',
        }
        help_texts = {
            'username': '',
        }
        widgets = {
            'password': forms.PasswordInput(),
        }

    # def __init__(self, *args, **kwargs):
    #     super(LoginForm, self).__init__(*args, **kwargs)

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']

        if User.objects.filter(username=username).exists():
            if not User.objects.get(username=username).check_password(password):
                raise forms.ValidationError({
                    'password': "Wrong password"},
                    code='wrong password')
        else:
            raise forms.ValidationError({
                'username': "User doesn't exists"},
                code='user not exists')


class OrderForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    phone = forms.CharField()
    date = forms.DateField(widget=forms.SelectDateWidget(), initial=timezone.now())
    address = forms.CharField(required=False)
    comment = forms.CharField(widget=forms.Textarea, required=False)

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].label = 'Name'
        self.fields['last_name'].label = 'Surname'
        self.fields['phone'].label = 'Mobile phone'
        self.fields['phone'].help_text = 'Input real phone number'
        self.fields['address'].label = 'Your address'
        self.fields['address'].help_text = 'Specify planet'
        self.fields['comment'].label = 'Comments to your order'
        self.fields['date'].label = 'Delivery date'
        self.fields['date'].help_text = 'Not earlier than tomorrow'

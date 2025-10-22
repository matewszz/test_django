from django import forms


class LoginForm(forms.Form):

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={'type': 'email', 'placeholder': 'Type your email'}
        )
    )

    password = forms.CharField(
        widget=forms.PasswordInput()
    )
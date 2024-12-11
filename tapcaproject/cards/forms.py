from django import forms


class CheckCardForm(forms.Form):
    word = forms.CharField(
        widget=forms.TextInput(attrs={
            'class':'form-control fs-7',
            'placeholder':'Введите перевод...',
            'autofocus': True,
            'onkeydown': "if (event.keyCode === 13) event.preventDefault();"
        }),
        label=''
    )

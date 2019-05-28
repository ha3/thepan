from django import forms

class ContactForm(forms.Form):
    full_name = forms.CharField(
        required = True,
        label = 'İsim',
        max_length = 60
    )

    sender = forms.EmailField(
        required = True,
        label='E-posta'
    )

    subject = forms.CharField(
        required = True,
        label='Konu',
        max_length=100
    )

    message = forms.CharField(
        required = True,
        label='Mesajınız',
        widget=forms.Textarea(attrs={'class': 'form-control'})
    )

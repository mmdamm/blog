from django import forms
from .models import *


class TicketForm(forms.Form):
    SUBJECT_CHOICES = (
        ("Report", "Report"),
        ("Problem", "Problem"),
        ("Advice", "Advice"),
    )

    message = forms.CharField(
        widget=forms.Textarea and forms.TextInput(attrs={'placeholder': 'Massage', 'class': 'ticketmassage'}),
        required=True, )
    name = forms.CharField(max_length=250, required=True, widget=forms.TextInput(attrs={'placeholder': 'Name'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    phone = forms.CharField(max_length=11, required=True, widget=forms.NumberInput(attrs={'placeholder': 'Phone'}))
    subject = forms.ChoiceField(choices=SUBJECT_CHOICES)

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if phone:
            if not phone.isnumeric():
                raise forms.ValidationError('Error:Number isnt valid!!! ')
            else:
                return phone


class CommentForm(forms.ModelForm):
    def clean_name(self):
        name = self.cleaned_data['name']
        if name:
            if len(name) < 3:
                raise forms.ValidationError("name is short!!!")
            else:
                return name

    class Meta:

        model = Comment
        fields = ['name', 'body']
        widgets = {
            'body': forms.TextInput(attrs={
                'placeholder': 'body',
                'class': 'cm-body'
            }),
            'name': forms.TextInput(attrs={
                'placeholder': 'name',
                'class': 'cm-name'
            })
        }


class SearchForm(forms.Form):
    query = forms.CharField()


class CreatePostForm(forms.ModelForm):
    image1 = forms.ImageField()
    image2 = forms.ImageField()

    class Meta:
        model = Post
        fields = ['title', 'description', 'category', 'reading_time']


class UserRigesterForm(forms.ModelForm):
    password = forms.CharField(max_length=20, widget=forms.PasswordInput(), label='password')
    password2 = forms.CharField(max_length=20, widget=forms.PasswordInput(), label='repeat password')

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('passwords do not match !')
        return cd['password2']


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class AccountEditForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['date_of_birth', 'bio', 'job', 'photo']

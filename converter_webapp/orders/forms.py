from django import forms


class UploadExelForm(forms.Form):
    file = forms.FileField(label='Файл')

    def clean_file(self):
        file = self.cleaned_data['file']
        if not file.name.endswith('.xlsx'):
            raise forms.ValidationError(
                'Принимаются только файлы формата xlsx'
            )

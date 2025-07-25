from django import forms
from notice.models import Employee, User, Notice

class NoticeWriteForm(forms.ModelForm):
    # files = forms.FileField(widget=forms.ClearableFileInput(attrs={
    #     'multiple': True
    #     }))
    def __init__(self, *args, **kwargs):
        super(NoticeWriteForm, self).__init__(*args, **kwargs)
        self.fields['not_title'].label = '제목'
        self.fields['not_title'].widget.attrs.update({
            'placeholder': '제목을 입력해주세요.',
            'class': 'form-control',
            'id': 'form_title',
            'autofocus': True,
        })

    class Meta:
        model = Notice
        fields = ['not_title', 'not_content']
        # widgets = {
        #     'upload_files': CustomFileWidget
        # }
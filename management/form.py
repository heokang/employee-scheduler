from django import forms
from management.models import Employee,Schedule_exchange
from django.contrib.auth.forms import UserChangeForm

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = '__all__'
class CustomCsUserChangeForm(UserChangeForm):
    password = None
    emp_name = forms.CharField(label='이름', widget=forms.TextInput(
        attrs={'class': 'form-control', 'maxlength': '10', }),
    )
    emp_address = forms.CharField(label='주소', widget=forms.TextInput(
        attrs={'class': 'form-control', 'maxlength':'45',}),
    )
    emp_phone = forms.CharField(label='전화번호', widget=forms.TextInput(
        attrs={'class': 'form-control', 'maxlength': '13', 'oninput': "maxLengthCheck(this)", }),
    )
    emp_account = forms.CharField(label='계좌번호', widget=forms.TextInput(
        attrs={'class': 'form-control', 'maxlength': '45', 'oninput': "maxLengthCheck(this)", }),
    )

    class Meta:
        model = Employee()
        fields = ['emp_name', 'emp_address', 'emp_phone', 'emp_account']


class ExchangeForm(forms.ModelForm):
    employee1 = forms.ModelChoiceField(queryset=Employee.objects.none(), disabled=True)
    start2 = forms.DateTimeField(required=False)
    end2 = forms.DateTimeField(required=False)

    def __init__(self, employee1, *args, **kwargs):
        super(ExchangeForm, self).__init__(*args, **kwargs)
        self.fields['employee1'].queryset = Employee.objects.filter(emp_id=employee1.emp_id)
        self.fields['employee1'].initial = employee1

        if employee1:
            employees = Employee.objects.exclude(emp_id=employee1.emp_id)

        else:
            employees = Employee.objects.all()



        self.fields['employee2'].queryset = employees

    class Meta:
        model = Schedule_exchange
        fields = ['employee1', 'employee2', 'start1', 'start2', 'end1', 'end2']

class
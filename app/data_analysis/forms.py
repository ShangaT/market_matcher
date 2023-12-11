from django import forms

class CategoryChoice(forms.Form):
    selected_button = forms.ChoiceField(choices=[])

    def update_choices(self, new_choices):
        self.fields['Введите данные'].choices = new_choices

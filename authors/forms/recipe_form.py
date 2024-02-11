from django import forms
from recipes.models import Recipe
from collections import defaultdict
from django.core.exceptions import ValidationError
from utils.strings import is_positive_number


class AuthorRecipeForm(forms.ModelForm):
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self._my_errors = defaultdict(list)
    class Meta:
        model = Recipe
        fields = 'title', 'description', 'preparation_time', 'preparation_time_unit', 'servings', 'servings_unit', \
            'preparation_steps', 'cover',
        widgets = {
            'preparation_steps': forms.Textarea(attrs={'class': 'span-2'}),
             'cover': forms.FileInput(attrs={'class': 'span-2'}),
            'description': forms.TextInput(),
            'servings_unit':forms.Select(choices=(
                ('Porções','Porções'),('Pedaços','Pedaços'),('Pessoas','Pessoas')
            )),
            'preparation_time_unit': forms.Select(choices=(
                ('Minutos', 'Minutos'), ('Horas', 'Horas'),
            )),

        }

    def clean(self):
        super_clean = super().clean()
        cd = self.cleaned_data

        title = cd.get('title')
        description = cd.get('description')

        if title == description:
            self._my_errors['title'].append('Cannot be equal to description')
            self._my_errors['description'].append('Cannot be equal to title')

        if self._my_errors:
            raise ValidationError(self._my_errors)

        return super_clean

    def clean_title(self):
        title = self.cleaned_data.get('title')

        if len(title) < 5:
            self._my_errors['title'].append('Must have at least 5 chars.')

        return title

    def clean_preparation_time(self):
        field_name = 'preparation_time'
        field_value = self.cleaned_data.get(field_name)

        if not is_positive_number(field_value):
            self._my_errors[field_name].append('Must be a positive number')

        return field_value

    def clean_servings(self):
        field_name = 'servings'
        field_value = self.cleaned_data.get(field_name)

        if not is_positive_number(field_value):
            self._my_errors[field_name].append('Must be a positive number')

        return field_value
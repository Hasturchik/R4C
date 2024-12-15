import re

from django.core.exceptions import ValidationError
from django.core.validators import MaxLengthValidator
from django.forms import ModelForm
from .models import Robot



class RobotForm(ModelForm):
    class Meta:
        model = Robot
        fields = ['model', 'version', 'created']

    def clean(self):
        cleaned_data = super().clean()

        max_length_validator = MaxLengthValidator(2)
        try:
            max_length_validator(cleaned_data.get('model', ''))
            max_length_validator(cleaned_data.get('version', ''))
        except ValidationError as e:
            raise ValidationError({"model": e.message, "version": e.message})

        model = cleaned_data.get('model')
        if model and not re.match(r'^[A-Z]\d$', model):
            raise ValidationError({"version": "Incorrect model."})
        # if model and not Robot.objects.filter(model=model).exists():
        #     raise ValidationError({"Incorrect model."})

        version = cleaned_data.get('version')
        if version and not re.match(r'^[A-Z]\d$', version):
            raise ValidationError({"version": "Incorrect version."})

        created_date = cleaned_data.get('created')
        if created_date is None:
            raise ValidationError({"created": "Invalid date format for 'created'."})

        return cleaned_data

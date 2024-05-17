from rest_framework import serializers

from habit.models import Habit
from habit.validators import (Hobit_Plese_Useful_Validator,
                              Time_Validator,
                              Related_Sign_Validator,
                              Good_Sign_Validator, Priority_Validator)


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = '__all__'

        validators = [
            Hobit_Plese_Useful_Validator(
                pleasant_habit='pleasant_habit',
                award='award'
            ),
            Time_Validator(time_to_complete='time_to_complete'),
            Related_Sign_Validator(pleasant_habit='pleasant_habit'),
            Good_Sign_Validator(
                pleasant_habit='pleasant_habit',
                sign_pleasand_habit='sign_pleasand_habit',
                award='award'),
            Priority_Validator(period='period'),
        ]

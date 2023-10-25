from rest_framework.serializers import ModelSerializer, ValidationError

from habits.models import Habit


PERIODICITY_VALID_VALUES = ('daily', 'every_other_day', 'every_third_day',
                            'every_fourth_day', 'every_fifth_day', 'every_sixth_day', 'weekly')


class HabitCreateUpdateSerializer(ModelSerializer):
    """ Serializer for creating and updating Habit objects. """

    class Meta:
        model = Habit
        fields = ('action', 'location', 'time', 'is_pleasant', 'periodicity', 'related_habit', 'reward',
                  'execution_time', 'is_public', 'start_date')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.context['request'].method in ['PUT', 'PATCH']:
            self.fields['location'].required = False
            self.fields['time'].required = False
            self.fields['periodicity'].required = False
            self.fields['execution_time'].required = False
            self.fields['start_date'].required = False


    def validate_periodicity(self, value):
        """
                Validates the 'periodicity' field in the provided data.
        """
        if value not in PERIODICITY_VALID_VALUES:
            raise ValidationError(f"Invalid value for 'periodicity'. "
                                  f"Valid values are: {', '.join(PERIODICITY_VALID_VALUES)}")

    def validate(self, attrs):
        """ Validate the serializer data. """

        reward = attrs.get('reward')
        related_habit = attrs.get('related_habit')
        is_pleasant = attrs.get('is_pleasant')

        if reward and related_habit:
            raise ValidationError('Error: Choose either a related habit or specify a reward, '
                                  'but not both simultaneously.')

        if is_pleasant and (reward or related_habit):
            raise ValidationError('Error: A pleasant habit cannot have a reward or a related habit.')

        return attrs

    def validate_related_habit(self, value):
        """ Validate the related habit. """

        if value is None:
            raise ValidationError("Error: Related habit is None.")
        elif value.owner != self.context['request'].user:
            raise ValidationError('Error: Only your own habits can be related to this habit.')
        elif not value.is_pleasant:
            raise ValidationError('Error: Only pleasant habits can be related to this habit.')
        return value

    def create(self, validated_data):
        """ Create a new Habit object. """

        owner = self.context['request'].user
        validated_data['owner'] = owner
        habit = Habit.objects.create(**validated_data)
        return habit


class HabitListSerializer(ModelSerializer):
    """ Serializer for listing Habit objects. """

    class Meta:
        model = Habit
        fields = ('action', 'periodicity')


class HabitDetailSerializer(ModelSerializer):
    """ Serializer for displaying detailed information about a Habit."""

    class Meta:
        model = Habit
        fields = '__all__'

    def to_representation(self, instance):

        """
        This method customizes the representation of the Habit object by excluding specific fields based on
        whether the requesting user is the owner.
        """

        user = self.context.get('request').user
        data = super().to_representation(instance)
        excluded_fields = ()

        if instance.owner == user:
            excluded_fields = ('id', 'owner', 'days', 'last_notification')

        if instance.owner != user:
            excluded_fields = ('id', 'owner', 'days', 'last_notification', 'reward', 'related_habit', 'start_date')

        for field in excluded_fields:
            data.pop(field, None)

        return data



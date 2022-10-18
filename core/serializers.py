from core.models import Profile
from rest_framework import serializers


class ProfileModelSerializer(serializers.ModelSerializer):
    """
        Profile Serializer is for serializing profile details.
        lookup_field - The field on the target that should be used for the lookup.
                        Should correspond to a URL keyword argument on the referenced view.
                        Default is 'pk'
    """
    email = serializers.CharField(required=False)
    class Meta:
        model = Profile
        fields = '__all__'


class GetProfileModelSerializer(serializers.ModelSerializer):
    """
        Profile Serializer is for serializing profile details.
        lookup_field - The field on the target that should be used for the lookup.
                        Should correspond to a URL keyword argument on the referenced view.
                        Default is 'pk'
    """
    url = serializers.HyperlinkedIdentityField(read_only=True, view_name='get-profile-detail')
    user_name = serializers.CharField(source='user.username', read_only=True)
    added_by_first_name = serializers.CharField(source='added_by.first_name', read_only=True)
    added_by_last_name = serializers.CharField(source='added_by.last_name', read_only=True)
    class Meta:
        model = Profile
        fields = '__all__'

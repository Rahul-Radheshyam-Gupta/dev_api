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

    class Meta:
        model = Profile
        fields = '__all__'

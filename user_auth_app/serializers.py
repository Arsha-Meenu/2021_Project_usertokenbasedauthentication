from django.contrib.auth import get_user_model
from rest_framework import serializers

# from user_auth_app.models import Library

User = get_user_model()

# For User Registration
class RegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(style={'input_type':'password'},write_only=True) #create a new field(confirm_password) in User model.
    class Meta:
        model = User#model for serializer
        fields = ['username','email','password','confirm_password'] # a tuple of field names to be included in the serialization 
    

    def save(self):
        # user given email and username is validated and save it into the corresponding fields
        regData = User(
            email = self.validated_data['email'],
            username = self.validated_data['username']
            )    
        # manually check the password confirmation
        password = self.validated_data['password']
        password2 = self.validated_data['confirm_password']
        if password != password2:
            raise serializers.ValidationError({'password':'password doesnot match'})
        regData.set_password(password2)
        regData.save()
        return regData


class UserLoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length = 65,min_length = 8,write_only = True)
    username = serializers.CharField(max_length=255,min_length=2)

    class Meta:
        model = User
        fields = ['username','password']
        # fields = '__all__'


class UserViewSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username","email","password"]
        # fields = '__all__'

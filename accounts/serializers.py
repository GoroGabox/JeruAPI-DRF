from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
from accounts.models import Rol

User = get_user_model()


class RolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rol
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    rol = RolSerializer(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'nombre', 'apellido', 'email', 'rol')


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'nombre',
            'apellido',
            'email',
            'rol',
            'password',
            'password2',
        ]
    extra_kwargs = {
        'password': {'write_only': True},
        'password2': {'write_only': True},
    }

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Las contraseñas no coinciden")
        return data

    def create(self, validated_data):
        password = validated_data.pop('password2', None)
        user = super().create(validated_data)
        user.set_password(password)
        user.save()
        return user


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['nombre'] = user.nombre
        token['apellido'] = user.apellido
        token['email'] = user.email
        token['rol'] = user.rol.id

        return token

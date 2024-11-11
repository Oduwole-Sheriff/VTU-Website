from rest_framework import serializers
from authentication.models import Profile

from django.contrib.auth.models import User


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=8)

    def validate(self, data):
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError('Username is taken')
        
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError('Email is taken')

        return data
        print(data)

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    

class LoginSerializer(serializers.Serializer):
        username = serializers.CharField()
        password = serializers.CharField()



# class RegisterSerializer(serializers.Serializer):
#     username = serializers.CharField()
#     email = serializers.EmailField()
#     password = serializers.CharField()

#     def validate(self, data):
#         if data['username']:
#             if User.objects.filter(username = data['username']).exists():
#                 raise serializers.ValidationError('username is taken')

#         if data['email']:
#             if User.objects.filter(username = data['email']).exists():
#                 raise serializers.ValidationError('email is taken')

#         return data
#     def create(self, validated_data):
#         user = User.objects.create(username = validated_data['username'], email = validated_data['email'])
#         user.set_password(validated_data['password'])
#         user.save()
#         return validated_data
#         print(validated_data)

# class LoginSerializer(serializers.Serializer):
#         username = serializers.CharField()
#         password = serializers.CharField()

# class PostSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Post
#         fields = "__all__"

#     def validate_name(self, value):
#         if self.instance: 
#             existing_post = Post.objects.exclude(pk=self.instance.pk).filter(name=value)
#             if existing_post.exists():
#                 raise serializers.ValidationError("A post with this name already exists.")
#         else:
#             if Post.objects.filter(name=value).exists():
#                 raise serializers.ValidationError("A post with this name already exists.")
#         return value

    # def create(self, validated_data):
    #     return Post.objects.create(**validated_data)

    # def update(self, instance, validated_data):
    #     instance.name = validated_data.get('name', instance.name)
    #     instance.content = validated_data.get('content', instance.content)
    #     instance.save()
    #     return instance

# class PersonSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Person
#         fields = "__all__"

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['city'].queryset = City.objects.none()

    #     if 'country' in self.data:
    #         try:
    #             country_id = int(self.data.get('country'))
    #             self.fields['city'].queryset = City.objects.filter(country_id=country_id).order_by('name')
    #         except (ValueError, TypeError):
    #             pass  # invalid input from the client; ignore and fallback to empty City queryset
    #     elif self.instance.pk:
    #         self.fields['city'].queryset = self.instance.country.city_set.order_by('name')

# class LanguageSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Entry
#         fields = '__all__'

# class ProfileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Profile
#         fields = '__all__'
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import AdminProfile, DoctorProfile, StaffProfile, Room, Task, Assign


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate_password(self, value):
        if User.objects.filter(password=value).exists():
            raise serializers.ValidationError("This password is already in use.")
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        return user

class AdminProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = AdminProfile
        fields = ['user', 'image']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_serializer = UserSerializer(data=user_data)
        if user_serializer.is_valid(raise_exception=True):
            user = user_serializer.save()
            admin_profile = AdminProfile.objects.create(user=user, **validated_data)
            return admin_profile
        
 
class DoctorProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = DoctorProfile
        fields = ['user', 'image']



    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_serializer = UserSerializer(data=user_data)
        if user_serializer.is_valid(raise_exception=True):
            user = user_serializer.save()
            doctor_profile = DoctorProfile.objects.create(user=user, **validated_data)
            return doctor_profile
        

class StaffProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = StaffProfile
        fields = ['user', 'image']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_serializer = UserSerializer(data=user_data)
        if user_serializer.is_valid(raise_exception=True):
            user = user_serializer.save()
            staff_profile = StaffProfile.objects.create(user=user, **validated_data)
            return staff_profile


class RoomSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')
    room = serializers.ReadOnlyField(source='room.name')

    class Meta:
        model = Room
        fields = ['room' , 'image', 'name','username'] 




class AssignSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')
    task = serializers.ReadOnlyField(source='task.name')

    class Meta:
        model = Assign
        fields = ['username', 'done_at', 'supervisor_approved', 'comment', 'task']


class TaskSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source='created_by.username')
    room = serializers.ReadOnlyField(source='room.name')
    assigns = AssignSerializer(many=True, read_only=True, source='assign_set')

    class Meta:
        model = Task
        fields = ('id', 'name', 'arabic_name', 'description', 'image', 'created_by', 'room', 'created', 'assigns')

    

class StaffLoginSerializer(serializers.Serializer):
    username = serializers.CharField()

    def validate(self, data):
        username = data.get('username')

        if username:
            try:
                user = User.objects.get(username=username)
                if not user.is_active:
                    raise serializers.ValidationError("User account is disabled.")
            except User.DoesNotExist:
                raise serializers.ValidationError("User with this username does not exist.")
        else:
            raise serializers.ValidationError("Must include 'username'.")

        data['user'] = user
        return data
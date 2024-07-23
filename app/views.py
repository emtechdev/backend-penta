from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from .serializers import AdminProfileSerializer, DoctorProfileSerializer, StaffProfileSerializer, RoomSerializer, TaskSerializer, AssignSerializer, StaffLoginSerializer
from django.contrib.auth import authenticate
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from .models import StaffProfile
from .models import Room , Task, Assign
from django.db import IntegrityError
from django.contrib.auth import login


class RegisterAdminView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = AdminProfileSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response({'message': 'Admin registered successfully'}, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegisterDoctorView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = DoctorProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Doctor registered successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegisterStaffView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = StaffProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Staff registered successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
    


class StaffProfileViewSet(viewsets.ModelViewSet):
    queryset = StaffProfile.objects.all()
    serializer_class = StaffProfileSerializer



# class StaffLoginView(APIView):
#     def post(self, request, *args, **kwargs):
#         photo_url = request.data.get('photo_url')
#         password = request.data.get('password')

#         try:
#             staff_profile = StaffProfile.objects.get(image=photo_url)
#             user = staff_profile.user

#             user = authenticate(username=user.username, password=password)
#             if user is not None:
#                 return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
#             else:
#                 return Response({'error': 'Invalid password'}, status=status.HTTP_400_BAD_REQUEST)
#         except StaffProfile.DoesNotExist:
#             return Response({'error': 'Invalid photo selection'}, status=status.HTTP_400_BAD_REQUEST)
        


class StaffLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = StaffLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            login(request, user)
            return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'], url_name='add_task', url_path='add_task')
    def add_task(self, request, pk):
        room = self.get_object()
        name = request.data.get('name')
        arabic_name = request.data.get('arabic_name')
        description = request.data.get('description')
        image = request.data.get('image')
        
        if not name:
            return Response({'error': 'Name is required'}, status=status.HTTP_400_BAD_REQUEST)

        user = request.user

        try:
            task = Task.objects.create(
                room=room,
                name=name,
                arabic_name=arabic_name,
                description=description,
                image=image,
                created_by=user
            )
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        serializer = TaskSerializer(task)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

    @action(detail=True, methods=['get'], url_name='get_tasks', url_path='get_tasks')
    def get_tasks(self, request, pk):
        try:
            room = self.get_object()
            tasks = Task.objects.filter(
                room=room
            ).distinct()
            serializer = TaskSerializer(tasks, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Task.DoesNotExist:
            return Response({'error': 'No tasks found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



    @action(detail=True, methods=['get'], url_name='get_unrevised_tasks', url_path='get_unrevised_tasks')
    def get_unrevised_tasks(self, request, pk):
        try:
            room = self.get_object()
            tasks = Task.objects.filter(
                assign__supervisor_approved__isnull=True,
                room=room
            ).distinct()
            serializer = TaskSerializer(tasks, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Task.DoesNotExist:
            return Response({'error': 'No tasks found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


   
    @action(detail=True, methods=['get'], url_name='get_not_approved_tasks', url_path='get_not_approved_tasks')
    def get_not_approved_tasks(self, request, pk):
        try:
            room = self.get_object()
            tasks = Task.objects.filter(
                assign__supervisor_approved=False,
                room=room
            ).distinct()
            serializer = TaskSerializer(tasks, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Task.DoesNotExist:
            return Response({'error': 'No tasks found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['get'], url_name='get_approved_tasks', url_path='get_approved_tasks')
    def get_approved_tasks(self, request, pk):
        try:
            room = self.get_object()
            tasks = Task.objects.filter(
                assign__supervisor_approved=True,
                room=room
            ).distinct()
            serializer = TaskSerializer(tasks, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Task.DoesNotExist:
            return Response({'error': 'No tasks found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer



    @action(detail=True, methods=['post'], url_name='assign_task', url_path='assign_task')
    def assign_task(self, request, pk):
        task = self.get_object()
        user = request.user
        serializer = AssignSerializer(data=request.data)
        if serializer.is_valid():
            try:
                assign = Assign.objects.create(task=task, user=user, **serializer.validated_data)
                response_serializer = AssignSerializer(assign)
                return Response(response_serializer.data, status=status.HTTP_201_CREATED)
            except IntegrityError:
                return Response({'error': 'This task has already been assigned to this user.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class AssignViewSet(viewsets.ModelViewSet):
    queryset = Assign.objects.all()
    serializer_class = AssignSerializer



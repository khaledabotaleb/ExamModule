from django.shortcuts import render, redirect
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from User.serializers import RegisterationSerializer, CreateHeadMaster, CreateTeacher, CreateStudent, CreateParent
from .models import User, HeadMaster
from rest_framework.authtoken.models import Token


#function that check if user is exict in database
def get_or_none(classmodel, **kwargs):
    try:
        return classmodel.objects.get(**kwargs)
    except classmodel.DoesNotExist:
        return None


#head master registeration view
@api_view(['POST'],)
def registration_headmaster_view(request):

    if request.method == 'POST':
        serializer = RegisterationSerializer(data=request.data)
        serializer2 = CreateHeadMaster(data=request.data)
        data = {}
        # status = 0
        if serializer.is_valid():
            user = serializer.save()
            data['respone'] = 'Successful registrated a new user'
            data['email'] = user.email
            data['username'] = user.username
            data['role'] = user.role
            data['address'] = user.address
            data['phone'] = user.phone_number
            data['birth_date'] = user.birth_date
            token = Token.objects.get(user=user).key
            data['token'] = token
            if serializer2.is_valid():
                username = user.username
                author = get_or_none(User, username=username)
                if username:
                    headmaster = serializer2.save(user=author)
                    data['uni_code'] = headmaster.uni_code
                    data['educationalType'] = headmaster.educational_type
                    data['level'] = headmaster.educational_level
                    # status = 201
                else:
                    data['responseUser'] = 'user not found'
                    # status = 404
            else:
                data['responseHeadMaster'] = 'error in validation'
                # status = 400
        else:
            if data:
                data += serializer.errors
            else:
                data = serializer.errors
        return Response(data)


#teacher registeration view
@api_view(['POST'],)
def registration_teacher_view(request):
    if request.method == 'POST':
        serializer = RegisterationSerializer(data=request.data)
        serializer2 = CreateTeacher(data=request.data)
        data = {}
        # status = 0
        if serializer.is_valid():
            user = serializer.save()
            data['respone'] = 'Successful registrated a new user'
            data['email'] = user.email
            data['username'] = user.username
            data['role'] = user.role
            data['address'] = user.address
            data['phone'] = user.phone_number
            data['birth_date'] = user.birth_date
            token = Token.objects.get(user=user).key
            data['token'] = token
            if serializer2.is_valid():
                username = user.username
                author = get_or_none(User, username=username)
                if author:
                    teacher = serializer2.save(user=author)
                    data['uni_code'] = teacher.uni_code
                    data['grade'] = teacher.grade
                    data['level'] = teacher.level
                    # status = 201
                else:
                    data['responseUser'] = 'user not found'
                    # status = 404
            else:
                data = serializer2.errors
        else:
            if data:
                data += serializer.errors
            else:
                data = serializer.errors
        return Response(data)


#student registeration view
@api_view(['POST'],)
def registration_student_view(request):
    if request.method == 'POST':
        serializer = RegisterationSerializer(data=request.data)
        serializer2 = CreateStudent(data=request.data)
        data = {}
        # status = 0
        if serializer.is_valid():
            user = serializer.save()
            data['respone'] = 'Successful registrated a new user'
            data['email'] = user.email
            data['username'] = user.username
            data['role'] = user.role
            data['address'] = user.address
            data['phone'] = user.phone_number
            data['birth_date'] = user.birth_date
            token = Token.objects.get(user=user).key
            data['token'] = token
            if serializer2.is_valid():
                username = user.username
                author = get_or_none(User, username=username)
                if username:
                    student = serializer2.save(user=author)
                    data['uni_code'] = student.uni_code
                    data['grade'] = student.grade
                    data['level'] = student.level
                    # status = 201
                else:
                    data['responseUser'] = 'user not found'
                    # status = 404
            else:
                data['responseStudent'] = 'error in validation'
                # status = 400
        else:
            if data:
                data += serializer.errors
            else:
                data = serializer.errors
        return Response(data)


#parent registeration view
@api_view(['POST'],)
def registration_parent_view(request):
    if request.method == 'POST':
        serializer = RegisterationSerializer(data=request.data)
        serializer2 = CreateParent(data=request.data)
        data = {}
        # status = 0
        if serializer.is_valid():
            user = serializer.save()
            data['respone'] = 'Successful registrated a new user'
            data['email'] = user.email
            data['username'] = user.username
            data['role'] = user.role
            data['address'] = user.address
            data['phone'] = user.phone_number
            data['birth_date'] = user.birth_date
            token = Token.objects.get(user=user).key
            data['token'] = token
            if serializer2.is_valid():
                username = user.username
                author = get_or_none(User, username=username)
                if username:
                    # check that unicode is exist in database
                    masters = HeadMaster.objects.all()
                    listMaster = []
                    for master in masters:
                        listMaster.append(master.uni_code)
                    
                    if serializer2.uni_code not in listMaster:
                        data['uni_code'] = 'unicode dose not exist'
                        confirmUser = serializer2.cofirm_user
                        userWhichSaved = User.objects.get(username=confirmUser)
                        if userWhichSaved:
                            userWhichSaved.delete()
                        else:
                            data['user'] = 'user dose not exist'
                    else:
                        parent = serializer2.save(user=author)
                        data['uni_code'] = parent.uni_code
                    # status = 201
                else:
                    data['responseUser'] = 'user not found'
                    # status = 404
            else:
                data['responseStudent'] = 'error in validation'
                # status = 400
        else:
            if data:
                data += serializer.errors
            else:
                data = serializer.errors
        return Response(data)
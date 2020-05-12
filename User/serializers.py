from rest_framework import serializers
from rest_framework.response import Response
from User.models import User, HeadMaster, Teacher, Student, Parent


#serializer for register new user
class RegisterationSerializer(serializers.ModelSerializer):
    #make confirm password write only (can not copy or past on it)
    password2 = serializers.CharField(style={'input_type' : 'password'}, write_only=True)
    phone_number = serializers.CharField(max_length=20)
    role = serializers.CharField(max_length=50)
    address = serializers.CharField(max_length=255)
    birth_date = serializers.DateField()

    class Meta:
        model = User
        fields = ['email', 'username', 'phone_number', 'role', 'address', 'birth_date', 'password', 'password2']
        extra_kwargs = {
            #make password write only (can not copy or past on it)
            'password' : {'write_only': True}
        }

    # override finction save to check if confirm password equal password
    def save(self):
        user = User(
            email = self.validated_data['email'],
            username = self.validated_data['username'],
            phone_number = self.validated_data['phone_number'],
            role = self.validated_data['role'],
            address = self.validated_data['address'],
            birth_date = self.validated_data['birth_date']
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'password': 'password must match'})
        user.set_password(password)
        user.save()
        return user

#serializer for register new head master
class CreateHeadMaster(serializers.ModelSerializer):
    class Meta:
        model = HeadMaster
        fields = ['school_name', 'educational_type', 'educational_level', 'confirm_user']


#serializer for register new teacher
class CreateTeacher(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['uni_code', 'grade', 'level', 'confirm_user']

    #overide save function to check that school unicode is exist in database
    # def save(self, *args, **kwargs):

    #     masters = HeadMaster.objects.all()
    #     listMaster = []

    #     for master in masters:
    #         listMaster.append(master.uni_code)

    #     teacher = Teacher(
    #         grade = self.validated_data['grade'],
    #         level = self.validated_data['level']
    #     )
    #     uni_code = self.validated_data['uni_code']
    #     confirm_user = self.validated_data['confirm_user']

    #     if uni_code not in listMaster:
    #         user = User.objects.get(username=confirm_user)
    #         if user:
    #             user.delete()
    #             raise serializers.ValidationError({'uni_code': 'unicode dose not exist'})
    #         else:
    #             raise serializers.ValidationError({'user': 'user dose not exist'})
    #     else:
    #         teacher.set_uni_code(uni_code)
    #         teacher.save()
    #         return teacher


#serializer for register new student
class CreateStudent(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['uni_code', 'grade', 'level', 'confirm_user']

    #overide save function to check that school unicode is exist in database
    def save(self, *args, **kwargs):

        masters = HeadMaster.objects.all()
        listMaster = []

        for master in masters:
            listMaster.append(master.uni_code)

        student = Student(
            grade = self.validated_data['grade'],
            level = self.validated_data['level']
        )
        uni_code = self.validated_data['uni_code']
        confirm_user = self.validated_data['confirm_user']

        if uni_code not in listMaster:
            user = User.objects.get(username=confirm_user)
            if user:
                user.delete()
                raise serializers.ValidationError({'uni_code': 'unicode dose not exist'})
            raise serializers.ValidationError({'user': 'user dose not exist'})
        student.set_uni_code(uni_code)
        student.save()
        return student


#serializer for register new parent
class CreateParent(serializers.ModelSerializer):
    class Meta:
        model = Parent
        fields = ['uni_code',  'confirm_user']

        #stell need to check unicode is exist but it will be in views.py not here
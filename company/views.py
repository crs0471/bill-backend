from django.shortcuts import render
from django.contrib.auth.models import User
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.hashers import check_password, make_password
from rest_framework_simplejwt.tokens import RefreshToken
from django.db.models import Q




from helper import functions
# Create your views here.
class Login(APIView):
    
    def post(self, request):
        try:
            email = request.data['email']
            password = request.data['password']
            user = User.objects.filter(Q(email=email) | Q(username=email)).first()
            if user:
                if not check_password(password, user.password):
                    return functions.formated_response(message="Invalid Credencials!", code=400)
                refresh = RefreshToken.for_user(user)
                data = {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
                return functions.formated_response("Login Successfull!", dict_=data)
            
            else:
                return functions.formated_response(message="Invalid Credencials!", code=400, dev_message="User name already exists.")
        except Exception as err:
            return functions.formated_response(message="Something went wrong!", code=500, dev_message=str(err))



class Register(APIView):
    def post(self, request):
        try:
            if not (username := request.data.get('username')):
                return functions.formated_response(message="User Name is required", code=400)
            if not (email := request.data.get('email')):
                return functions.formated_response(message="Email is required", code=400)
            if not (password := request.data.get('password')):
                return functions.formated_response(message="Password is required", code=400)
            if not (cpassword := request.data.get('confirm_password')):
                return functions.formated_response(message="Confirm Password is required", code=400)
            if password != cpassword:
                return functions.formated_response(message="Password and Confirm Password not Match", code=400)
            
            if User.objects.filter(Q(username=username) | Q(email=email)).exists():
                return functions.formated_response(message="User Already Exists", code=400, dev_message="User name already exists.")

            user = User.objects.create(username=username, email=email, password=make_password(password))            
            return functions.formated_response(message="Register Successful", code=200)

        except Exception as err:
            return functions.formated_response(message="Something went wrong!", code=500, dev_message=str(err))
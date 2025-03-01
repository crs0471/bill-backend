from django.shortcuts import render
from django.contrib.auth.models import User
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.hashers import check_password, make_password
from rest_framework_simplejwt.tokens import RefreshToken



from helper import functions
# Create your views here.
class Login(APIView):
    
    def post(self, request):
        email = request.data['email']
        password = request.data['password']
        user = User.objects.filter(email=email)
        if user:
            user = User.objects.get(email=email)
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


    def get(self, request):
        user = request.user
        print("USER : ", user)
        return functions.formated_response("Successfull!")
        
        
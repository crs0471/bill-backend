from django.shortcuts import render
from django.contrib.auth.models import User
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.hashers import check_password, make_password
from rest_framework_simplejwt.tokens import RefreshToken
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from company.models import Company



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
        

class Companyview(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):

        try:
            user = request.user
            if not (name := request.data.get('name')):
                return functions.formated_response(message="Name is required", code=400)
            if not (email := request.data.get('email')):
                return functions.formated_response(message="Email is required", code=400)
            if not (phone := request.data.get('phone')):
                return functions.formated_response(message="phone is required", code=400)
            if not (gst_number := request.data.get('gst_number')):
                return functions.formated_response(message="gst number is required", code=400)
            if not (address := request.data.get('address')):
                return functions.formated_response(message="address is required", code=400)
    
            user = Company.objects.create(user=user , name=name, email=email, phone=phone, gst_number=gst_number, address=address)            
            return functions.formated_response(message="Company Created Successful", code=200)
        

        except Exception as err:
            return functions.formated_response(message="Something went wrong!", code=500, dev_message=str(err))
        

    def get(self, request):
        try:
            user = request.user
            print("dfsf : ", user)
            user_company = Company.objects.filter(user=user)
            companys = []
            for company in user_company:
                com = {}
                print("ERR : ", company.user)
                com['name'] = company.name
                com['email'] = company.email
                com['phone'] = company.phone
                com['gst_number'] = company.gst_number
                com['address'] = company.address
                companys.append(com)

            return functions.formated_response(message="Company List", code=200, dict_={"companys":companys})
 

        except Exception as err:
            return functions.formated_response(message="Something went wrong!", code=500, dev_message=str(err))

class Updatecompanyview(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, id):
        try:
            user = request.user
            company = Company.objects.filter(Q(user=user) & Q(id=id)).values()
            company = company[0]
            com = {
                'id':company['id'],
                'name':company['name'],
                'email':company['email'],
                'phone':company['phone'],
                'gst_number': company['gst_number'],
                'address' : company['address'],
            }

            return functions.formated_response(message="Company List", code=200, dict_={"company":com})

        except Exception as err:
            return functions.formated_response(message="Something went wrong!", code=500, dev_message=str(err))

    def delete(self, request, id):
        try:    
            user = request.user
            Company.objects.filter(Q(user=user) & Q(id=id)).delete()
            return functions.formated_response(message="Deleted Successfull", code=200)
        
        except Exception as err:
            return functions.formated_response(message="Something went wrong!", code=500, dev_message=str(err))

    def patch(self, request, id):
        try:
            user = request.user
            company = Company.objects.filter(Q(user=user) & Q(id=id))[0]

            if not company:
                return functions.formated_response(message="Company not exists", code=200)

            if name := request.data.get('name'):
                company.name = name
            if email := request.data.get('email'):
                company.email = email
            if phone := request.data.get('phone'):
                company.phone = phone
            if gst_number := request.data.get('gst_number'):
                company.gst_number = gst_number
            if address := request.data.get('address'):
                company.address = address
            
            company.save()
            return functions.formated_response(message="Updated Successfull", code=200)

        except Exception as err:
            return functions.formated_response(message="Something went wrong!", code=500, dev_message=str(err))

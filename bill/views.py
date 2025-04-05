from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from helper import functions
from company.models import Company, Client
from bill.models import Bill, Bill_product, Bill_product_master
from bill.serializers import BillSerializer


# Create your views here.




class Master_productview(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            master_bills_qs = Bill_product_master.objects.filter(company_id__user_id=request.user)

            # if comapny if filter
            if (company_id := request.GET.get('company_id')):
                master_bills_qs = master_bills_qs.filter(company_id=company_id)

            # if search
            if search := request.GET.get('search'):
                master_bills_qs = master_bills_qs.filter(name__icontains=search)

            return functions.formated_response(message="Bill Master Product of Company", code=200, dict_=master_bills_qs.values())

            
        except Exception as err:
            return functions.formated_response(message="Something went wrong!", code=500, dev_message=str(err))
        






class Billview(APIView):
    permission_classes = [IsAuthenticated]

    # listing, GET method , filter comp_id, client_id,  search(bill no)
    def get(self, request):
        try:

            if not Company.objects.filter(user=request.user).exists():
                return functions.formated_response(message="Company not exists for this user", code=400)
            
            bill = Bill.objects.filter(company_id__user = request.user)
            if company_id := request.query_params.get('company_id'):
                bill = bill.filter(company_id = company_id)
            if client_id := request.query_params.get('client_id'):
                bill = bill.filter(client_id = client_id)
            if bill_no := request.query_params.get('bill_no'):
                bill = bill.filter(bill_no = bill_no)

            serializer = BillSerializer(bill, many=True)
            return functions.formated_response(message="Bill Successfully Retrieved", code=200, dict_=serializer.data)
            


        except Exception as err:
            return functions.formated_response(message="Something went wrong!", code=500, dev_message=str(err))





    def post(self, request):
        try:
            if not (company_id := request.data.get('company_id')):
                return functions.formated_response(message="Company ID is required", code=400)
            if not (client_id := request.data.get('client_id')):
                return functions.formated_response(message="Client ID is required", code=400)
            if not (note := request.data.get('note')):
                return functions.formated_response(message="Note is required", code=400)
            if not (description := request.data.get('description')):
                return functions.formated_response(message="Description is required", code=400)
            if not (due_date := request.data.get('due_date')):
                return functions.formated_response(message="Due Date is required", code=400)
            if not (cgst := request.data.get('cgst')):
                return functions.formated_response(message="cgst is required", code=400)
            if not (igst := request.data.get('igst')):
                return functions.formated_response(message="igst is required", code=400)
            if not (sgst := request.data.get('sgst')):
                return functions.formated_response(message="sgst is required", code=400)
            if not (discount := request.data.get('discount')):
                return functions.formated_response(message="Discount is required", code=400)
            if not (shipping := request.data.get('shipping')):
                return functions.formated_response(message="Shipping is required", code=400)
            if not (bill_no := request.data.get('bill_no')):
                return functions.formated_response(message="Bill No is required", code=400)
            if not (bill_products := request.data.get('bill_products')):
                return functions.formated_response(message="bill_product is required", code=400)
            
            if not Company.objects.filter(user=request.user, id=company_id).exists():
                return functions.formated_response(message="Company not exists for this user", code=400)
            
            for bill_pro in request.data.get('bill_products'):
                if not (price := bill_pro['price']):
                    return functions.formated_response(message="Price is required", code=400)
                if not (quantity := bill_pro['quantity']):
                    return functions.formated_response(message="Quantity is required", code=400)
                if not (code := bill_pro['code']):
                    return functions.formated_response(message="Code is required", code=400)
                if not (name := bill_pro['name']):
                    return functions.formated_response(message="Name is required", code=400)
                if not (new := bill_pro['new']):
                    return functions.formated_response(message="New is required", code=400)
            
            if not Client.objects.filter(id=client_id, company_id=company_id).first():
                return functions.formated_response(message="Client not exists for this Company", code=400)
            

            bill = Bill(company_id=company_id, client_id=client_id, note=note, description=description, due_date=due_date,cgst=cgst, igst=igst, sgst=sgst,discount=discount, shipping=shipping, bill_no=bill_no)
            bill.save()

            for bill_pro in request.data.get('bill_products'):
                bill_product = Bill_product(bill=bill, price=bill_pro['price'], quantity=bill_pro['quantity'], code=bill_pro['code'], name=bill_pro['name'])
                bill_product.save()
                if str(bill_pro['new']) == "1":
                    bill_product_master = Bill_product_master(company_id=company_id, name=bill_pro['name'], price=bill_pro['price'], code=bill_pro['code'])
                    bill_product_master.save()

            return functions.formated_response(message="Bill Successfully Saved", code=200)

        except Exception as err:
            return functions.formated_response(message="Something went wrong!", code=500, dev_message=str(err))




   
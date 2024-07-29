from django.shortcuts import render

# Create your viewss.py here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializer import *
import pandas as pd
from io import BytesIO
from django.http import HttpResponse
import pandas as pd
from io import StringIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


class UserList(APIView):
 def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

 def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ExportUsersToExcel(APIView):
    def get(self, request):
        # Retrieve all users from the database
        users = User.objects.all()

        # Create a pandas DataFrame from the users data
        data = {
            'Product Name': [user.item_name for user in users],
            'Home Depot': [user.description for user in users],
            'Targeted Price': [user.weight for user in users],
            'Cost Price': [user.price for user in users],
            'SKU': [user.sku for user in users],
            'Internal Id': [user.unit_cost for user in users],
            'Category': [user.category for user in users],
            'Brand': [user.variation_name for user in users],
            'Supplier': [user.name_area for user in users],
        }
        df = pd.DataFrame(data)

        # Convert DataFrame to Excel file in memory (BytesIO)
        excel_file = BytesIO()
        df.to_excel(excel_file, index=False)
        excel_file.seek(0)  # Move the cursor to the beginning of the file

        # Prepare response
        response = HttpResponse(
            excel_file,
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename="users.xlsx"'

        return response


class ExportUsersToCSV(APIView):
    def get(self, request):
        # Retrieve all users from the database
        users = User.objects.all()

        # Create a pandas DataFrame from the users data
        data = {
            'User ID': [user.user_id for user in users],
            'Item Name': [user.item_name for user in users],
            'Price': [user.price for user in users],
            'SKU': [user.sku for user in users],
            'Category': [user.category for user in users],
            'Weight': [user.weight for user in users],
            'Unit Cost': [user.unit_cost for user in users],
            'Description': [user.description for user in users],
            'Variation Name': [user.variation_name for user in users],
            'Name Area': [user.name_area for user in users],
        }
        df = pd.DataFrame(data)

        # Convert DataFrame to CSV file in memory (StringIO)
        csv_file = StringIO()
        df.to_csv(csv_file, index=False)
        csv_file.seek(0)  # Move the cursor to the beginning of the file

        # Prepare response
        response = HttpResponse(
            csv_file.getvalue(),
            content_type='text/csv'
        )
        response['Content-Disposition'] = 'attachment; filename="users.csv"'

        return response



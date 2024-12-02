from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
# from .AirtimeAPI import VTPassAPI  # Import your VTPassAPI class
from datetime import datetime as Mdate
import random
import uuid
import json

# Initialize VTPassAPI instance
BASE_URL = "https://sandbox.vtpass.com"
AUTH_TOKEN = "Token be76014119dd44b12180ab93a92d63a2"
SECRET_KEY = "SK_873dc5215f9063f6539ec2249c8268bb788b3150386"

api = VTPassAPI(BASE_URL, AUTH_TOKEN, SECRET_KEY)

# Helper function to generate request_id
def create_random_id():
    num = random.randint(1000, 4999)
    num_2 = random.randint(5000, 8000)
    num_3 = random.randint(111, 999) * 2
    return str(num) + str(num_2) + str(num_3) + str(uuid.uuid4())

@csrf_exempt  # Disable CSRF verification for this view (not recommended for production)
def buy_airtime(request):
    if request.method == 'POST':
        try:
            # Parse incoming JSON data
            data = json.loads(request.body)
            
            # Generate request_id
            date_time_format = Mdate.now().strftime("%Y%m%d%H%M%S")
            request_id = str(date_time_format) + create_random_id()

            # Prepare the data for VTPassAPI
            vtpass_data = {
                'request_id': request_id,
                'serviceID': data.get('data_type'),  # assuming 'data_type' is sent from the front-end
                'amount': data.get('amount'),
                'phone': f"+234{data.get('mobile_number')}"  # format mobile number
            }

            # Call the buy_airtime function from VTPassAPI
            transaction_id = api.buy_airtime(vtpass_data)

            if transaction_id:
                return JsonResponse({'status': 'success', 'transaction_id': transaction_id}, status=200)
            else:
                return JsonResponse({'status': 'error', 'message': 'Failed to process the airtime purchase.'}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid data format.'}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Only POST method is allowed.'}, status=405)

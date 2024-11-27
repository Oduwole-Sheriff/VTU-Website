from .models import CustomUser
from .forms import NINForm, CustomUserForm

def account_details(request):
    user = request.user
    account_details = []
    nin_form = None
    bvn_form = None  # Initialize the BVN form
    account_message = None  # Variable to store a message if no account details

    if user.is_authenticated:
        # Check if the user has entered their NIN or BVN
        if request.method == 'POST':
            document_type = request.POST.get('document_type')

            # Handle NIN Submission
            if document_type == 'nin' and not user.nin:
                nin_form = NINForm(request.POST)
                if nin_form.is_valid():
                    user.nin = nin_form.cleaned_data['nin']
                    user.save()
                    account_details = _get_account_details(user)
                else:
                    nin_form.add_error('nin', 'Please enter a valid NIN.')
            
            # Handle BVN Submission
            elif document_type == 'bvn' and not user.bvn:
                bvn_form = CustomUserForm(request.POST, instance=user)
                if bvn_form.is_valid():
                    user.bvn = bvn_form.cleaned_data['bvn']
                    user.save()
                    account_details = _get_account_details(user)
                else:
                    bvn_form.add_error('bvn', 'Please enter a valid BVN.')

        # If NIN or BVN is already provided, just fetch account details
        else:
            if user.nin:
                account_details = _get_account_details(user)
            elif user.bvn:
                account_details = _get_account_details(user)

        # If no account details, set the message
        if not account_details:
            account_message = "You Already Have an Account, Can't Generate another Account Detail for a user. Please contact +2347046799872."

    return {
        'account_details': account_details,
        'nin_form': nin_form,
        'bvn_form': bvn_form,  # Pass the BVN form to the context
        'account_message': account_message,  # Pass the message to the template
    }

def _get_account_details(user):
    """ Helper function to extract bank account details """
    account_details = []
    if user.bank_account and 'accounts' in user.bank_account:
        for account in user.bank_account['accounts']:
            account_info = {
                'bank_name': account.get('bankName', 'No Bank Name'),
                'account_name': account.get('accountName', 'No Account Name'),
                'account_number': account.get('accountNumber', 'No Account Number')
            }
            account_details.append(account_info)
    return account_details

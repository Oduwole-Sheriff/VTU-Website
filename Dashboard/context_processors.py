from .models import CustomUser
from .forms import NINForm, CustomUserForm  # Import the form that includes BVN

def account_details(request):
    user = request.user
    account_details = []
    nin_form = None
    bvn_form = None  # Initialize the BVN form

    if user.is_authenticated:
        # Check if the user has entered their NIN
        if not user.nin:
            # If NIN is not set, display the NIN form
            if request.method == 'POST':
                nin_form = NINForm(request.POST)
                if nin_form.is_valid():
                    # Save the NIN to the user's profile
                    user.nin = nin_form.cleaned_data['nin']
                    user.save()
                    # Fetch the account details after saving the NIN
                    account_details = _get_account_details(user)
                else:
                    # If form is invalid, show errors
                    nin_form.add_error('nin', 'Please enter a valid NIN.')
            else:
                nin_form = NINForm()
        else:
            # If NIN is already provided, check for BVN
            if not user.bvn:  # Check if the BVN is not provided
                if request.method == 'POST':
                    bvn_form = CustomUserForm(request.POST, instance=user)  # Use CustomUserForm to handle BVN
                    if bvn_form.is_valid():
                        # Save the BVN to the user's profile
                        user.bvn = bvn_form.cleaned_data['bvn']
                        user.save()
                        # Fetch the account details after saving the BVN
                        account_details = _get_account_details(user)
                    else:
                        # If form is invalid, show errors
                        bvn_form.add_error('bvn', 'Please enter a valid BVN.')
                else:
                    bvn_form = CustomUserForm(instance=user)  # Pre-fill the form with the current user's data
            else:
                # If BVN is already provided, fetch the account details
                account_details = _get_account_details(user)

    return {
        'account_details': account_details,
        'nin_form': nin_form,
        'bvn_form': bvn_form,  # Pass the BVN form to the context
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

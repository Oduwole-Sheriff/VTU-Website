from .forms import NINForm, CustomUserForm

def account_details(request):
    user = request.user
    account_details = []
    nin_form = None
    bvn_form = None
    account_message = None
    has_filled_fund_form = False  # Add a flag to check if the wallet has been funded

    if user.is_authenticated:
        # Initialize the forms
        nin_form = NINForm()
        bvn_form = CustomUserForm(instance=user)

        # Check if user has already submitted the form and funded the wallet
        if user.has_filled_fund_form:
            account_details = _get_account_details(user)
            has_filled_fund_form = True
        elif user.nin or user.bvn:
            account_details = _get_account_details(user)
        else:
            account_message = "Fill the form to generate your account details."

    else:
        # For anonymous users, you could still show blank forms if needed
        nin_form = NINForm()
        bvn_form = CustomUserForm()  # No instance for anonymous users

    return {
        'account_details': account_details,
        'nin_form': nin_form,
        'bvn_form': bvn_form,
        'account_message': account_message,
        'has_filled_fund_form': has_filled_fund_form  # Include the flag in the context
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

from django import forms


class PaymentForm(forms.Form):
    """
    Form for collecting payment information.
    """
    PAYMENT_METHODS = [
        ('stripe', 'Credit Card (Stripe)'),
        ('credit_card', 'Credit Card (Legacy)'),
        ('paypal', 'PayPal'),
        ('bank_transfer', 'Bank Transfer'),
    ]
    
    payment_method = forms.ChoiceField(
        choices=PAYMENT_METHODS,
        widget=forms.RadioSelect(attrs={
            'class': 'payment-method-radio'
        }),
        initial='stripe'
    )
    
    # Credit Card Fields
    card_number = forms.CharField(
        max_length=19,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': '1234 5678 9012 3456',
            'data-payment': 'credit_card'
        })
    )
    
    expiry_month = forms.ChoiceField(
        choices=[(f'{i:02d}', f'{i:02d}') for i in range(1, 13)],
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-input',
            'data-payment': 'credit_card'
        })
    )
    
    expiry_year = forms.ChoiceField(
        choices=[(str(year), str(year)) for year in range(2025, 2036)],
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-input',
            'data-payment': 'credit_card'
        })
    )
    
    cvv = forms.CharField(
        max_length=4,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': '123',
            'data-payment': 'credit_card'
        })
    )
    
    cardholder_name = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'John Doe',
            'data-payment': 'credit_card'
        })
    )
    
    # PayPal Fields
    paypal_email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={
            'class': 'form-input',
            'placeholder': 'your@email.com',
            'data-payment': 'paypal'
        })
    )
    
    # Bank Transfer Fields
    bank_account = forms.CharField(
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Account Number',
            'data-payment': 'bank_transfer'
        })
    )
    
    bank_name = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Bank Name',
            'data-payment': 'bank_transfer'
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        payment_method = cleaned_data.get('payment_method')
        
        if payment_method == 'credit_card':
            required_fields = ['card_number', 'expiry_month', 'expiry_year', 'cvv', 'cardholder_name']
            for field in required_fields:
                if not cleaned_data.get(field):
                    self.add_error(field, 'This field is required for credit card payments.')
        
        elif payment_method == 'paypal':
            if not cleaned_data.get('paypal_email'):
                self.add_error('paypal_email', 'PayPal email is required for PayPal payments.')
        
        elif payment_method == 'bank_transfer':
            required_fields = ['bank_account', 'bank_name']
            for field in required_fields:
                if not cleaned_data.get(field):
                    self.add_error(field, 'This field is required for bank transfer payments.')
        
        return cleaned_data
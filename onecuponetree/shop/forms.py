from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Order, OrderItem, Product
#from django_countries.fields import CountryField
#from django_countries.widgets import CountrySelectWidget


class CheckoutForm(forms.Form):
    shipping_address = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': _('123 Main St, Kigali'),
            'class': 'form-control'
        }),
        label=_('Shipping Address')
    )
    shipping_address2 = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': _('Apartment or suite'),
            'class': 'form-control'
        }),
        label=_('Address 2 (Optional)')
    )
    """ shipping_country = CountryField().formfield(
        required=True,
        widget=CountrySelectWidget(attrs={
            'class': 'custom-select d-block w-100'
        }),
        label=_('Country')
    ) """
    shipping_zip = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('Postal/Zip Code')
        }),
        label=_('Zip Code')
    )
    phone_number = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+250 78X XXX XXX'
        }),
        label=_('Phone Number')
    )
    payment_option = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=(
            ('M', _('Mobile Money')),
            ('P', _('PayPal')),
            ('C', _('Credit Card')),
            ('B', _('Bank Transfer'))
        ),
        label=_('Payment Method')
    )
    same_billing_address = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(),
        label=_('Billing address same as shipping'),
        initial=True
    )
    save_info = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(),
        label=_('Save this information for next time')
    )


class CouponForm(forms.Form):
    code = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('Promo code'),
            'aria-label': _('Recipient\'s username'),
            'aria-describedby': 'basic-addon2'
        }),
        label=_('Coupon Code')
    )


class RefundForm(forms.Form):
    ref_code = forms.CharField(
        label=_('Order Reference Number'),
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('e.g. OCT-12345')
        })
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 4,
            'class': 'form-control',
            'placeholder': _('Reason for refund')
        }),
        label=_('Reason')
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'your@email.com'
        }),
        label=_('Email Address')
    )


class PaymentForm(forms.Form):
    mobile_money_number = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+250 78X XXX XXX'
        }),
        label=_('Mobile Money Number')
    )
    mtn_or_airtel = forms.ChoiceField(
        required=False,
        choices=(
            ('MTN', _('MTN Mobile Money')),
            ('AIRTEL', _('Airtel Money'))
        ),
        widget=forms.RadioSelect,
        label=_('Mobile Money Provider')
    )
    paypal_email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'paypal@email.com'
        }),
        label=_('PayPal Email')
    )
    credit_card_number = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '4242 4242 4242 4242'
        }),
        label=_('Credit Card Number'),
        max_length=19
    )
    expiry = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'MM/YY'
        }),
        label=_('Expiration Date'),
        max_length=5
    )
    cvv = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '123'
        }),
        label=_('CVV'),
        max_length=3
    )


class AddToCartForm(forms.ModelForm):
    quantity = forms.IntegerField(
        min_value=1,
        initial=1,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'style': 'width: 60px'
        })
    )

    class Meta:
        model = OrderItem
        fields = ['quantity']


class ProductFilterForm(forms.Form):
    SORT_CHOICES = (
        ('price_asc', _('Price: Low to High')),
        ('price_desc', _('Price: High to Low')),
        ('name_asc', _('Name: A-Z')),
        ('name_desc', _('Name: Z-A')),
        ('date_newest', _('Newest First')),
        ('date_oldest', _('Oldest First'))
    )

    category = forms.ModelChoiceField(
        queryset=None,  # Will be set in __init__
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control'
        }),
        label=_('Category')
    )
    min_price = forms.DecimalField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': _('Min')
        }),
        label=_('Minimum Price')
    )
    max_price = forms.DecimalField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': _('Max')
        }),
        label=_('Maximum Price')
    )
    sort_by = forms.ChoiceField(
        choices=SORT_CHOICES,
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control'
        }),
        label=_('Sort By')
    )

    def __init__(self, *args, **kwargs):
        from .models import ProductCategory
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = ProductCategory.objects.filter(is_active=True)
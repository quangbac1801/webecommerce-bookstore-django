from django import forms

class PaymentForm(forms.Form):
    order_type = forms.CharField(max_length=255, label='Loại đơn hàng')
    amount = forms.DecimalField(max_digits=10, decimal_places=2, label='Số tiền')
    order_desc = forms.CharField(widget=forms.Textarea, label='Mô tả đơn hàng')
    bank_code = forms.CharField(max_length=255, required=False, label='Mã ngân hàng')
    language = forms.CharField(max_length=10, required=False, label='Ngôn ngữ')


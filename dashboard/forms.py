from django import forms
from django.forms import ModelForm

from products.models import Product, Category,Stock,StockItem


class AddProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['category', 'image', 'title','description', 'price']

    def __init__(self, *args, **kwargs):
        super(AddProductForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class AddCategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ['name']
    

    def __init__(self, *args, **kwargs):
        super(AddCategoryForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['class'] = 'form-control'


class EditProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['category', 'image', 'title','description', 'price']

    def __init__(self, *args, **kwargs):
        super(EditProductForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class AddStockForm(ModelForm):
    class Meta:
        model = Stock
        fields = ['title', 'quantity', 'threshold']
    
    def __init__(self, *args, **kwargs):
        super(AddStockForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs['class'] = 'form-control'
        self.fields['quantity'].widget.attrs['class'] = 'form-control'
        self.fields['threshold'].widget.attrs['class'] = 'form-control'

class RequestStockForm(ModelForm):
    class Meta:
        model = StockItem
        fields = ['item','quantity']
    
    def __init__(self, *args, **kwargs):
        super(RequestStockForm, self).__init__(*args, **kwargs)
        self.fields['item'].widget.attrs['class'] = 'form-control'
        self.fields['quantity'].widget.attrs['class'] = 'form-control'



from django import forms
from .models import Supplier

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = [
            'name', 'founder_name', 'website_url', 'logo', 'image', 
            'category', 'sub_category1', 'sub_category2', 'sub_category3', 
            'sub_category4', 'sub_category5', 'sub_category6', 'email', 'contact_person_name', 
            'person_image', 'product1', 'product2', 'product3', 
            'product_image1', 'product_image2', 'product_image3', 'product_image4',
            'door_number', 'street', 'area', 'city', 'state', 
            'pin_code', 'business_description', 'phone_number'
        ]  # Explicitly include all fields from the Supplier model

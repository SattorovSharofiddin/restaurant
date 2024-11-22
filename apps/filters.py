from django_filters import FilterSet

from apps.models import Product


class ProductFilter(FilterSet):
    class Meta:
        model = Product
        fields = {
            'name': ['exact', 'icontains'],

        }

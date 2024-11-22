from django_filters import FilterSet, CharFilter

from apps.models import Category


class CategoryFilter(FilterSet):
    product_name = CharFilter(field_name='products__name', lookup_expr='icontains', label='Product Name')

    class Meta:
        model = Category
        fields = {
            'name': ['exact', 'icontains'],
        }

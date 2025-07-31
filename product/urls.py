from django.urls import path
from product.views import ProductAnalyticsView

urlpatterns = [
    path('api/products/analytics/', ProductAnalyticsView.as_view(), name='product-analytics'),
]

import hashlib
from django.core.cache import cache
from django.db.models import F, Avg, Sum, DecimalField, ExpressionWrapper
from rest_framework.views import APIView
from rest_framework.response import Response
from product.models import Product


class ProductAnalyticsView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        category = request.GET.get('category')
        min_price = request.GET.get('min_price')
        max_price = request.GET.get('max_price')

        # 🔹 Build a unique cache key based on the query parameters
        key_string = f"{category}-{min_price}-{max_price}"
        cache_key = f"product_analytics:{hashlib.md5(key_string.encode()).hexdigest()}"
        cached_response = cache.get(cache_key)

        if cached_response:
            return Response(cached_response)

        products = Product.objects.all()

        if category:
            products = products.filter(category__name__iexact=category)

        if min_price:
            try:
                products = products.filter(price__gte=float(min_price))
            except ValueError:
                return Response({"error": "Invalid min_price"}, status=400)

        if max_price:
            try:
                products = products.filter(price__lte=float(max_price))
            except ValueError:
                return Response({"error": "Invalid max_price"}, status=400)

        total_stock_value_expr = ExpressionWrapper(
            F('price') * F('stock'),
            output_field=DecimalField(max_digits=20, decimal_places=2)
        )

        analytics = products.aggregate(
            total_products=Sum(1),
            average_price=Avg('price'),
            total_stock_value=Sum(total_stock_value_expr),
        )

        response_data = {
            "total_products": analytics["total_products"] or 0,
            "average_price": round(analytics["average_price"] or 0, 2),
            "total_stock_value": round(analytics["total_stock_value"] or 0, 2)
        }

        # 🔹 Store response in cache for 5 minutes (300 seconds)
        cache.set(cache_key, response_data, timeout=300)

        return Response(response_data)

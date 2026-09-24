from apps.smartphones.models import PriceHistory,Smartphone
from django.db.models import OuterRef, Subquery

def filter_by_price(preference):
    min_price = preference.min_price
    max_price = preference.max_price

    latest_price_sq = PriceHistory.objects.filter(
        smartphone=OuterRef('pk')
    ).order_by('-created_at').values('price')[:1]

    smartphones = Smartphone.objects.annotate(
        latest_price=Subquery(latest_price_sq)
    )

    if min_price is not None:
        smartphones = smartphones.filter(latest_price__gte=min_price)

    if max_price is not None:
        smartphones = smartphones.filter(latest_price__lte=max_price)
    
    return smartphones
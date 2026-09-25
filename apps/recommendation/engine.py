from .scoring import get_phone_scores
from .price_filter import filter_by_price
from apps.users.models import UserPreference
from rest_framework.generics import get_object_or_404


def get_recommendations(user):
    user_preference = get_object_or_404(UserPreference, user=user)

    if user_preference.min_price is not None and user_preference.max_price is not None:
        if user_preference.min_price > user_preference.max_price:
            return []

    camera_weight = user_preference.camera_weight
    battery_weight = user_preference.battery_weight
    performance_weight = user_preference.performance_weight
    display_weight = user_preference.display_weight

    total_weight = (
        camera_weight + battery_weight + performance_weight + display_weight
    )

    if total_weight == 0:
        return []

    phones = filter_by_price(user_preference)

    recommendations = []

    for phone in phones:
        scores = get_phone_scores(phone)

        final_score = (
            scores["performance"] * performance_weight
            + scores["battery"] * battery_weight
            + scores["display"] * display_weight
            + scores["camera"] * camera_weight
        ) / total_weight

        if (
            user_preference.preferred_brand_id
            and phone.brand_id == user_preference.preferred_brand_id
        ):
            final_score = min(100, final_score + 10)

        recommendations.append({
            "smartphone": phone,
            "latest_price": phone.latest_price,
            "score": round(final_score, 2),
            "breakdown": scores,
        })

    recommendations.sort(key=lambda item: item["score"], reverse=True)

    return recommendations
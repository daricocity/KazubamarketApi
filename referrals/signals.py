import django.dispatch

create_referral = django.dispatch.Signal(
    providing_args=["request", "user", "position"])

from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in
from apps.carts.services.cart_merge_service import CartMergeService
from apps.carts.utils.session import CART_SESSION_KEY


@receiver(user_logged_in)
def merge_cart_on_login(sender, request, user, **kwargs):
    session_id = request.session.get(CART_SESSION_KEY)
    if not session_id:
        return

    CartMergeService().merge(
        user=user,
        session_id=session_id,
    )

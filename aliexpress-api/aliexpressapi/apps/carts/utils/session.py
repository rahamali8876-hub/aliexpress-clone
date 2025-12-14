import uuid

CART_SESSION_KEY = "cart_session_id"


def get_or_create_cart_session_id(request) -> str:
    session = request.session

    if CART_SESSION_KEY not in session:
        session[CART_SESSION_KEY] = str(uuid.uuid4())
        session.modified = True

    return session[CART_SESSION_KEY]

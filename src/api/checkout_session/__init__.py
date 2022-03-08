from flask_restx import Namespace

api = Namespace(
    "Session Operations",
    description="Session Operations",
    path="/checkout_session",
)



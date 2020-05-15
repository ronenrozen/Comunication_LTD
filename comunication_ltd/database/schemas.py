from comunication_ltd import ma
from comunication_ltd.database.models import User


class CustomerSchema(ma.Schema):
    class Meta:
        fields = ("id", "customer_name", "email", "sector", "package")

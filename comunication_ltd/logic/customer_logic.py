from comunication_ltd import db
from comunication_ltd.database.models import Customer
from comunication_ltd.database.schemas import CustomerSchema


def create_customer(customer):
    db.session.add(customer)
    db.session.commit()
    return customer


def get_all():
    customer_schema = CustomerSchema(many=True)
    return customer_schema.dump(obj=Customer.query.all())

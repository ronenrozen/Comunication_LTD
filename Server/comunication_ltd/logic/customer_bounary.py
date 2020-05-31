from comunication_ltd.database.models import Customer


class CustomerPayload:

    def __init__(self, id=None, customer_name=None, sector=None, package=None, email=None):
        self.id = id
        self.customer_name = customer_name
        self.sector = sector
        self.package = package
        self.email = email

    def serialize(self):
        return {"id": self.id,
                "customer_name": self.customer_name,
                "sector": self.sector,
                "package": self.package,
                "email": self.email}


def parse_customer(payload):
    customer_name, email, sector, package = payload.get_json().values()
    return Customer(customer_name=customer_name, email=email, sector=sector, package_id=package)

from Server.comunication_ltd import db
from Server.comunication_ltd.database.models import Customer, Package
from Server.comunication_ltd.database.schemas import CustomerSchema
from Server.comunication_ltd.logic.user_logic import response_mail_already_exist, check_sqli, response_server_error


def create_customer(customer):
    customer_db = get_customer_by_mail(customer.email)
    if not customer_db:
        if not check_sqli(customer.email) or not check_sqli(customer.customer_name) or not \
                check_sqli(customer.package_id) or not check_sqli(customer.sector):
            return response_server_error()
        db.session.add(customer)
        db.session.commit()
        return customer
    return response_mail_already_exist()


def get_all():
    customer_schema = CustomerSchema(many=True)
    customers = Customer.query.join(
        Package, Customer.package_id == Package.package_id
    ).order_by(
        Customer.id.asc()
    ).with_entities(
        Customer.id, Customer.customer_name, Customer.email, Customer.sector, Package.package_id, Package.package_price,
        Package.package_size
    ).all()
    return customer_schema.dump(obj=customers)


def delete_customer_by_id(customer_id):
    user = get_customer_by_id(customer_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return True
    else:
        return False


def get_customer_by_id(customer_id):
    return Customer.query.filter_by(id=customer_id).first()


def get_customer_by_mail(customer_email):
    return Customer.query.filter_by(email=customer_email).first()


def update_customer_by_id(customer_id, new_customer):
    customer = get_customer_by_id(customer_id)
    update_customer(customer, new_customer)
    db.session.commit()
    return customer


def update_customer(customer, new_customer):
    if customer.customer_name != new_customer.get("companyName"):
        customer.customer_name = new_customer.get("companyName")
    if customer.sector != new_customer.get("sector"):
        customer.sector = new_customer.get("sector")
    if customer.email != new_customer.get("email"):
        customer.email = new_customer.get("email")
    if customer.package_id != new_customer.get("packageId"):
        customer.package_id = new_customer.get("packageId")


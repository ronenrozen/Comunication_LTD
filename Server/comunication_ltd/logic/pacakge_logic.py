from Server.comunication_ltd import db
from Server.comunication_ltd.database.models import Package
from Server.comunication_ltd.database.schemas import PackageSchema


def create_package(package):
    db.session.add(package)
    db.session.commit()
    return package


def get_all():
    package_schema = PackageSchema(many=True)
    return package_schema.dump(obj=Package.query.all())

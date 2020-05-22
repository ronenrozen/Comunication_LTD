from comunication_ltd import ma


class CustomerSchema(ma.Schema):
    class Meta:
        fields = ("id", "company_name", "email", "sector", "package_id", "package_price", "package_size")


class PackageSchema(ma.Schema):
    class Meta:
        fields = ("package_id", "package_name")

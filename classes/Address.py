class Address:
    def __init__(self, admin_area, district, address):
        self.admin_area = admin_area
        self.district = district
        self.address = address

    def __str__(self):
        return f"{self.admin_area}, {self.district}, {self.address}"

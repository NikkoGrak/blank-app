# customer.py

class Customer:
    def __init__(self, kota, kelurahan, name, latitude, longitude):
        self.kota = kota
        self.kelurahan = kelurahan
        self.name = name
        self.latitude = latitude
        self.longitude = longitude

    def __repr__(self):
        return (f"Customer(kota={self.kota}, kelurahan={self.kelurahan}, "
                f"name={self.name}, latitude={self.latitude}, longitude={self.longitude})")

    def to_dict(self):
        return {
            "kota": self.kota,
            "kelurahan": self.kelurahan,
            "name": self.name,
            "latitude": self.latitude,
            "longitude": self.longitude
        }

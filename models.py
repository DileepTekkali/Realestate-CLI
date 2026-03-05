from dataclasses import dataclass

@dataclass
class Property:
    id: int = None
    title: str = ""
    price: float = 0.0
    area: str = ""
    property_type: str = ""
    contact: str = ""

    def __str__(self):
        return f"[{self.id}] {self.title} in {self.area} - ₹{self.price:,} ({self.property_type}) | Contact: {self.contact}"

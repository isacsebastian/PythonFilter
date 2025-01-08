
# models.py
class Client:
    def __init__(self, id, name):
        self.id = id
        self.name = name

class Product:
    def __init__(self, category, subcategory, material, description):
        self.category = category
        self.subcategory = subcategory
        self.material = material
        self.description = description

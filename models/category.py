from db.postgres import db

class Category(db.Model):
    __tablename__ = 'category'
    __table_args__ = {'schema': 'salesinsights'}
    category_id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String, nullable=False)
    subcategory = db.Column(db.String, nullable=False)
    details = db.Column(db.String, nullable=False)

    def __init__(self, category_id,category,details,subcategory):
        self.category_id = category_id
        self.category = category
        self.details = details
        self.subcategory = subcategory

    def __repr__(self):
        return f"<Category {self.category}>"

    def serialize(self):
        return {
            'category_id': self.category_id,
            'category': self.category,
            'subcategory': self.subcategory,
            'details': self.details

        }
from db.postgres import db

class Subcategory(db.Model):
    __tablename__ = 'subcategory'
    __table_args__ = {'schema': 'salesinsights'}
    subcategory_id = db.Column(db.Integer, primary_key=True)
    subcategory = db.Column(db.String, nullable=False)
    category = db.Column(db.String, nullable=False)
    details = db.Column(db.String, nullable=False)

    def __init__(self, subcategory_id,subcategory,details,category):
        self.subcategory_id = subcategory_id
        self.subcategory = subcategory
        self.details = details
        self.category = category

    def __repr__(self):
        return f"<Sub Category {self.subcategory}>"

    def serialize(self):
        return {
            'subcategory_id': self.subcategory_id,
            'subcategory': self.subcategory,
            'category': self.category,
            'details': self.details

        }
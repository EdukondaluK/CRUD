from db.postgres import db

class Department(db.Model):
    __tablename__ = 'department'
    __table_args__ = {'schema': 'salesinsights'}
    department_id = db.Column(db.Integer, primary_key=True)
    department = db.Column(db.String, nullable=False)
    category = db.Column(db.String, nullable=False)
    details = db.Column(db.String, nullable=False)

    def __init__(self, department_id,department,details,category):
        self.department_id = department_id
        self.department = department
        self.details = details
        self.category = category

    def __repr__(self):
        return f"<department {self.department}>"

    def serialize(self):
        return {
            'department_id': self.department_id,
            'department': self.department,
            'details': self.details,
            'category': self.category
        }
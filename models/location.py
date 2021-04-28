from db.postgres import db

class Location(db.Model):
    __tablename__ = 'location'
    __table_args__ = {'schema': 'salesinsights'}

    location_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    location = db.Column(db.String, nullable=False)
    department = db.Column(db.String, nullable=False)

    def __init__(self, location_id,location,department):
        self.location_id = location_id
        self.location = location
        self.department = department

    def __repr__(self):
        return f"<Location {self.location}>"

    def serialize(self):
        return {
            'location_id': self.location_id,
            'location': self.location,
            'department': self.department
        }
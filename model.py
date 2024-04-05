from config import db



class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    fileName = db.Column(db.String(50))

    def to_json(self):
        return {
            'id': self.id,
            'title': self.title,
            'fileName': self.fileName
        }


    

    
    


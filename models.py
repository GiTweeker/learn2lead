

from app import db


class Resources(db.Model):
    __tablename__ = 'resources'

    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String())
    name = db.Column(db.String())
    status = db.Column(db.String())
    donated_by = db.Column(db.Integer)
    taken_by = db.Column(db.Integer)
    requested_by = db.Column(db.Integer)

    def __init__(self,id,category,name,status,donated_by,taken_by,requested_by,created_at):
        self.id=id
        self.category=category
        self.name=name
        self.status=status
        self.donated_by=donated_by
        self.taken_by=taken_by
        self.requested_by=requested_by
        created_at = db.Column(db.DateTime)


    def __repr__(self,):
        return '<id {}>'.format(self.id)


    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category,
            'donated_by': self.donated_by,
            'status': self.status,
            'taken_by': self.taken_by,
            'requested_by': self.requested_by,
            'created_at': self.created_at
        }


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    phone_number = db.Column(db.String())
    name = db.Column(db.String())
    email = db.Column(db.String())
    sex = db.Column(db.Integer)
    user_type = db.Column(db.Integer)
    dob = db.Column(db.Integer)
    user_class = db.Column(db.Integer)
    created_at = db.Column(db.DateTime)
    address = db.Column(db.DateTime)

    def __init__(self,id,phone_number,name,email,sex,user_type,dob,user_class,created_at,address):
        self.id=id
        self.phone_number=phone_number
        self.name=name
        self.email=email
        self.sex=sex
        self.user_type=user_type
        self.dob=dob
        self.user_class=user_class
        self.created_at=created_at
        self.address=address


    def __repr__(self,):
        return '<id {}>'.format(self.id)


    def serialize(self):
        return {
            'id': self.id,
            'phone_number': self.phone_number,
            'name': self.name,
            'email': self.email,
            'sex': self.sex,
            'user_type': self.user_type,
            'dob': self.dob,
            'user_class': self.user_class,
            'created_at': self.created_at,
            'address': self.address,
        }
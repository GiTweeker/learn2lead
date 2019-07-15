
from sqlalchemy import func
from app import db

class ResourceCategories(db.Model):
    __tablename__ = 'resource_categories'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    short_name = db.Column(db.String(255), nullable=False)

class Resources(db.Model):
    __tablename__ = 'resources'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    category_id = db.Column(db.Integer, db.ForeignKey('resource_categories.id'), nullable=True)
    category = db.relationship('ResourceCategories', backref='resources', lazy='dynamic')

    name = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(10),nullable=False)

    donated_by_id = db.Column(db.Integer, db.ForeignKey('users.id'),nullable=True)
    donated_by = db.relationship('User', backref='resources', lazy='dynamic')
    #donated_by = db.relationship('User', backref=db.backref('resources'), lazy='dynamic')

    taken_by_id = db.Column(db.Integer, db.ForeignKey('users.id'),nullable=True)
    taken_by = db.relationship('User', backref='resources', lazy='dynamic')

    requested_by_id = db.Column(db.Integer, db.ForeignKey('users.id'),nullable=True)
    requested_by = db.relationship('User', backref='resources', lazy='dynamic', uselist=False)

    created_at = db.Column(db.DateTime, default=func.now())

    def __init__(self,id,category,name,status,donated_by,taken_by,requested_by,created_at):
        self.id=id
        self.category=category
        self.name=name
        self.status=status
        self.donated_by=donated_by
        self.taken_by=taken_by
        self.requested_by=requested_by
        self.created_at = created_at


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
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    phone_number = db.Column(db.String(20),nullable=False)
    name = db.Column(db.String(255),nullable=False)
    email = db.Column(db.String(255),nullable=False)
    sex = db.Column(db.String(5),nullable=True)
    user_type = db.Column(db.String(20),nullable=False)
    dob = db.Column(db.Date,nullable=True)
    user_class = db.Column(db.String(20),nullable=True)
    created_at = db.Column(db.DateTime, default=func.now())
    address = db.Column(db.String(255),nullable=False)

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
from sqlalchemy import func
from app import db


class Users(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    phone_number = db.Column(db.String(20), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    sex = db.Column(db.String(5), nullable=True)
    user_type = db.Column(db.String(20), nullable=False)
    dob = db.Column(db.Date, nullable=True)
    user_class = db.Column(db.String(20), nullable=True)
    school = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=func.now())
    address = db.Column(db.String(255), nullable=False)

    def __init__(self,phone_number, name, email, sex, user_type, dob, user_class, address):

        self.phone_number = phone_number
        self.name = name
        self.email = email
        self.sex = sex
        self.user_type = user_type
        self.dob = dob
        self.user_class = user_class
        self.address = address

    def __repr__(self):
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


class ResourceCategories(db.Model):
    __tablename__ = 'resource_categories'
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    short_name = db.Column(db.String(255), nullable=False)


class ResourceTypes(db.Model):
    __tablename__ = 'resource_types'
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    short_name = db.Column(db.String(255), nullable=False)
    category_id = db.Column(db.BigInteger, db.ForeignKey(ResourceCategories.id), nullable=True)
    category = db.relationship('ResourceCategories', backref='resourcetypes', foreign_keys=[category_id])


class Resources(db.Model):
    __tablename__ = 'resources'

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)

    type_id = db.Column(db.BigInteger, db.ForeignKey(ResourceTypes.id), nullable=True)
    type = db.relationship('ResourceTypes', backref='resources')

    name = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(10), nullable=False)

    donated_by_id = db.Column(db.BigInteger, db.ForeignKey(Users.id), nullable=True)
    donated_by = db.relationship('Users', backref='donated_by_resources', uselist=False,
                                 foreign_keys=[donated_by_id])
    # donated_by = db.relationship('User', backref=db.backref('resources'), lazy='dynamic')

    taken_by_id = db.Column(db.BigInteger, db.ForeignKey(Users.id), nullable=True)
    taken_by = db.relationship('Users', backref='taken_by_resources', uselist=False,
                               foreign_keys=[taken_by_id])

    requested_by_id = db.Column(db.BigInteger, db.ForeignKey(Users.id), nullable=True)
    requested_by = db.relationship('Users', backref='requested_by_resources', uselist=False,
                                   foreign_keys=[requested_by_id])

    created_at = db.Column(db.DateTime, default=func.now())

    def __init__(self, type_id, name, status, donated_by_id, taken_by_id, requested_by_id):
        self.type_id = type_id
        self.name = name
        self.status = status
        self.donated_by_id = donated_by_id
        self.taken_by_id = taken_by_id
        self.requested_by_id = requested_by_id

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category,
            'donated_by_id': self.donated_by_id,
            'status': self.status,
            'taken_by_id': self.taken_by_id,
            'requested_by_id': self.requested_by_id,
            'created_at': self.created_at
        }

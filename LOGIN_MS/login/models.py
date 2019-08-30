from run import db
from datetime import datetime
from pytz import *
import bcrypt
from login.idGenerator import model_id

class UserModel(db.Model):
    __tablename__ = 'users'

    userId = db.Column(db.String(10), unique=True, primary_key=True)
    userName = db.Column(db.String(100), unique=True, nullable=False)
    userPassword = db.Column(db.String(512), nullable=False)
    userFullName = db.Column(db.String(512))
    userRole = db.Column(db.String(10))
    userOrg = db.Column(db.String(20))
    createdDate = db.Column(db.DateTime(timezone=True), nullable=False)
    modifiedDate = db.Column(db.DateTime(timezone=True), nullable=False)
    createdBy = db.Column(db.String(512))
    modifiedBy = db.Column(db.String(512))


def save_to_db(self):
    user = self;
    user.userPassword = bcrypt.hashpw(user.userPassword, bcrypt.gensalt())

    eastern = timezone('Europe/London')
    loc_dt = eastern.localize(datetime.now())

    user.userId = model_id.getNewId("COM")
    user.createdDate(loc_dt);

    db.session.add(user)
    db.session.commit()


@classmethod
def update_to_db(cls, self):
    updateUser = self;

    dbuser = cls.query.filter_by(userId=updateUser.userId).first()

    dbuser.userFullName = updateUser.userFullName
    dbuser.userRole = updateUser.userRole
    dbuser.userOrg = updateUser.userOrg
    dbuser.modifiedBy = updateUser.modifiedBy

    eastern = timezone('Europe/London')
    loc_dt = eastern.localize(datetime.now())

    dbuser.modifiedDate(loc_dt);

    db.session.add(dbuser)
    db.session.commit()


@classmethod
def find_by_username(cls, userName):
    return cls.query.filter_by(userName=userName).first()


@classmethod
def find_by_userid(cls, userId):
    def to_json(x):
        return {
            'userId': x.userId,
            'userName': x.userName,
            'userPassword': x.userPassword,
            'userFullName': x.userFullName,
            'userRole': x.userRole,
            'userOrg': x.userOrg,
            'createdDate': x.createdDate,
            'modifiedDate': x.modifiedDate,
            'createdBy': x.createdBy,
            'modifiedBy': x.modifiedBy
        }
    user = cls.query.filter_by(userId=userId).first()
    return to_json(user);


@classmethod
def return_all(cls):
    def to_json(x):
        return {
            'userId':x.userId,
            'userName':x.userName,
            'userPassword':x.userPassword,
            'userFullName':x.userFullName,
            'userRole':x.userRole,
            'userOrg':x.userOrg,
            'createdDate':x.createdDate,
            'modifiedDate':x.modifiedDate,
            'createdBy':x.createdBy,
            'modifiedBy':x.modifiedBy
        }
    return {'users': list(map(lambda x: to_json(x), UserModel.query.all()))}


@classmethod
def delete_by_userid(cls, userId):
    try:
        obj = UserModel.query.filter_by(id=userId).one()
        db.session.delete(obj)
        db.session.commit()
        return {'message': 'User deleted successfully'}
    except:
        return {'message': 'Something went wrong'}
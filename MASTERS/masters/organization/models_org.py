from run import db
from datetime import datetime
from pytz import *
from masters.idGenerator import model_id


class OrgModel(db.Model):
    __tablename__ = 'withdrawal'

    organizationId = db.Column(db.String(10), unique=True, primary_key=True)
    organizationName = db.Column(db.String(100),nullable=False)
    organizationType = db.Column(db.String(512))
    organizationAddress = db.Column(db.String(512))
    organizationLocation = db.Column(db.String(512))
    organizationCity = db.Column(db.String(512))
    organizationZipCode = db.Column(db.String(512))
    organizationState = db.Column(db.String(512))
    organizationDate = db.Column(db.DateTime(timezone=True), nullable=False)
    createdDate = db.Column(db.DateTime(timezone=True), nullable=False)
    modifiedDate = db.Column(db.DateTime(timezone=True), nullable=False)
    createdBy = db.Column(db.String(512))
    modifiedBy = db.Column(db.String(512))


def save_to_db(self):
    organization = self

    eastern = timezone('Europe/London')
    loc_dt = eastern.localize(datetime.now())

    organization.organizationId = model_id.getNewId("ORG")
    organization.createdDate(loc_dt);
    db.session.add(organization)
    db.session.commit()


@classmethod
def update_to_db(cls, self):
    updateorg = self;

    dborg = cls.query.filter_by(organizationId=updateorg.organizationId).first()

    dborg.organizationName = updateorg.organizationName
    dborg.organizationType = updateorg.organizationType
    dborg.organizationAddress = updateorg.organizationAddress
    dborg.organizationLocation = updateorg.organizationLocation
    dborg.organizationCity = updateorg.organizationCity
    dborg.organizationZipCode = updateorg.organizationZipCode
    dborg.organizationState = updateorg.organizationState
    dborg.organizationDate = updateorg.organizationDate
    dborg.modifiedBy = updateorg.modifiedBy

    eastern = timezone('Europe/London')
    loc_dt = eastern.localize(datetime.now())

    dborg.modifiedDate(loc_dt);

    db.session.add(dborg)
    db.session.commit()


@classmethod
def find_by_orgid(cls, orgid):
    def to_json(x):
        return {
            'organizationId': x.organizationId,
            'organizationName': x.organizationName,
            'organizationAddress': x.organizationAddress,
            'organizationLocation': x.organizationLocation,
            'organizationCity':x.organizationCity,
            'organizationZipCode':x.organizationZipCode,
            'organizationState':x.organizationState,
            'organizationDate':x.organizationDate,
            'createdDate': x.createdDate,
            'modifiedDate': x.modifiedDate,
            'createdBy': x.createdBy,
            'modifiedBy': x.modifiedBy
        }
    organization = cls.query.filter_by(organizationId=orgid).first()
    return to_json(organization);


@classmethod
def return_all(cls):
    def to_json(x):
        return {
            'organizationId': x.organizationId,
            'organizationName': x.organizationName,
            'organizationAddress': x.organizationAddress,
            'organizationLocation': x.organizationLocation,
            'organizationCity':x.organizationCity,
            'organizationZipCode':x.organizationZipCode,
            'organizationState':x.organizationState,
            'organizationDate':x.organizationDate,
            'createdDate': x.createdDate,
            'modifiedDate': x.modifiedDate,
            'createdBy': x.createdBy,
            'modifiedBy': x.modifiedBy
        }
    return {'organizations': list(map(lambda x: to_json(x), OrgModel.query.all()))}


@classmethod
def delete_by_orgid(cls, orgid):
    try:
        obj = OrgModel.query.filter_by(organizationId=orgid).one()
        db.session.delete(obj)
        db.session.commit()
        return {'message': 'Organization deleted successfully'}
    except:
        return {'message': 'Something went wrong'}
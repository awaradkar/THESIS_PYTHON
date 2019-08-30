from run import db
from datetime import datetime
from pytz import *


class BillingModel(db.Model):
    __tablename__ = 'wh_bill_ledger'

    billingId = db.Column(db.String(10), unique=True, primary_key=True)
    depositId = db.Column(db.String(10))
    warehouseCode = db.Column(db.String())
    warehouseName = db.Column(db.String(100))
    clientId = db.Column(db.String(10))
    clientName = db.Column(db.String(100))
    commodityCode = db.Column(db.String(10))
    commodityName = db.Column(db.String(100))
    uomCode = db.Column(db.String(10))
    quantity = db.Column(db.Float(Precision='25,5'))
    noOfPacks = db.Column(db.Float(Precision='25,5'))
    startBilledDate = db.Column(db.DateTime(timezone=True), nullable=False)
    endBilledDate = db.Column(db.DateTime(timezone=True), nullable=False)
    dailyRate = db.Column(db.Float(Precision='10,5'))
    weeklyRate = db.Column(db.Float(Precision='10,5'))
    monthlyRate = db.Column(db.Float(Precision='10,5'))
    billRate = db.Column(db.Float(Precision='25,5'))
    taxComponent = db.Column(db.Float(Precision='25,5'))
    totalBill = db.Column(db.Float(Precision='25,5'))
    invoiceId = db.Column(db.String(10));
    createdBy = db.Column(db.String(100));
    createdTimeStamp = db.Column(db.DateTime(timezone=True), nullable=False)
    modifiedBy = db.Column(db.String(100));
    modifiedTimeStamp = db.Column(db.DateTime(timezone=True), nullable=False)


class DepositModel:

    def __init__(self, depositid, clientid, clientname, warehousecode, warehousename, commoditycode, commodityname, uomcode,
                 packtype, noofbags, quantity, netquantity, currenyqty, currentpacks, depositdate, lastbilleddate, billingtype):

        self.depositId = depositid
        self.clientId = clientid
        self.clientName =clientname
        self.warehouseCode =warehousecode
        self.warehouseName =warehousename
        self.commodityCode =commoditycode
        self.commodityName =commodityname
        self.uomCode =uomcode
        self.packType =packtype
        self.noOfBags =noofbags
        self.quantity =quantity
        self.netQuantity =netquantity
        self.currenyQty =currenyqty
        self.currentPacks =currentpacks
        self.depositDate =depositdate
        self.lastBilledDate =lastbilleddate
        self.billingType =billingtype


class WithdrawalModel:

    def __init__(self, withdrawalid, depositid, withdrawaldate, withDrawalnoofbags, withdrawalquantity):

        self.withdrawalId = withdrawalid;
        self.depositId = depositid
        self.withdrawalDate = withdrawaldate
        self.withdrawalNoOfBags =withDrawalnoofbags
        self.withdrawalQuantity =withdrawalquantity


class BillingMaster:

    def __init__(self, warehousecode, packtypechargemonthly, quantitytypechargemonthly, packtypechargeweekly, quantitytypechargeweekly,
                 packtypechargedaily, quantitytypechargedaily):

        self.warehouseCode = warehousecode;
        self.packTypeChargeMonthly = packtypechargemonthly
        self.quantityTypeChargeMonthly = quantitytypechargemonthly
        self.packTypeChargeWeekly = packtypechargeweekly
        self.quantityTypeChargeWeekly = quantitytypechargeweekly
        self.packTypeChargeDaily = packtypechargedaily
        self.quantityTypeChargeDaily = quantitytypechargedaily


class IdGeneratorModel:

    def __init__(self, idKey, idValue, createdDate, modifiedDate):

        self.idKey = idKey
        self.idValue = idValue
        self.createdDate = createdDate
        self.modifiedDate = modifiedDate

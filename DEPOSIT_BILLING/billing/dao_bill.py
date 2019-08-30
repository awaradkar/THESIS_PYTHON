from datetime import datetime
from xml.etree.ElementPath import prepare_descendant

from billing.models_bill import DepositModel
from billing.models_bill import WithdrawalModel
from billing.models_bill import BillingMaster
from billing.models_bill import BillingModel
from billing.dbConnection import Connection


class BillingDao:

    def getdepositlist(self):

        depositlist = [DepositModel]

        try:
            conn = Connection.connection()

            selectsql = """SELECT depositId,clientId,clientName,commodityCode,commodityName," \
                        "currentPacks,currenyQty,depositDate,netQuantity,noOfBags,billingType," \
                        "packType,quantity,uomCode,warehouseCode,warehouseName,lastBilledDate " \
                        " FROM deposit_details where " \
                        " active = %s and status = %s and isBillingCompleted = %s " \
                        " and (lastBilledDate < current_timestamp() or lastBilledDate is null) """

            cursor = conn.cursor()
            select_tuple = {"Y", "COMPLETED", "N"}

            cursor.execute(selectsql, select_tuple)
            rows = cursor.fetchall()

            for row in rows:
                deposit = DepositModel()
                deposit.depositId = row[0]
                deposit.clientId = row[1]
                deposit.clientName = row[2]
                deposit.commodityCode = row[3]
                deposit.commodityName = row[4]
                deposit.currentPacks = row[5]
                deposit.currenyQty = row[6]
                deposit.depositDate = row[7]
                deposit.netQuantity = row[8]
                deposit.noOfBags = row[9]
                deposit.billingType = row[10]
                deposit.packType = row[11]
                deposit.quantity = row[12]
                deposit.uomCode = row[13]
                deposit.warehouseCode = row[14]
                deposit.warehouseName = row[15]
                deposit.lastBilledDate = row[16]
                depositlist.append(deposit)

                return depositlist;

            cursor.close()
            conn.close()

        except:
            return {'message': 'Something went wrong'}, 500

    def getwithdrawallist(self):

        withdrwallist = [WithdrawalModel]

        try:
            conn = Connection.connection()

            selectsql = """SELECT withdrawalId,a.depositId,withDrawalNoOfBags,withdrawalDate,withdrawalQuantity," \
                               " FROM withdrawal_details a, deposit_details b where a.active = %s and a.status = %s" \
                               " and a.depositId = b.depositId and b.isBillingCompleted = %s order by createdDate asc"""

            cursor = conn.cursor()
            select_tuple = {"Y", "COMPLETED", "N"}

            cursor.execute(selectsql, select_tuple)
            rows = cursor.fetchall()

            for row in rows:
                withdrawal = WithdrawalModel()
                withdrawal.withdrawalId = row[0]
                withdrawal.depositId = row[1]
                withdrawal.withdrawalNoOfBags = row[2]
                withdrawal.withdrawalDate = row[3]
                withdrawal.withdrawalQuantity = row[4]
                withdrwallist.append(withdrawal)

            return withdrwallist

            cursor.close()
            conn.close()

        except:
            return {'message': 'Something went wrong'}, 500


    def getbillingmaster(self):

        billingMasterMap = dict

        try:
            conn = Connection.connection()

            selectsql = """SELECT warehouse,packTypeChargeMonthly,quantityTypeChargeMonthly," \
                               " packTypeChargeWeekly,quantityTypeChargeWeekly,packTypeChargeDaily,quantityTypeChargeDaily "\
                               " FROM BillingMaster"""

            cursor = conn.cursor()

            cursor.execute(selectsql)
            rows = cursor.fetchall()

            for row in rows:
                billingMaster = BillingMaster()
                wareCode = row[0];
                billingMaster.warehouseCode = wareCode
                billingMaster.packTypeChargeMonthly = row[1]
                billingMaster.quantityTypeChargeMonthly = row[2]
                billingMaster.packTypeChargeWeekly = row[3]
                billingMaster.quantityTypeChargeWeekly = row[4]
                billingMaster.packTypeChargeDaily = row[5]
                billingMaster.quantityTypeChargeDaily = row[6]
                billingMasterMap[wareCode] = billingMaster

            return billingMasterMap

            cursor.close()
            conn.close()
        except:
            return {'message': 'Something went wrong'}, 500


    def saveLedgerData(self, ledgerlist:list):

        try:
            conn = Connection.connection()
            length = 0;

            insertsql = """INSERT INTO WH_BILL_LEDGER" \
                            "(billingId,depositId,warehouseCode,warehouseName,clientId,clientName,"\
                            "commodityCode,commodityName,uomCode,quantity,noOfPacks,\
                            "startBilledDate,endBilledDate,dailyRate,weeklyRate,monthlyRate,"\
                            "billRate,taxComponent,totalBill,createdBy,createdTimeStamp) VALUES"\
                            " (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""

            cursor = conn.cursor()

            val:list

            for record in ledgerlist:
                ledger:BillingModel = record
                select_tuple = {ledger.billingId, ledger.depositId, ledger.warehouseCode, ledger.warehouseName, ledger.clientId, ledger.clientName,
                                ledger.commodityCode, ledger.commodityName, ledger.uomCode, ledger.quantity, ledger.noOfPacks, ledger.startBilledDate,
                                ledger.endBilledDate, ledger.dailyRate, ledger.weeklyRate, ledger.monthlyRate, ledger.billRate,
                                ledger.taxComponent, ledger.totalBill, ledger.createdBy, datetime.now()}
                val.append(select_tuple);

            cursor.executemany(insertsql, val)

            conn.commit();

            length = cursor.rowcount

            return length

            cursor.close()
            conn.close()

        except:
            return {'message': 'Something went wrong'}, 500

        return length
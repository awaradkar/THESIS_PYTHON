from billing.dao_bill import BillingDao
from billing.dao_idGenerator import IdGeneratorDao
from billing.models_bill import BillingModel
from datetime import datetime
from billing.models_bill import WithdrawalModel
from billing.models_bill import DepositModel
from billing.models_bill import BillingMaster
from decimal import Decimal
from datetime import timedelta
from dateutil import relativedelta

class BillingService:

    def runbilling(self):
        responseStr = "";

        billingDao = BillingDao();

        depositlist =  billingDao.getdepositlist()
        withdrawallist = billingDao.getwithdrawallist()

        billingmastermap = billingDao.getbillingmaster()

        whbillledgerlist = list

        depMap = dict

        filteredsize = 0;

        for withdrawal in withdrawallist:
            if withdrawal.depositId not in depMap:
                withdrawallistdep:list = filter(lambda x: withdrawal.depositId == x.depositId, withdrawallist)
                depMap[withdrawal.depositId] = withdrawallistdep
                filteredsize = filteredsize + len(withdrawallistdep)

            if filteredsize == len(withdrawallist):
                    break

        for deposit in depositlist:
            lst:list = depMap[deposit.depositId]
            master = billingmastermap[deposit.warehouseCode]

            if len(lst) > 0:
                billledgers = self.calculatewithdrawal(deposit, master, lst)
                whbillledgerlist.extend(billledgers)
            else:
                billledger = self.calculatewithoutwithdrawal(deposit, master)
                whbillledgerlist.append(billledger)

        count = billingDao.saveLedgerData(whbillledgerlist);
        responseStr = "No of records updated:" + count;
        return responseStr;



    def calculatewithdrawal(self, deposit, master, lst):

        whbillledgerlist = list

        previousBillingDate:datetime
        newBillingDate:datetime

        withdrawalQty:float
        withdrawalPacks:float

        n = len(lst)

        for i in range(n):
            withdrawal:WithdrawalModel = lst[i]

            if(i != 0):
                withdrawalQty = withdrawalQty + withdrawal.withdrawalQuantity
                withdrawalPacks = withdrawalQty + withdrawal.withdrawalNoOfBags

            if(i==0):
                if deposit.lastBilledDate is None:
                    previousBillingDate = deposit.depositDate
                else:
                    previousBillingDate = deposit.lastBilledDate + timedelta(days=1)

                newBillingDate = withdrawal.withdrawalDate
            elif (n>0 & i==n-1):
                withDraw: WithdrawalModel = lst[i - 1]
                previousBillingDate = withDraw.withdrawalDate + timedelta(days=1)
                newBillingDate = datetime.now();
            else:
                withDraw: WithdrawalModel = lst[i - 1]
                previousBillingDate = withDraw.withdrawalDate + timedelta(days=1)
                newBillingDate = withdrawal.withdrawalDate

        billingService = BillingService()
        billing:BillingModel

        billing = self.getwhbillledger(deposit, master, withdrawalQty, withdrawalPacks, previousBillingDate, newBillingDate);
        whbillledgerlist.append(billing)

        return whbillledgerlist;

    def calculatewithoutwithdrawal(self, deposit:DepositModel, master:BillingMaster):
        newBillingDate:datetime = datetime.now()

        billledger = BillingModel()

        if deposit.lastBilledDate is None:
            previousBillingDate = deposit.depositDate
        else:
            previousBillingDate = deposit.lastBilledDate

        difference = relativedelta.relativedelta(previousBillingDate, newBillingDate)

        years = difference.years
        months = difference.months
        days = difference.days
        totalMonths = years * 12 + months
        weeks = days / 7
        remainingDays = days % 7

        if deposit.billingType is "P":
            monthlyRate = master.packTypeChargeWeekly
            weeklyRate = master.packTypeChargeWeekly
            dailyRate = master.packTypeChargeDaily

            billamount = monthlyRate*totalMonths*deposit.noOfBags
            billamount = billamount + (weeklyRate*weeks*deposit.noOfBags)
            billamount = billamount + (dailyRate*remainingDays*deposit.noOfBags)
        else:
            monthlyRate = master.quantityTypeChargeMonthly
            weeklyRate = master.quantityTypeChargeWeekly
            dailyRate = master.quantityTypeChargeDaily

            billamount = monthlyRate * totalMonths * deposit.netQuantity
            billamount = billamount + (weeklyRate * weeks * deposit.netQuantity)
            billamount = billamount + (dailyRate * remainingDays * deposit.netQuantity)

        taxamount:Decimal = billamount*10/100

        idGeneratordao = IdGeneratorDao();

        billledger.billingId = idGeneratordao.getnewid("BILL")
        billledger.billRate = billamount
        billledger.clientId = deposit.clientId
        billledger.clientName = deposit.clientName
        billledger.commodityCode = deposit.commodityCode
        billledger.commodityName = deposit.commodityName
        billledger.dailyRate = dailyRate
        billledger.depositId = deposit.depositId
        billledger.monthlyRate = monthlyRate
        billledger.noOfPacks = deposit.noOfBags
        billledger.quantity = deposit.netQuantity
        billledger.startBilledDate = previousBillingDate
        billledger.endBilledDate = newBillingDate
        billledger.taxComponent = taxamount
        billledger.createdTimeStamp = datetime.now()
        billledger.totalBill = billamount + taxamount
        billledger.uomCode = deposit.uomCode
        billledger.warehouseCode = deposit.warehouseCode
        billledger.warehouseName = deposit.warehouseName
        billledger.weeklyRate = weeklyRate

        return billledger

    def getwhbillledger(deposit:DepositModel, master:BillingMaster, withdrawalQty:Decimal, withdrawalPacks:Decimal,
                        previousbillingDate:datetime, newbillingDate:datetime):

        billledger = BillingModel();

        difference = relativedelta.relativedelta(previousbillingDate, newbillingDate)

        years = difference.years
        months = difference.months
        days = difference.days
        totalMonths = years * 12 + months
        weeks = days / 7
        remainingDays = days % 7

        billnoofbags = deposit.noOfBags - withdrawalPacks
        billnoofqty = deposit.netQuantity - withdrawalQty

        if deposit.billingType is "P":
            monthlyRate = master.packTypeChargeWeekly
            weeklyRate = master.packTypeChargeWeekly
            dailyRate = master.packTypeChargeDaily

            billamount = monthlyRate*totalMonths*billnoofbags
            billamount = billamount + (weeklyRate*weeks*billnoofbags)
            billamount = billamount + (dailyRate*remainingDays*billnoofbags)
        else:
            monthlyRate = master.quantityTypeChargeMonthly
            weeklyRate = master.quantityTypeChargeWeekly
            dailyRate = master.quantityTypeChargeDaily

            billamount = monthlyRate * totalMonths * billnoofqty
            billamount = billamount + (weeklyRate * weeks * billnoofqty)
            billamount = billamount + (dailyRate * remainingDays * billnoofqty)

        taxamount:Decimal = billamount*10/100

        idGeneratordao = IdGeneratorDao();

        billledger.billingId = idGeneratordao.getnewid("BILL")
        billledger.billRate = billamount
        billledger.clientId = deposit.clientId
        billledger.clientName = deposit.clientName
        billledger.commodityCode = deposit.commodityCode
        billledger.commodityName = deposit.commodityName
        billledger.dailyRate = dailyRate
        billledger.depositId = deposit.depositId
        billledger.monthlyRate = monthlyRate
        billledger.noOfPacks = billnoofbags
        billledger.quantity = billnoofqty
        billledger.startBilledDate = previousbillingDate
        billledger.endBilledDate = newbillingDate
        billledger.taxComponent = taxamount
        billledger.createdTimeStamp = datetime.now()
        billledger.totalBill = billamount + taxamount
        billledger.uomCode = deposit.uomCode
        billledger.warehouseCode = deposit.warehouseCode
        billledger.warehouseName = deposit.warehouseName
        billledger.weeklyRate = weeklyRate

        return billledger

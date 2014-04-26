from django.db import models
from jdatetime import datetime as jalali_datetime
from rose_config.models import Town, Province, JobType, JobCertificateType, Bank, VasigheType, BusinessPlace

CUSTOMER_TYPE = (
    ("haghighi", "haghighi"),
    ("hoghooghi", "haghighi"),
)


class CustomerInformation(models.Model):
    type = models.CharField(choices=CUSTOMER_TYPE, max_length=30)
    national_number = models.CharField(max_length=10, primary_key=True)
    cif = models.CharField(max_length=20)
    name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    father_name = models.CharField(max_length=50)
    bc_number = models.CharField(max_length=20)
    bc_serial_number = models.CharField(max_length=20)
    birth_date = models.DateTimeField()
    bc_place = models.CharField(max_length=100)
    birth_place = models.CharField(max_length=100)
    gender = models.CharField(max_length=10)

    def get_persian_birth_date(self):
        return jalali_datetime.fromgregorian(datetime=self.birth_date).strftime('%Y/%m/%d')

    @staticmethod
    def from_dic(dic):
        birth_date = dic['birth_date']
        birth_date_parts = birth_date.split('/')
        gregorian_birth_date = jalali_datetime(int(birth_date_parts[0]), int(birth_date_parts[1]),
                                               int(birth_date_parts[2])).togregorian()
        cif = str(long(dic['national_number']))
        c = CustomerInformation(type=dic['type'], cif=cif, national_number=dic['national_number'],
                                name=dic['name'], last_name=dic['last_name'], father_name=dic['father_name'],
                                bc_number=dic['bc_number'], bc_serial_number=dic['bc_serial_number'],
                                birth_date=gregorian_birth_date, bc_place=dic['bc_place'],
                                birth_place=dic['birth_place'], gender=dic['gender'])

        return c


class ContactInformation(models.Model):
    customer = models.OneToOneField(CustomerInformation, related_name='contact_info', primary_key=True)
    phone_number = models.CharField(max_length=16)
    cell_number = models.CharField(max_length=16)
    email = models.EmailField()
    address = models.CharField(max_length=300)
    town = models.ForeignKey(Town)
    province = models.ForeignKey(Province)
    postal_code = models.CharField(max_length=20)

    @staticmethod
    def from_dic(dic):
        c = ContactInformation(
            customer_id=dic["customer_id"],
            phone_number=dic["phone_number"], cell_number=dic["cell_number"], email=dic["email"],
            address=dic["email"], town_id=dic['town_id'], province_id=dic['province_id'],
            postal_code=dic['postal_code'])
        return c


class JobInformation(models.Model):
    customer = models.OneToOneField(CustomerInformation, related_name='job_info', primary_key=True)
    job = models.ForeignKey(JobType)
    job_activity = models.CharField(max_length=100)
    Job_certificate = models.ForeignKey(JobCertificateType)
    job_certificate_number = models.CharField(max_length=25)
    job_province = models.ForeignKey(Province)
    job_town = models.ForeignKey(Town)
    job_contact_number = models.CharField(max_length=30)
    job_postal_code = models.CharField(max_length=30)
    job_address = models.CharField(max_length=700)

    @staticmethod
    def from_dic(dic):
        j = JobInformation(
            customer_id=dic['customer_id'],
            job_id=dic['job_id'],
            job_activity=dic['job_activity'],
            Job_certificate_id=dic["Job_certificate_id"],
            job_certificate_number=dic["job_certificate_number"],
            job_province_id=dic[
                "job_province_id"], job_town_id=
            dic["job_town_id"],
            job_contact_number=dic['job_contact_number'], job_address=dic['job_address'],
            job_postal_code=dic['job_postal_code'])
        return j


class AssetInformation(models.Model):
    customer = models.OneToOneField(CustomerInformation, related_name='asset_info', primary_key=True)
    cash = models.BigIntegerField(default=0)
    account = models.BigIntegerField(default=0)
    business_place = models.ForeignKey(BusinessPlace)
    business_place_value = models.BigIntegerField(default=0)
    individual_credit_amount = models.BigIntegerField(default=0)
    company_credit_amount = models.BigIntegerField(default=0)
    manghool_value = models.BigIntegerField(default=0)
    no_manghool_value = models.BigIntegerField(default=0)
    vehicles_value = models.BigIntegerField(default=0)
    individual_debit_amount = models.BigIntegerField(default=0)
    company_debit_amount = models.BigIntegerField(default=0)
    bank_debit_amount = models.BigIntegerField(default=0)

    @staticmethod
    def from_dic(dic):
        asset = AssetInformation(
            customer_id=dic['customer_id'],
            cash=dic['cash'],
            account=dic['account'],
            business_place_id=dic['business_place_id'],
            business_place_value=dic['business_place_value'],
            individual_credit_amount=dic['individual_credit_amount'],
            company_credit_amount=dic['company_credit_amount'],
            manghool_value=dic['manghool_value'],
            no_manghool_value=dic['no_manghool_value'],
            vehicles_value=dic['vehicles_value'],
            individual_debit_amount=dic['individual_debit_amount'],
            company_debit_amount=dic['company_debit_amount'],
            bank_debit_amount=dic['bank_debit_amount']

        )
        return asset


class SanadMelkiInformation(models.Model):
    sanad_no = models.CharField(max_length=30)
    owner_name = models.CharField(max_length=60)
    current_value = models.BigIntegerField()
    address = models.CharField(max_length=500)

    @staticmethod
    def from_dic(dic, ):
        sanad = SanadMelkiInformation(sanad_no=dic['sanad_no'],
                                      owner_name=dic['owner_name'],
                                      current_value=dic['current_value'],
                                      address=dic['address']
        )

        return sanad


class BankIncomeInformation(models.Model):
    customer = models.OneToOneField(CustomerInformation, related_name='bank_income_info', primary_key=True)
    banks = models.ManyToManyField(Bank, null=True, blank=True)
    income = models.IntegerField()
    vasighe_types = models.ManyToManyField(VasigheType, null=True, blank=True)
    sanad_melki_info = models.ForeignKey(SanadMelkiInformation, blank=True, null=True)


    @staticmethod
    def from_dic(dic, sanad):
        if sanad is None:
            bi = BankIncomeInformation(income=dic['income'], customer_id=dic['customer_id'])
        else:
            bi = BankIncomeInformation(income=dic['income'], customer_id=dic['customer_id'],
                                       sanad_melki_info_id=sanad.id)
        bi.save()
       # if bi.sanad_melki_info:
       #     bi.sanad_melki_info.delete()

        bi.vasighe_types.clear()
        bi.banks.clear()
        bi.vasighe_types = dic.getlist('vasighe_types')
        bi.banks = dic.getlist('banks')
        return bi









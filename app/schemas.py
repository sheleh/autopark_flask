from datetime import date
from marshmallow import fields, validate, validates_schema, ValidationError, RAISE
from app import ma
from app.accounts.models import User
from app.companys.models import Company
from app.offices.models import Office
from app.vehicles.models import Vehicle


class AdminUserSchema(ma.SQLAlchemySchema):
    email = fields.Email(required=True, validate=[validate.Length(min=2, max=80)])
    first_name = fields.String(required=True, validate=[validate.Length(min=2, max=100)])
    last_name = fields.String(required=True, validate=[validate.Length(min=2, max=100)])
    password = fields.String(required=True, validate=[validate.Length(min=2, max=50)])
    confirm_password = fields.String(required=True, validate=[validate.Length(min=2, max=50)])

    @validates_schema
    def validate_password(self, data, **kwargs):
        if data["password"] != data["confirm_password"]:
            raise ValidationError("Passwords did not matched")

    class Meta:
        model = User
        ordered = True
        fields = ['email', 'first_name', 'last_name', 'password', 'confirm_password', ]


class CompanySchema(ma.SQLAlchemySchema):
    name = fields.String(required=True, validate=[validate.Length(min=2, max=100)])
    address = fields.String(required=False, validate=[validate.Length(min=2, max=150)])

    class Meta:
        model = Company
        unknown = RAISE
        ordered = True
        fields = ['id', 'name', 'address']


class UserSchema(ma.SQLAlchemySchema):
    email = fields.Email(required=True, validate=[validate.Length(min=2, max=80)])
    first_name = fields.String(required=True, validate=[validate.Length(min=2, max=100)])
    last_name = fields.String(required=True, validate=[validate.Length(min=2, max=100)])
    password = fields.String(required=True, validate=[validate.Length(min=2, max=50)])
    company_id = fields.Integer(required=False)
    company = fields.Nested(CompanySchema())

    class Meta:
        model = User
        ordered = True
        fields = ['id', 'email', 'first_name', 'last_name', 'password', 'company_id', 'company']


class OfficeSchema(ma.SQLAlchemySchema):
    name = fields.String(required=True, validate=[validate.Length(min=1, max=100)], unique=True)
    address = fields.String(required=False, validate=[validate.Length(min=8, max=150)])
    country = fields.String(required=False, validate=[validate.Length(min=3, max=50)])
    city = fields.String(required=False, validate=[validate.Length(min=3, max=50)])
    company_id = fields.Integer(required=False)
    region = fields.String(required=False)
    company = fields.Nested(CompanySchema(exclude=['address']))

    class Meta:
        model = Office
        ordered = True
        unknown = RAISE
        fields = ['id', 'name', 'address', 'country', 'city', 'region', 'company', 'company_id']


class VehicleSchema(ma.SQLAlchemySchema):
    license_plate = fields.String(required=True, validate=[validate.Length(min=2, max=15)])
    name = fields.String(required=True, validate=[validate.Length(min=1, max=100)])
    model = fields.String(required=True, validate=[validate.Length(min=1, max=50)])
    year_of_manufacture = fields.Integer(required=True, validate=[validate.Range(min=1885, max=int(date.today().year))])
    company_id = fields.Integer(required=False)
    company = fields.Nested(CompanySchema(exclude=['address']))
    office_id = fields.Integer(required=False)
    driver_id = fields.Integer(required=False)
    driver = fields.Nested(UserSchema(many=True, only=['id', 'email']))

    class Meta:
        model = Vehicle
        unknown = RAISE
        ordered = True
        fields = ['id', 'license_plate', 'name', 'model', 'year_of_manufacture',
                  'company', 'company_id', 'office_id', 'driver_id', 'driver']


admin_form_schema = AdminUserSchema()
user_create_form_schema = UserSchema()
user_login_form_schema = UserSchema(only=('email', 'password'))
single_user_form_schema = UserSchema(only=('id', 'email', 'first_name', 'last_name', 'company_id'))
single_user_update_form_schema = UserSchema(partial=True, dump_only=('email',))
users_form_schema = UserSchema(many=True, only=('id', 'email', 'first_name', 'last_name', 'company_id'))

company_form_schema = CompanySchema()
company_list_form_schema = CompanySchema(many=True)
company_update_form_schema = CompanySchema(partial=True)

user_profile_form_schema = UserSchema(only=('email', 'first_name', 'last_name'))
user_update_profile_form_schema = UserSchema(
    partial=True, only=('email', 'first_name', 'last_name', 'password'), dump_only=('email',), load_only=('password',)
)

office_form_schema = OfficeSchema()
office_get_form_schema = OfficeSchema(exclude=('id', 'company', 'company_id'))
offices_with_company_info_list_form_schema = OfficeSchema(many=True, exclude=('company_id',))
offices_list_form_schema = OfficeSchema(many=True, exclude=('company', 'company_id'))
offices_update_form_schema = OfficeSchema(partial=True)

vehicle_create_form_schema = VehicleSchema()
vehicle_list_form_schema = VehicleSchema(many=True, exclude=('company_id', 'office_id'))
vehicle_update_form_schema = VehicleSchema()
vehicle_staff_form_schema = VehicleSchema(many=True, exclude=('driver', 'company_id', 'office_id', 'company'))

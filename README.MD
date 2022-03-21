
run application  = python3 run.py or flask run

# +++ 1 +++
# Admin user registration
POST {url}:5000/api/admin/registration/
params: {
    "email": "elon@admin.com",
    "first_name": "Elon",
    "last_name": "Musk",
    "password": "password",
    "confirm_password": "password"
}
# Company registration (admin permissions required)
POST {url}:5000/api/company/ Headers(Authorization: Bearer {token})
params: {
    "name": "Tesla",
    "address": "addresss123445"
}
# +++ 2 +++
# User Login
POST {url}:5000/api/login
params: {
    "email": "elon@admin.com",
    "password": "password"
}
response:
{
    "message": "Logged message",
    "access_token": "JWT Token",
    "refresh": "JWT Refresh Token"
}
# User Logout
POST {url}:5000/api/login  Headers(Authorization: Bearer {token})
# +++ 3 +++
# Workers register/list
POST {url}:5000/api/users/  Headers(Authorization: Bearer {token})
params: {
    "email": "vasya@mail.ru",
    "password": "password",
    "first_name": "Vasiliy",
    "last_name": "Pupkin"
}
response:
{
    "message": "Logged message",
    "access_token": "JWT Token",
    "refresh": "JWT Refresh Token"id
}
# View list of Users
GET {url}:5000/api/users/  Headers(Authorization: Bearer {token})
response:
{"users": [{
            "id": [],
            "email": "[email]",
            "first_name": "[first name]",
            "last_name": "[second name]",
            "company_id": [company id]
        }]}
# Filters "first_name", "last_name", "email"
GET {url}:5000/api/users/?first_name={key}  Headers(Authorization: Bearer {token})

# +++4+++
# Worker view/update/delete
GET {url}:5000/api/users/{id}  Headers(Authorization: Bearer {token})
response:
{
    "id": [],
    "email": "[email]",
    "first_name": "[first name]",
    "last_name": "[last name]",
    "company_id": [company id]
}
PUT {url}:5000/api/users/{id}  Headers(Authorization: Bearer {token})
response: "User has been updated"
DELETE {url}:5000/api/users/{id}  Headers(Authorization: Bearer {token})
response: "User has been deleted"

# +++5+++
#  Company view
GET {url}:5000/api/company/ Headers(Authorization: Bearer {token})
response:
{"company": [{
            "id": [],
            "name": "[company name]",
            "address": "[company address]"
        }]}

# +++ 6 +++
# Company edit
PUT {url}:5000/api/company/{id} Headers(Authorization: Bearer {token})
request:
{
    "name": "[company name]",
    "address": "[company address]"
}
response: 
{ "message": "Company Tesla has been updated" }
# +++ 7 +++
# MyProfile view/edit   5000/profile/
GET {url}:5000/api/profile/ Headers(Authorization: Bearer {token})
response:
{
    "email": "[email]",
    "first_name": "[first name]",
    "last_name": "[last name]"
}

PUT {url}:5000/api/profile/ Headers(Authorization: Bearer {token})
request:
{
    "first_name": "[first name]",
    "last_name": "[last name]"
}
response: 
{ "message": "User [] has been updated" }

# +++ 8 +++ 
# Create offices/view list of offices
POST {url}:5000/api/offices/ Headers(Authorization: Bearer {token})
request: 
{
    "name": "[company name]",
    "address": "[company address]",
    "country": "[country]",
    "city": "[city]",
    "region": "[region]"
}
response:
{"message": "Office with name [name] was created"}

GET {url}:5000/api/offices/ Headers(Authorization: Bearer {token})
response:
"offices": [
        {
            "id": [],
            "name": "[name]",
            "address": "[address]",
            "country": "[country]",
            "city": "[city]",
            "region": "[region]"
}]

GET {url}:5000/api/offices/?country=[country] Headers(Authorization: Bearer {token})
GET {url}:5000/api/offices/?city=[city] Headers(Authorization: Bearer {token})
GET {url}:5000/api/offices/?city=[city]&country=[country] Headers(Authorization: Bearer {token})
response:
"offices": [
        {
            "id": [],
            "name": "[name]",
            "address": "[address]",
            "country": "[country]",
            "city": "[city]",
            "region": "[region]"
}]

# +++ 9 +++
# Offices retrieve/update/delete
GET {url}:5000/api/offices/{id}  Headers(Authorization: Bearer {token})
response:
{
    "name": "[name]",
    "address": "[address]",
    "country": "[country]",
    "city": "[city]",
    "region": "[region]"
}

PUT {url}:5000/api/offices/{id}  Headers(Authorization: Bearer {token})
request:
{
    "name": "[name]",
    "address": "[address]",
    "country": "[country]",
    "city": "[city]",
    "region": "[region]"
}
response:
{"message": "Office [name] has been updated"}

# +++ 10 +++ 
# Assign worker to an office
PUT {url}:5000/api/office/{office id}/assign/{worker id} Headers(Authorization: Bearer {token})
response:
{"message": "User [email] has been assigned to [office name]"}

# +++ 11 +++
# View my office
GET {url}:5000/api/my_office/ Headers(Authorization: Bearer {token})

# +++ 12 +++
#  Vehicle list/create
POST {url}:5000/api/vehicle/ Headers(Authorization: Bearer {token})
request:
{
    "license_plate": "[license plate]",
    "name": "[name]",
    "model": "[model]",
    "year_of_manufacture": 'year'
}
response: {"message": "Vehicle T999 Tesla was created"}

GET {url}:5000/api/vehicle/ Headers(Authorization: Bearer {token})
response:
"vehicles": [
        {
            "id": 1,
            "license_plate": "[license]",
            "name": "[name]",
            "model": "[model]",
            "year_of_manufacture": "year",
            "driver": [{}]
        },]
GET {url}:5000/api/vehicle/?office_id={id} Headers(Authorization: Bearer {token})
GET {url}:5000/api/vehicle/?driver_id={id} Headers(Authorization: Bearer {token})
GET {url}:5000/api/vehicle/?driver_id={id}&office_id={id} Headers(Authorization: Bearer {token})

# +++ 13 +++ 
# Vehicle view/update/delete
GET {url}:5000/api/vehicle/{id}  Headers(Authorization: Bearer {token})
response:
{
    "id": 1,
    "license_plate": "[license plate]",
    "name": "[Name]",
    "model": "[Model]",
    "year_of_manufacture": 'year',
    "driver": []
}

PUT {url}:5000/api/vehicle/{id} Headers(Authorization: Bearer {token})
{
        "license_plate": ['license_plate'],
        "name": ['name'],
        "model": ['model'],
        "year_of_manufacture": 'year_of_manufacture',
        "office_id": 'id',
        "driver_id": 'id',
}
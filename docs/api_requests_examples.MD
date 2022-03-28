
##1. Admin user registration
POST {url}:5000/api/admin/registration/</br>

request:
<pre>
{
    "email": "elon@admin.com",
    "first_name": "Elon",
    "last_name": "Musk",
    "password": "password",
    "confirm_password": "password"
}
</pre>
## Company registration (admin permissions required)
POST {url}:5000/api/company/ Headers(Authorization: Bearer {token})</br>

request:
<pre>
{
    "name": "Tesla",
    "address": "addresss123445"
}
</pre>

## 2. User Login
POST {url}:5000/api/login<br/>

request:
<pre>
{
    "email": "elon@admin.com",
    "password": "password"
}
</pre>
response:
<pre>
{
    "message": "Logged message",
    "access_token": "JWT Token",
    "refresh": "JWT Refresh Token"
}
</pre>
### User Logout
POST {url}:5000/api/login  Headers(Authorization: Bearer {token})


## 3. Workers register/list
POST {url}:5000/api/users/  Headers(Authorization: Bearer {token})<br>

request:
<pre>
{
    "email": "vasya@mail.ru",
    "password": "password",
    "first_name": "Vasiliy",
    "last_name": "Pupkin"
}
</pre>
response:
<pre>
{
    "message": "Logged message",
    "access_token": "JWT Token",
    "refresh": "JWT Refresh Token"id
}
</pre>
### View list of Users
GET {url}:5000/api/users/  Headers(Authorization: Bearer {token})</br>

response:
<pre>
{"users": [{
            "id": [],
            "email": "[email]",
            "first_name": "[first name]",
            "last_name": "[second name]",
            "company_id": [company id]
        }]}
</pre>
### Filters "first_name", "last_name", "email"
GET {url}:5000/api/users/?first_name={key}  Headers(Authorization: Bearer {token})


##4.  Worker view/update/delete
GET {url}:5000/api/users/{id}  Headers(Authorization: Bearer {token})<br>

response:
<pre>
{
    "id": [],
    "email": "[email]",
    "first_name": "[first name]",
    "last_name": "[last name]",
    "company_id": [company id]
}
</pre>
PUT {url}:5000/api/users/{id}  Headers(Authorization: Bearer {token})<br/>

response: 
<pre>"User has been updated"</pre>
DELETE {url}:5000/api/users/{id}  Headers(Authorization: Bearer {token})<br/>

response:
<pre>"User has been deleted"</pre>


## 5. Company view
GET {url}:5000/api/company/ Headers(Authorization: Bearer {token})</br>

response:
<pre>
{"company": 
    [{
        "id": [],
        "name": "[company name]",
        "address": "[company address]"
    }]
}
</pre>

##6. Company edit
PUT {url}:5000/api/company/{id} Headers(Authorization: Bearer {token})</br>

request:
<pre>
{
    "name": "[company name]",
    "address": "[company address]"
}
</pre>
response: 
<pre>{ "message": "Company Tesla has been updated" }</pre>

##7. MyProfile view/edit   5000/profile/
GET {url}:5000/api/profile/ Headers(Authorization: Bearer {token})</br>

response:
<pre>
{
    "email": "[email]",
    "first_name": "[first name]",
    "last_name": "[last name]"
}
</pre>
PUT {url}:5000/api/profile/ Headers(Authorization: Bearer {token})</br>

request:
<pre>
{
    "first_name": "[first name]",
    "last_name": "[last name]"
}
</pre>
response:
<pre>
{ "message": "User [] has been updated" }
</pre>
 
##8. Create offices/view list of offices
POST {url}:5000/api/offices/ Headers(Authorization: Bearer {token})</br>

request: 
<pre>
{
    "name": "[company name]",
    "address": "[company address]",
    "country": "[country]",
    "city": "[city]",
    "region": "[region]"
}
</pre>
response:
<pre>{"message": "Office with name [name] was created"}</pre>

GET {url}:5000/api/offices/ Headers(Authorization: Bearer {token})<br/>

response:
<pre>
"offices": [
        {
            "id": [],
            "name": "[name]",
            "address": "[address]",
            "country": "[country]",
            "city": "[city]",
            "region": "[region]"
}]
</pre>

GET {url}:5000/api/offices/?country=[country] Headers(Authorization: Bearer {token})</br>
GET {url}:5000/api/offices/?city=[city] Headers(Authorization: Bearer {token})</br>
GET {url}:5000/api/offices/?city=[city]&country=[country] Headers(Authorization: Bearer {token})</br>

response:
<pre>
"offices": [
        {
            "id": [],
            "name": "[name]",
            "address": "[address]",
            "country": "[country]",
            "city": "[city]",
            "region": "[region]"
}]
</pre>

##9. Offices retrieve/update/delete
GET {url}:5000/api/offices/{id}  Headers(Authorization: Bearer {token})</br>

response:
<pre>
{
    "name": "[name]",
    "address": "[address]",
    "country": "[country]",
    "city": "[city]",
    "region": "[region]"
}
</pre>

PUT {url}:5000/api/offices/{id}  Headers(Authorization: Bearer {token})</br>

request:
<pre>
{
    "name": "[name]",
    "address": "[address]",
    "country": "[country]",
    "city": "[city]",
    "region": "[region]"
}
</pre>
response:
<pre>
{"message": "Office [name] has been updated"}
</pre>

##10. Assign worker to an office
PUT {url}:5000/api/office/{office id}/assign/{worker id} Headers(Authorization: Bearer {token})</br>

response:
<pre>
{"message": "User [email] has been assigned to [office name]"}
</pre>


##11. View my office
GET {url}:5000/api/my_office/ Headers(Authorization: Bearer {token})

##12.  Vehicle list/create
POST {url}:5000/api/vehicle/ Headers(Authorization: Bearer {token})</br>


request:
<pre>
{
    "license_plate": "[license plate]",
    "name": "[name]",
    "model": "[model]",
    "year_of_manufacture": 'year'
}
</pre>
response: 

<pre>
{"message": "Vehicle T999 Tesla was created"}
</pre>

GET {url}:5000/api/vehicle/ Headers(Authorization: Bearer {token})</br>

response:
<pre>
"vehicles": [
        {
            "id": 1,
            "license_plate": "[license]",
            "name": "[name]",
            "model": "[model]",
            "year_of_manufacture": "year",
            "driver": [{}]
        },]
</pre>
GET {url}:5000/api/vehicle/?office_id={id} Headers(Authorization: Bearer {token})</br>
GET {url}:5000/api/vehicle/?driver_id={id} Headers(Authorization: Bearer {token})</br>
GET {url}:5000/api/vehicle/?driver_id={id}&office_id={id} Headers(Authorization: Bearer {token})
 
##13. Vehicle view/update/delete
GET {url}:5000/api/vehicle/{id}  Headers(Authorization: Bearer {token})</br>

response:
<pre>
{
    "id": 1,
    "license_plate": "[license plate]",
    "name": "[Name]",
    "model": "[Model]",
    "year_of_manufacture": 'year',
    "driver": []
}
</pre>


PUT {url}:5000/api/vehicle/{id} Headers(Authorization: Bearer {token})<br />
<pre>
{
        "license_plate": ['license_plate'],<br />
        "name": ['name'],<br />
        "model": ['model'],<br />
        "year_of_manufacture": 'year_of_manufacture',<br />
        "office_id": 'id',<br />
        "driver_id": 'id',<br />
}
</pre>
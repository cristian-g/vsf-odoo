# RESTful API Odoo Module
## Installation
1. `cd C:\Program Files (x86)\Odoo 12.0\server\odoo\addons`
2. `git clone https://github.com/cristian-g/restful.git restful`
3. Update app list
4. Install module
## Class diagram
![Class diagram](docs/vuepress/public/class_diagram.png)
## Endpoints
This section contains an example of call to each endpoint. If you are testing it locally, your base url can be: `base_url = 'http://localhost:8069'`

Remember to `import requests, json`
### Public endpoints
They do not require to be authenticated.
```python
headers = {
    'content-type': 'application/x-www-form-urlencoded',
    'charset':'utf-8'
}
```
#### Get all categories
```python
req = requests.get(base_url+'/api/categories', data={}, headers=headers)
print (req.content)
```
#### Get all products of given category
```python
req = requests.get(base_url+'/api/category_products', data={
    'category_id': 4,
}, headers=headers)
print (req.content)
```
#### Get stock of given product
```python
req = requests.get(base_url+'/api/stock', data={
    'product_id': 16,
}, headers=headers)
print (req.content)
```
#### Log in (get access token)
```python
req = requests.get(base_url+'/api/auth/token', data={
    'login': 'example@example.com',
    'password': 'secret',
}, headers=headers)
print (req.content)
```
#### Sign up
```python
req = requests.post(base_url+'/api/signup', data={
    'email': 'example@example.com',
    'name': 'Cristian González',
    'password': 'secret',
}, headers=headers)
print (req.content)
```
### Private endpoints
They require an access token.
```python
content = json.loads(req.content.decode('utf-8'))
headers['access-token'] = content.get('access_token') # add the access token to the headers
```
#### Get user profile
```python
req = requests.get(base_url+'/api/profile/', headers=headers,
                   data={})
print(req.content)
```
#### Edit user profile
```python
req = requests.patch(base_url+'/api/edit_profile', data={
    'name': 'Cristian González',
    'email': 'example@example.com',
    'phone': '+34434391',
    'company_name': 'My company',
    'nif': 'ES12345678Z',
    'street': 'My street name',
    'city': 'My city name',
    'zip': 40120,
    'state_id': 434,
}, headers=headers)
print (req.content)
```
#### Change password
```python
req = requests.patch(base_url+'/api/change_password', data={
    'password': 'secret',
}, headers=headers)
print (req.content)
```
#### Get shopping cart
```python
req = requests.get(base_url+'/api/cart/', headers=headers,
                   data={})
print(req.content)
```
#### Edit a shopping cart quantity
```python
req = requests.patch(base_url+'/api/edit_quantity', data={
    'line_id': 14,
    'quantity': 0.0,
}, headers=headers)
print (req.content)
```
Note: it can return Unauthorized code.
#### Remove a shopping cart line
```python
req = requests.delete(base_url+'/api/remove_line', data={
    'line_id': 16,
}, headers=headers)
print (req.content)
```
Note: it can return Unauthorized code.
#### Add line to shopping cart
```python
req = requests.post(base_url+'/api/add_to_cart', data={
    'product_id': 6,
    'quantity': 11.0,
}, headers=headers)
print (req.content)
```
#### Set user shipping address
```python
req = requests.patch(base_url+'/api/set_shipping', data={
}, headers=headers)
print (req.content)
```
#### Get completed orders
```python
req = requests.get(
    base_url+'/api/orders/',
    headers=headers,
    data={}
)
print(req.content)
```

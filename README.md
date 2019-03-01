# RESTful API Odoo Module
## Installation
1. `cd C:\Program Files (x86)\Odoo 12.0\server\odoo\addons`
2. `git clone https://github.com/cristian-g/restful.git restful`
3. Update app list
4. Install module
## Endpoints
This section contains an example of call to each endpoint. If you are testing it locally, your base url can be: `base_url = 'http://localhost:8069'`

Remember to `import requests, json`
### Public endpoints
They do not require to be authenticated.
`
headers = {
    'content-type': 'application/x-www-form-urlencoded',
    'charset':'utf-8'
}
`
### Private endpoints
They require a token.
`
`


`
`
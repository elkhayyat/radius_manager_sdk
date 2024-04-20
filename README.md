# RADIUS MANAGER SDK

## Introduction

This is a Python SDK for Radius Manager API. It is a simple and easy to use SDK that allows you to interact with Radius
Manager API. It is a wrapper around the Radius Manager API that allows you to interact with the API using Python.

## Installation

1. Clone this repository.
2. Install the requirements using the following command:

```bash
pip install -r requirements.txt
```

3. Import the SDK in your Python script using the following command:

```python
from radius_manager_sdk.api import RMClient
```

4. First You need to enable API in Radius Manager. To enable API, you need to edit the config.php file located in the
   /var/www/html/radiusmanager directory. Edit the following lines to the config.php file:

```php
$API_ENABLED = 1;
$API_USERNAME = 'your_api_key';
$API_PASSWORD = 'your_api_password';
```

5Create an instance of the RMClient class using the following command:

```python
client = RMClient(api_url='http://localhost', api_username='your_api_key', api_password='your_api_password')
```

## Usage

1. Create new user:

```python
user = client.create_user(username='test_user', password='test_password')
print(user)
```

2. Get user by username:

```python
user = client.get_user(username='test_user')
print(user)
```

3. Get all service plans:

```python
service_plans = client.get_all_service_plans()
print(service_plans)
```

4. Get specific service plan:

```python
service_plan = client.get_service_plan(service_plan_id=1)
print(service_plan)
```

## TODO:

- [ ] Test More API Endpoints.
- [ ] Complete documentation.

## License

```angular2html
This project is licensed under the MIT License - see the LICENSE file for details
```
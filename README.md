# QuickPay

**Overview:** This QuickPay is a FastAPI application for micro-payments services (create users, make deposits, make transfers).

## Design Overview
The systems is organized into feature-based modules, with user managagement and transaction management.

The implementation separates into following layers: 
- **API layer**: defines FastAPI endpoints and handles HTTP requests and response
- **Validation layer**: validates the user inputs based on system requirements
- **Service layer**: the core business logic
- **Repository layer**: handles data CRUD by sqlite
- **Schema layer**: defines request and response data models with Pydantic

## Database schema
For the database schema, I have 3 main tables, you can see more details in `app/storage/repository.py`. Transaction ids are auto incremented, while user ids are supplied by the client as unique strings and stored as the primary key:
- `users` table: `uid` as key, `legal_name`, `email`, `age`, `balance`
- `deposits` table: `tid` as prikey, `amount`, `user_id`, `timestamp`
- `transfers` table: `tid` as primary key, `amount`, `sender_id`, `receiver_id`, `timestamp`

## Setup

1. Make sure Python is available in your environment, then install requirements:

```bash
python -m pip install -r requirements.txt
```

2. Start the server with Uvicorn (make sure that local port 8000 is available):

```bash
uvicorn app.main:app --host 127.0.0.1 --port 8000
```

- The SQLite database file `quickpay.db` is created automatically on application startup at the root folder.

## API usage

Below are instructions to run the API endpoints with sample payloads based on system requirements.

### Create user

`POST /users/create`

Request:

```bash
curl -s -X POST http://127.0.0.1:8000/users/create \
    -H "Content-Type: application/json" \
    -d '{"user_id":"user-1","legal_name":"Gia Lam","email":"gtlam@mun.ca","age":24}'
```

Expected: HTTP `201` with JSON including `uid`, `legal_name`, `email`, `age`, and `balance` (0.0).

If the age is < 18, the response is HTTP `400` with JSON:

```json
{ "detail": "ERR_AGE_RESTRICTED" }
```

If the email is invalid, the response is HTTP `400` with JSON:

```json
{ "detail": "ERR_INVALID_EMAIL" }
```

If the `user_id` already exists, the response is HTTP `400` with JSON:

```json
{ "detail": "ERR_DUPLICATE_USER_ID" }
```

### Deposit

`POST /transactions/deposit`

First, make sure at least one user exists and you know their `uid`. In the sample below, I assume the `uid` is `"user-1"`.

Request:

```bash
curl -s -X POST http://127.0.0.1:8000/transactions/deposit \
    -H "Content-Type: application/json" \
    -d '{"amount":100.0,"user_id":"user-1"}' -i
```

Expected: HTTP `201` and JSON with `tid`, `amount`, `user_id`, and `timestamp`. The user's `balance` increases by `100.0`.

If the deposit amount is < 5 or > 5000, the response is HTTP `400` with JSON:

```json
{ "detail": "ERR_DEPOSIT_LIMIT" }
```

If the `user_id` does not exist, the response is HTTP `404` with JSON:

```json
{ "detail": "ERR_USER_NOT_FOUND" }
```

### Transfer

`POST /transactions/transfer`

Make sure at least two users exist and you know both `uid`. In the sample below, I assume sender's is `"user-1"` and receiver's is `"user-2"`.

Request:

```bash
curl -s -X POST http://127.0.0.1:8000/transactions/transfer \
    -H "Content-Type: application/json" \
    -d '{"amount":50.0,"sender_id":"user-1","receiver_id":"user-2"}' -i
```

Expected: HTTP `201` and JSON with `tid`, `amount`, `sender_id`, `receiver_id`, and `timestamp`.

Sender's balance is debited by `amount + 1% fee`, and receiver's balance is credited by `amount`.

If the sender balance is insufficient, the response is HTTP `400` with JSON:

```json
{ "detail": "ERR_INSUFFICIENT_FUNDS" }
```

If either user does not exist, the response is HTTP `404` with JSON:

```json
{ "detail": "ERR_USER_NOT_FOUND" }
```

If `amount` is `<= 0`, the response is HTTP `400` with JSON:

```json
{ "detail": "ERR_INVALID_TRANSFER_AMOUNT" }
```

## Supporting endpoints

### List users

`GET /users/`

Request:

```bash
curl -s http://127.0.0.1:8000/users/
```

Expected: HTTP `200` with a JSON array of users.

### User balance

`GET /users/{user_id}/balance`

Request:

```bash
curl -s http://127.0.0.1:8000/users/user-1/balance
```

Expected: HTTP `200` with JSON including `uid` and `balance`.

### List deposits

`GET /transactions/deposits`

Request:

```bash
curl -s http://127.0.0.1:8000/transactions/deposits
```

Expected: HTTP `200` with a JSON array of deposit records.

### List transfers

`GET /transactions/transfers`

Request:

```bash
curl -s http://127.0.0.1:8000/transactions/transfers
```

Expected: HTTP `200` with a JSON array of transfer records.

## Black box testing

### TC-01 — SR 1.2
```bash
curl -i -X POST http://127.0.0.1:8000/users/create \
  -H "Content-Type: application/json" \
  -d '{"user_id":"U001","legal_name":"Gia Lam","email":"gtlam@mun.ca","age":17}'
```

### TC-02 — SR 1.2
```bash
curl -i -X POST http://127.0.0.1:8000/users/create \
  -H "Content-Type: application/json" \
  -d '{"user_id":"U002","legal_name":"Gia Lam","email":"gtlam@mun.ca","age":18}'
```

### TC-03 — SR 1.2
```bash
curl -i -X POST http://127.0.0.1:8000/users/create \
  -H "Content-Type: application/json" \
  -d '{"user_id":"U003","legal_name":"Gia Lam","email":"gtlam@mun.ca","age":19}'
```

### TC-04 — SR 1.3
```bash
curl -i -X POST http://127.0.0.1:8000/users/create \
  -H "Content-Type: application/json" \
  -d '{"user_id":"U004","legal_name":"Gia Lam","email":"gtlam@mun.ca","age":24}'
```

### TC-05 — SR 1.3
```bash
curl -i -X POST http://127.0.0.1:8000/users/create \
  -H "Content-Type: application/json" \
  -d '{"user_id":"U005","legal_name":"Gia Lam","email":"gtlammun.ca","age":24}'
```

### TC-06 — SR 1.3
```bash
curl -i -X POST http://127.0.0.1:8000/users/create \
  -H "Content-Type: application/json" \
  -d '{"user_id":"U006","legal_name":"Gia Lam","email":"gt-lam@@mun.ca","age":24}'
```
### TC-07 — SR 1.3
```bash
curl -i -X POST http://127.0.0.1:8000/users/create \
  -H "Content-Type: application/json" \
  -d '{"user_id":"U007","legal_name":"Gia Lam","email":"gtlam@munca","age":24}'
```
### TC-08 — SR 2.1
```bash
curl -i -X POST http://127.0.0.1:8000/transactions/deposit \
  -H "Content-Type: application/json" \
  -d '{"amount":4.99,"user_id":"U002"}'
```
### TC-09 — SR 2.1
```bash
curl -i -X POST http://127.0.0.1:8000/transactions/deposit \
  -H "Content-Type: application/json" \
  -d '{"amount":5.00,"user_id":"U002"}'
```
### TC-10 — SR 2.1
```bash
curl -i -X POST http://127.0.0.1:8000/transactions/deposit \
  -H "Content-Type: application/json" \
  -d '{"amount":5.01,"user_id":"U002"}'
```
### TC-11 — SR 2.1
```bash
curl -i -X POST http://127.0.0.1:8000/transactions/deposit \
  -H "Content-Type: application/json" \
  -d '{"amount":4999.99,"user_id":"U002"}'
```

### TC-12 — SR 2.1
```bash
curl -i -X POST http://127.0.0.1:8000/transactions/deposit \
  -H "Content-Type: application/json" \
  -d '{"amount":5000.00,"user_id":"U002"}'
```

### TC-13 — SR 2.1
```bash
curl -i -X POST http://127.0.0.1:8000/transactions/deposit \
  -H "Content-Type: application/json" \
  -d '{"amount":5000.01,"user_id":"U002"}'
```

## White box testing
The project uses `pytest` for automated testing `Coverage.py` for statement and branch coverage. 
All testing files are placed in tests folder. Tests are divided into 3 layers: routes, services, and validators of 2 modules including users and transactions. 

* Validator test call validation functions directly and check both valid and invalid inputs
* Service tests call business-logic functions directly and verify balance updates, duplicate detection, missing-user handling, and transfer fee behavior
* Route tests use FastAPI `TestClient` to send in-process HTTP requests to the API and verify status codes and JSON responses

All of them shared fixtures in `conftest.py` which isolate each test case. Each test have a fresh temporary SQLite DB so test data does not lead between tests. Helper fixtures also generate valid users and seed balances. 

To run all the tests: 
```bash
python -m pytest -q
```

To run the test while collecting line and branch coverage:
```bash
python -m coverage run --branch -m pytest -q
```

To get the coverage summary and missing lines: 
```bash
python -m coverage report -m
```



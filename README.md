# QuickPay

**Overview:** This QuickPay is a FastAPI application for micro-payments services (create users, make deposits, make transfers).

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
    -d '{"legal_name":"Gia Lam","email":"gtlam@mun.ca","age":24}'
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

### Deposit

`POST /transactions/deposit`

First, make sure at least one user exists and you know their `uid`. In the sample below, I assume the `uid` is `1`.

Request:

```bash
curl -s -X POST http://127.0.0.1:8000/transactions/deposit \
    -H "Content-Type: application/json" \
    -d '{"amount":100.0,"user_id":1}' -i
```

Expected: HTTP `201` and JSON with `tid`, `amount`, `user_id`, and `timestamp`. The user's `balance` increases by `100.0`.

If the deposit amount is < 5 or > 5000, the response is HTTP `400` with JSON:

```json
{ "detail": "ERR_DEPOSIT_LIMIT" }
```

### Transfer

`POST /transactions/transfer`

Make sure at least two users exist and you know both `uid`. In the sample below, I assume sender's is `1` and receiver's is `2`.

Request:

```bash
curl -s -X POST http://127.0.0.1:8000/transactions/transfer \
    -H "Content-Type: application/json" \
    -d '{"amount":50.0,"sender_id":1,"receiver_id":2}' -i
```

Expected: HTTP `201` and JSON with `tid`, `amount`, `sender_id`, `receiver_id`, and `timestamp`.

Sender's balance is debited by `amount + 1% fee`, and receiver's balance is credited by `amount`.

If the sender balance is insufficient, the response is HTTP `400` with JSON:

```json
{ "detail": "ERR_INSUFFICIENT_FUNDS" }
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
curl -s http://127.0.0.1:8000/users/1/balance
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


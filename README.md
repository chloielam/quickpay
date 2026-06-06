**QuickPay**

- **Overview:** This QuickPay is a FastAPI application for micro-payments servicees (create users, make deposits, make transfer)

 **Setup**
 - First, make sure that you have python in your environment, then install requirements: 

 ```bash
python -m pip install -r requirements.txt
```

- Then you can start the server with Uvicorn (make sure the port 8000 of your local machine is available): 

```bash
uvicorn app.main:app --host 127.0.0.1 --port 8000
```

- The SQLite database file `quickpay.db` is created automatically on application startup at the root folder 

- Below are instruction to run the API endpoints with sample payloads based on our system requirements: 

- **Create user**: `POST /users/create` — body: `legal_name`, `email`, `age`. Returns `201` and a user object including `uid` and `balance`

Sameple payloads:

Request:

```bash
curl -s -X POST http://127.0.0.1:8000/users/create \
    -H "Content-Type: application/json" \
    -d '{"legal_name":"Gia Lam","email":"gtlam@mun.ca","age":24}'
```

Expected: HTTP `201` with JSON including `uid`, `legal_name`, `email`, `age`, and `balance` (0.0)


If the age is < 18, it would be HTTP `400` with JSON `{ "detail": "ERR_AGE_RESTRICTED" }`
If the email does not contain exactly one @ character and at least one . character after the @, it would be HTTP `400` with JSON `{ "detail": "ERR_INVALID_EMAIL" }`

- **Deposit**

First, make sure that there is at least 1 user was created and you know her/his `uid`. In the sample below assume the `uid` is 1

Request:

```bash
curl -s -X POST http://127.0.0.1:8000/transactions/deposit \
    -H "Content-Type: application/json" \
    -d '{"amount":100.0,"user_id":1}' -i
```

Expected: HTTP `201` and JSON with `tid`, `amount`, `user_id`, and `timestamp`. The user's `balance` increases by `100.0`.

If the deposit amount is < 5 or > 5000, it would be HTTP `400` with JSON `{ "detail": "ERR_DEPOSIT_LIMIT" }`


- **Transfer**
For this one, make sure that there is at least 2 user was created and you know her/his `uid`. In the sample below assume the `uid` of the sender is 1 and the receiver is 2. 

```bash
curl -s -X POST http://127.0.0.1:8000/transactions/transfer \
    -H "Content-Type: application/json" \
    -d '{"amount":50.0,"sender_id":1,"receiver_id":2}' -i
```

Expected: HTTP `201` and JSON with `tid`, `amount`, `sender_id`, `receiver_id`, `timestamp`.
Sender's balance will be debited by `amount + 1% fee` and receiver credited by `amount`.

if the sender balance < `amount + 1% fee`, it would be HTTP `400` with JSON `{ "detail": "ERR_INSUFFICIENT_FUNDS" }`


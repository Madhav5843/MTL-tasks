This looks like a **Push Notification Token Investigation** for multiple clients where some device tokens have expired and new tokens may have been generated.

## What the data is showing

### 1. Expired Tokens

For Client ID `4832043502`, you listed these tokens as expired:

```text
629448a5c9fd6318da71d2ad33428a379178ae5d65c84b8935e001923c6220ce
2d8b2d5c39bb6ff647e22c70a4e554dc55af362412d570bae9c1aaebc28cb067
e2116ed6d25dc9d00d0927c2f665114f1d103172d7f8e503cc7b7a5c862f4e0e
...
```

This usually means:

* Mobile app reinstall
* User logged out/login
* FCM/APNS rotated the token
* Device no longer uses that token

***

### 2. Total List of Tokens

You then pulled all tokens from:

```sql
select *
from t_push_tokens
where client_id = 4832043502
order by id desc;
```

This shows every token ever registered for that client.

***

### 3. New Token Found

I noticed this entry:

```text
fNcDXADwxEMFtuj8_jKunb:APA91bGPL3stUA2UGrhZOvz7hLhGJUs4aQ1wso5cZMyr4hLNOSqUi2mF0Gl1V7SVUAVKnlV7vft6JMscL4fue_XenC6LonigkuxIp0YOyAvJ2TfW0tyo05c
```

You marked it as:

```text
New token
```

This strongly suggests the user's application has refreshed its push token and registered a new token with the backend.

***

## Analysis for Client 4832043502

Comparing the lists:

### Expired Tokens Found Again in Database

These expired tokens still exist in `t_push_tokens`:

```text
629448a5...
2d8b2d5...
e2116ed...
814b3ee...
c68c1de...
339a10f...
a636f62...
4ebf901...
a7b2c71...
ce06dab...
```

This means:

✅ Tokens are stored in DB

❌ But FCM/APNS is reporting them as expired

***

## What should be checked

### Check latest token

```sql
select *
from t_push_tokens
where client_id = 4832043502
order by id desc;
```

Verify:

* Most recent record
* Active flag
* Created date
* Updated date

***

### Check if new token exists

```sql
select *
from t_push_tokens
where push_token like 'fNcDXADwxEMFtuj8_jKunb%';
```

Expected:

```text
Found
```

***

### Check which token notification service is using

If the notification service is still attempting:

```text
629448a5...
2d8b2d5...
```

instead of

```text
fNcDXAD...
```

then notifications will fail.

***

## About this query

```sql
select *
from t_push_tokens
where push_token='c962b05b66035d65acb2003ac19d0cb823416363cc777ac37b52b75069f76112';
```

This token belongs to:

```text
Client ID 7317430158
```

based on the data you pasted.

Purpose of this query:

```sql
select *
from t_push_tokens
where push_token='c962b05b66035d65acb2003ac19d0cb823416363cc777ac37b52b75069f76112';
```

is to find:

* Client ID
* Registration date
* Device information
* Whether token is active
* Last updated date

If no rows are returned:

```text
Token not registered in DB
```

If rows are returned:

```text
Token exists in DB
```

Then compare it against notification logs.

***

## L2 Support Investigation Notes

When you get a "Token Expired" issue:

### Step 1

Identify failed token from logs.

### Step 2

Search in DB:

```sql
select *
from t_push_tokens
where push_token='<failed_token>';
```

### Step 3

Get client:

```sql
select *
from t_push_tokens
where client_id='<client_id>'
order by id desc;
```

### Step 4

Check whether a newer token exists.

### Step 5

If newer token exists:

```text
Old Token -> Expired
New Token -> Active
```

### Step 6

Verify notification service is picking the latest token.

***

### Likely conclusion from your data

For client **4832043502**, multiple historical tokens have expired and there appears to be a **new FCM token (`fNcDXADwxEMFtuj8...`)** registered. The investigation should confirm whether notification delivery is using this latest token instead of the expired tokens stored in `t_push_tokens`.

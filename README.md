# pytinder
A makeshift implementation of API access to Tinder through Facebook using Python

#### Example Implementation
```python
from pytinder import Client
client = Client('facebook_email', 'facebook_password')
for tinder_user in client.recommendations():
    client.like(tinder_user.id)
```
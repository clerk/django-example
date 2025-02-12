Install dependencies:

```bash
pip install -r requirements.txt
```

Make sure the CLERK_SECRET_KEY [environment variable](https://clerk.com/docs/deployments/clerk-environment-variables#clerk-publishable-and-secret-keys) is set, ie:

```bash
export CLERK_SECRET_KEY=my_secret_key
```

Start the server:

```bash
python3 manage.py runserver
```

Set `CLERK_AUTHORIZED_PARTIES` in clerkproject/settings.py:
```python
# default server location for Clerk React App
CLERK_AUTHORIZED_PARTIES = ['http://localhost:5173', ]
```

From a Clerk frontend, use the `useSession` hook to retrieve the getToken() function:

```js
const session = useSession();
const getToken = session?.session?.getToken
```

Then, request the python server:

```js
if (getToken) {
    // get the userId or None if the token is invalid
    const res = await fetch("http://localhost:8000/clerk_jwt", {
        headers: {
            "Authorization": `Bearer ${await getToken()}`
        }
    })
    console.log(await res.json()) // {userId: 'the_user_id_or_null'}

    // get gated data or a 401 Unauthorized if the token is not valid
    const res = await fetch("http://localhost:8000/gated_data", {
        headers: {
            "Authorization": `Bearer ${await getToken()}`
        }
    })
    if (res.status === 401) {
        // token was invalid
    } else {
        console.log(await res.json()) // {foo: "bar"}
    }
}
```

If you're using Django REST Framework, you can create a permission that can be used to guard data in a ViewSet.

```py
from rest_framework.permissions import BasePermission

class ClerkAuthenticated(BasePermission):
    """
    Allows access only to authenticated users.
    """

    def has_permission(self, request, view):
        return request.verified_clerk_token is not None
```

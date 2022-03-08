Run `python3 manage.py runserver`

From a Clerk frontend, use the `useSession` hook to retrieve the getToken() function:

```
const { getToken } = useSession();
```

Then, request the python server with:

```
await fetch("http://localhost:8000/clerk_jwt", {
    headers: {
        "Authorization": `Bearer ${await getToken()}`
    }
})
```

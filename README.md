1. Ensure `CLERK_API_SECRET_KEY` and `CLERK_AUTHORIZED_PARTIES` is set in your environment variables. `CLERK_AUTHORIZED_PARTIES` is a comma-separated list of allowed parties for example `http://localhost:5173`

2. Install dependencies with 
```commandline
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. Run `python3 manage.py runserver`

4. From a Clerk frontend, use the `useSession` hook to retrieve the getToken() function:

```
const { getToken } = useSession();
```

5. Then, request the python server with:

```
await fetch("http://localhost:8000/clerk_jwt", {
    headers: {
        "Authorization": `Bearer ${await getToken()}`
    }
})
```


## Important Note:
This project is not optimized for production and do not address all best practices that should be configured in a production app (CORS, 401 error handling and HTTPs for example).
These projects serve as a design template and should be given appropriate consideration before being used in production.
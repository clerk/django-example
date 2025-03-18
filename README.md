# Django Clerk Auth Example

A demonstration of using Clerk JWT authentication with Django. This example shows how to integrate Clerk's user authentication with a Django DRF backend API.

## Installation 

```commandline
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Configuration

Set the required environment variables:

```bash
$ export CLERK_API_SECRET_KEY=your_secret_key

# Set authorized parties (comma-separated list of allowed origins)
$ export CLERK_AUTHORIZED_PARTIES=http://localhost:5173
```

## Running 

```commandline
python manage.py runserver
```

The server will be running at `http://localhost:8000`.

## Frontend Integration

From a Clerk React frontend:

```javascript
import { useAuth } from '@clerk/clerk-react';

function ApiExample() {
  const { getToken } = useAuth();
  
  const fetchData = async () => {
    if (getToken) {
      // Get the userId or null if the token is invalid
      let res = await fetch("http://localhost:8000/clerk_jwt", {
          headers: {
              "Authorization": `Bearer ${await getToken()}`
          }
      });
      console.log(await res.json()); // {userId: 'the_user_id_or_null'}

      // Get gated data or a 401 Unauthorized if the token is not valid
      res = await fetch("http://localhost:8000/gated_data", {
          headers: {
              "Authorization": `Bearer ${await getToken()}`
          }
      });
      if (res.ok) {
          console.log(await res.json()); // {foo: "bar"}
      } else {
          // Token was invalid
      }
    }
  };
  
  return <button onClick={fetchData}>Fetch Data</button>;
}
```

## API Reference

Available endpoints:

- `GET /clerk_jwt` - Returns the authenticated user ID
- `GET /gated_data` - Returns protected data (requires authentication)


## ⚠️ Production Warning

This project is not optimized for production and does not address all best practices that should be configured in a production app. It serves as a design template and should be given appropriate consideration before being used in production.

Issues to address for production use:
- CORS configuration is specific to development environments
- No HTTPS enforcement
- Minimal error handling (especially 401 errors)
- Using development server settings

For production deployment:
1. Configure proper CORS settings for your specific domains
2. Enforce HTTPS for all API communication
3. Implement comprehensive error handling
4. Use a production-grade web server instead of the built-in development server
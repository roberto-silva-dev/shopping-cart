
# Shopping Cart API
Shopping cart system with a promotional campaign and differentiated pricing based on user type.

This is a Django project configured with SQLite3 as the default database. Follow the steps below to clone, set up, and run the project.

If you need any help, don't hesitate to reach out to me. 

Check my [contacts here](https://robertosilva.dev/)


#### This project is deployed at [https://shopping-cart.portfolio.robertosilva.dev](https://shopping-cart.portfolio.robertosilva.dev)

---

## 🛠️ Prerequisites

- Python 3 or higher
- pip (Python package manager)
- Git
- Postman (optional, to test the API)

---

## 🚀 How to set up the project

### 1. Clone the Repository
```bash
git clone https://github.com/roberto-silva-dev/shopping-cart.git
cd shopping-cart
```

### 2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # Linux/MacOS
venv\Scripts\activate   # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure the database and static files
The project uses SQLite3 by default. No external database setup is required. Just run the migrations:

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic
```

### 5. Create initial users and products
Run the script to create the default users and products:
```bash
python manage.py runscript setup
```

#### Default user credentials:
- **Administrator**
  - **Username:** `admin`
  - **Password:** `admin`
- **Common user**
  - **Username:** `common`
  - **Password:** `Common@2024*`
- **VIP user**
  - **Username:** `vip`
  - **Password:** `Vip@2024*`

### 6. Run the local server
```bash
python manage.py runserver
```

The server will be available at [http://127.0.0.1:8000](http://127.0.0.1:8000).

---

## 🌐 Testing the API

The project includes a Postman collection to simplify API testing.

### With Postman
- Locate the [`docs/postman_collection.json`](docs/postman_collection.json) and [`docs/postman_environment.json`](docs/postman_environment.json) file in the repository.
- Import it into Postman by following [this guide](https://learning.postman.com/docs/getting-started/importing-and-exporting-data/#importing-postman-data).

### With other clients
- If you desire to test the API using other client, you must set up:
- - **Base URL**: `http://127.0.0.1:8000`
- - **X-CSRFToken**: `<csrf_token>` - the token will be set on cookies when you call the `/auth/csrf` endpoint - Just for http methods that aren't GET
---

## 📚 API Endpoints
You'll have access to all the configured API endpoints:

| Method | Endpoint           | Description                              |
|--------|--------------------|------------------------------------------|
| GET    | `/cart`            | List all items on cart besides the total |
| POST   | `/cart/items`      | Add or upgrade an item to cart           |
| GET    | `/cart/items/<id>` | Get details from a specific item at cart |
| PATCH  | `/cart/items/<id>` | Update the item at cart                  |
| DELETE | `/cart/items/<id>` | Remove a specific item from cart         |
| GET    | `/auth/csrf`       | Set the CSRF token on cookies            |
| POST   | `/auth/login`      | Perform login                            |
| GET    | `/auth/profile`    | Get the profile's data                   |
| POST   | `/auth/logout`     | Perform logout                           |

More details about each endpoints are available in the [`/docs/swagger`](http://127.0.0.1:8000/docs/swagger) or [`/docs/redoc`](http://127.0.0.1:8000/docs/redoc) endpoints.



# Architecture and design summary

## Framework
- **Backend Framework:** Django with Django REST Framework (DRF) for handling RESTful public endpoints.

## User roles & cart handling
- **Common user:** Default for non-logged users or logged users without VIP status.
- **VIP user:** Logged users with VIP status, identified by `user_type` field in the user model.
- **Anonymous users:** Can add items to the cart, just like logged-in users, but their cart is temporary and not linked to any account.
- **Logged-in users:** Have a persistent cart tied to their account.

### Cart merging on login
When an anonymous user logs in, their cart (from the session) is merged with their existing account cart, if any. This ensures a seamless experience where no items are lost upon login.

## Promotions
- **Common users:** The "Get 3 Pay 2" promotion is available.
- **VIP users:** "Get 3 Pay 2" promotion or a 15% discount is available, but not both. The system picks the best option for the user based on the higher discount.

## Access control
- All endpoints are public. Role-based logic (VIP vs. Common) is applied based on authentication and user status.

## Key design decisions
1. **Scalability:** 
- DRF’s modular architecture allows for easy extension of the system to support additional user roles or new features.
- The apps are separated based on resource types and responsibilities, making it easier to manage and scale the system as the project grows.
2. **User experience:**
 - The role-based categorization ensures an intuitive user flow, with seamless transitions between "Common" and "VIP" functionalities depending on login status.
3. **Security:**
- The system uses CSRF tokens to protect against cross-site request forgery attacks and CORS headers to allow cross-origin requests.
4. **Maintainability:**
- The use of DRF viewsets and serializers promotes code reuse and simplifies maintenance as the system grows.
5. **Documentation:**
- The functions and classes are well-documented, making it easy to understand and maintain the codebase.
- The API documentation is generated using the [Swagger UI](https://github.com/swagger-api/swagger-ui) and [ReDoc](https://github.com/Rebilly/ReDoc) tools. Usefully for testing and development.

## Summary
This architecture provides a flexible, extensible structure that supports both anonymous and logged-in users while ensuring that cart merging and promotions are handled seamlessly. The design maintains simplicity and scalability as the system grows.


## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## 🤝 Contributing

Contributions are welcome! Feel free to open issues and pull requests.

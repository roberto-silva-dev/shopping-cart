
# Shopping Cart API
Shopping cart system with a promotional campaign and differentiated pricing based on user type.

This is a Django project configured with SQLite3 as the default database. Follow the steps below to clone, set up, and run the project.

If you need any help, don't hesitate to reach out to me. 

Check my [contacts here](https://robertosilva.dev/)


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

### 4. Configure the database
The project uses SQLite3 by default. No external database setup is required. Just run the migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create initial users
Run the script to create the default users:
```bash
python manage.py runscript scripts/create_initial_users
```

#### Default user credentials:
- **Administrator**
  - **Username:** `admin`
  - **Password:** `admin123`
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

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## 🤝 Contributing

Contributions are welcome! Feel free to open issues and pull requests.

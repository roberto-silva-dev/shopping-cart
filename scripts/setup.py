from users.models import CustomUser
from products.models import Product


def run():
    print("Running setup script...")

    if not CustomUser.objects.filter(username="admin").exists():
        CustomUser.objects.create_superuser("admin", "admin@example.com", "admin")
        print("Superuser 'admin' created.")
    else:
        print("Superuser 'admin' already exists.")

    for username, user_type, email, password in [
        ("common", "common", "common@email.com", "Common@2024*"),
        ("vip", "vip", "vip@email.com", "Vip@2024*"),
    ]:
        if not CustomUser.objects.filter(username=username).exists():
            CustomUser.objects.create_user(username, email, password, user_type=user_type)
            print(f"User '{username}' created.")
        else:
            print(f"User '{username}' already exists.")

    for name, price in [
        ("T-shirt", 35.99),
        ("Jeans", 65.50),
        ("Dress", 80.75),
    ]:
        if not Product.objects.filter(name=name).exists():
            Product.objects.create(name=name, price=price)
            print(f"Product '{name}' created.")
        else:
            print(f"Product '{name}' already exists.")

    print("Setup script completed.")

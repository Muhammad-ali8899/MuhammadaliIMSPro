class Product:
    def __init__(self, product_id, name, category, price, stock_quantity):
        self.product_id = product_id
        self.name = name
        self.category = category
        self.price = price
        self.stock_quantity = stock_quantity

    def __repr__(self):
        return f"Product({self.product_id}, {self.name}, {self.category}, {self.price}, {self.stock_quantity})"


class Inventory:
    def __init__(self):
        self.products = {}
    
    def add_product(self, product):
        self.products[product.product_id] = product

    def update_product(self, product_id, **kwargs):
        if product_id in self.products:
            product = self.products[product_id]
            for key, value in kwargs.items():
                setattr(product, key, value)
        else:
            raise ValueError("Product not found.")

    def delete_product(self, product_id):
        if product_id in self.products:
            del self.products[product_id]
        else:
            raise ValueError("Product not found.")

    def view_products(self):
        return self.products.values()

    def search_product(self, name=None, category=None):
        results = []
        for product in self.products.values():
            if (name and name.lower() in product.name.lower()) or (category and category.lower() == product.category.lower()):
                results.append(product)
        return results

    def adjust_stock(self, product_id, quantity):
        if product_id in self.products:
            product = self.products[product_id]
            product.stock_quantity += quantity
            if product.stock_quantity < 10:  # Low stock threshold
                print(f"Low stock alert for {product.name}. Consider restocking.")
        else:
            raise ValueError("Product not found.")


class User:
    def __init__(self, username, password, role):
        self.username = username
        self.password = password
        self.role = role


class InventorySystem:
    def __init__(self):
        self.inventory = Inventory()
        self.users = {}
        self.logged_in_user = None

    def create_user(self, username, password, role):
        if username not in self.users:
            self.users[username] = User(username, password, role)
        else:
            raise ValueError("User already exists.")

    def login(self, username, password):
        user = self.users.get(username)
        if user and user.password == password:
            self.logged_in_user = user
            print(f"Welcome, {username}!")
        else:
            raise ValueError("Invalid username or password.")

    def logout(self):
        self.logged_in_user = None
        print("Logged out successfully.")

    def admin_actions(self):
        if self.logged_in_user.role != "Admin":
            raise PermissionError("You do not have permission to perform this action.")
        
        while True:
            print("\nAdmin Menu:")
            print("1. Add Product")
            print("2. Update Product")
            print("3. Delete Product")
            print("4. View All Products")
            print("5. Logout")
            choice = input("Choose an action: ")
            
            if choice == '1':
                self.add_product()
            elif choice == '2':
                self.update_product()
            elif choice == '3':
                self.delete_product()
            elif choice == '4':
                self.view_products()
            elif choice == '5':
                self.logout()
                break
            else:
                print("Invalid choice. Try again.")

    def user_actions(self):
        while True:
            print("\nUser Menu:")
            print("1. View All Products")
            print("2. Search Product")
            print("3. Logout")
            choice = input("Choose an action: ")
            
            if choice == '1':
                self.view_products()
            elif choice == '2':
                self.search_product()
            elif choice == '3':
                self.logout()
                break
            else:
                print("Invalid choice. Try again.")

    def add_product(self):
        product_id = input("Enter Product ID: ")
        name = input("Enter Product Name: ")
        category = input("Enter Product Category: ")
        price = float(input("Enter Product Price: "))
        stock_quantity = int(input("Enter Stock Quantity: "))
        
        product = Product(product_id, name, category, price, stock_quantity)
        self.inventory.add_product(product)
        print(f"Product {name} added successfully.")

    def update_product(self):
        product_id = input("Enter Product ID to update: ")
        try:
            price = float(input("Enter new Product Price (leave blank for no change): ") or "NaN")
            stock_quantity = int(input("Enter new Stock Quantity (leave blank for no change): ") or "NaN")
            
            updates = {}
            if not isnan(price):
                updates['price'] = price
            if not isnan(stock_quantity):
                updates['stock_quantity'] = stock_quantity
            
            self.inventory.update_product(product_id, **updates)
            print("Product updated successfully.")
        except ValueError as e:
            print(e)

    def delete_product(self):
        product_id = input("Enter Product ID to delete: ")
        try:
            self.inventory.delete_product(product_id)
            print("Product deleted successfully.")
        except ValueError as e:
            print(e)

    def view_products(self):
        products = self.inventory.view_products()
        for product in products:
            print(product)

    def search_product(self):
        name = input("Enter Product Name to search (leave blank for category search): ")
        category = input("Enter Product Category to search (leave blank for name search): ")
        
        results = self.inventory.search_product(name=name, category=category)
        for product in results:
            print(product)


def main():
    ims = InventorySystem()
    ims.create_user("admin", "adminpass", "Admin")
    ims.create_user("user", "userpass", "User")

    while True:
        print("\nMain Menu:")
        print("1. Login as Admin")
        print("2. Login as User")
        print("3. Exit")
        choice = input("Choose an action: ")

        if choice == '1':
            username = input("Enter username: ")
            password = input("Enter password: ")
            try:
                ims.login(username, password)
                ims.admin_actions()
            except (ValueError, PermissionError) as e:
                print(e)
        elif choice == '2':
            username = input("Enter username: ")
            password = input("Enter password: ")
            try:
                ims.login(username, password)
                ims.user_actions()
            except ValueError as e:
                print(e)
        elif choice == '3':
            print("Exiting the system.")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()

from colorama import Cursor
from flask import Flask, render_template, request,url_for,redirect
import mysql.connector
import os
from pathlib import Path
from dotenv import load_dotenv
env_path = Path(__file__).parent / '.env'  
load_dotenv(dotenv_path=env_path)          
app = Flask(__name__)
db = mysql.connector.connect(
    host=os.getenv("DB_HOST", "localhost"),
    user=os.getenv("DB_USER", "root"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME", "angadimithra")
)
@app.route('/')
def home():
    return redirect('/login')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        sql="""INSERT INTO users(name,email,password)VALUES(%s,%s,%s)"""
        values=(name,email,password)
        cursor=db.cursor()
        cursor.execute(sql,values)
        db.commit()
        cursor.close()
        return redirect('/login')
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        return redirect(url_for('dashboard'))


    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


 
@app.route('/products', methods=['GET', 'POST'])
def products():
    cursor = db.cursor()

    if request.method == 'POST':
        product_name = request.form['product_name']
        price = request.form['price']
        quantity = request.form['quantity']
    
        cursor.execute(
            """
            INSERT INTO products
            (product_name, price, quantity)
            VALUES (%s, %s, %s)
            """,
            (product_name, price, quantity)
        )

        db.commit()
        cursor.close()

        return redirect('/products')

    cursor.execute(
        """
        SELECT *
        FROM products
        ORDER BY id DESC
        """
    )

    products = cursor.fetchall()
    cursor.close()

    return render_template(
        'products.html',
        products=products
    )
@app.route('/sales', methods=['GET', 'POST'])
def sales():

    cursor = db.cursor()

    if request.method == 'POST':

        product_id = request.form['product_id']
        quantity_sold = int(request.form['quantity_sold'])

        cursor.execute(
            "SELECT price, quantity FROM products WHERE id=%s",
            (product_id,)
        )

        product = cursor.fetchone()

        if product:

            price = product[0]
            current_stock = product[1]

            if quantity_sold > current_stock:
                cursor.close()
                return "Not enough stock available"

            total_amount = price * quantity_sold

            cursor.execute(
                """
                INSERT INTO sales
                (product_id, quantity_sold, total_amount, sale_date)
                VALUES (%s,%s,%s,CURDATE())
                """,
                (product_id, quantity_sold, total_amount)
            )

            new_stock = current_stock - quantity_sold

            cursor.execute(
                """
                UPDATE products
                SET quantity=%s
                WHERE id=%s
                """,
                (new_stock, product_id)
            )

            db.commit()

        cursor.close()

        return redirect('/sales')

    cursor.execute(
        """
        SELECT id,
               product_name,
               price,
               quantity
        FROM products
        """
    )

    products = cursor.fetchall()

    cursor.execute(
        """
        SELECT s.id,
               p.product_name,
               s.quantity_sold,
               p.price,
               s.total_amount,
               s.sale_date
        FROM sales s
        JOIN products p
        ON s.product_id = p.id
        ORDER BY s.id DESC
        """
    )

    sales_data = cursor.fetchall()

    cursor.execute(
        """
        SELECT SUM(total_amount)
        FROM sales
        WHERE sale_date = CURDATE()
        """
    )

    today_sales = cursor.fetchone()[0] or 0

    cursor.execute(
        """
        SELECT SUM(total_amount)
        FROM sales
        WHERE MONTH(sale_date)=MONTH(CURDATE())
        AND YEAR(sale_date)=YEAR(CURDATE())
        """
    )

    monthly_sales = cursor.fetchone()[0] or 0

    cursor.execute(
        """
        SELECT SUM(total_amount)
        FROM sales
        """
    )

    total_revenue = cursor.fetchone()[0] or 0

    cursor.execute(
        """
        SELECT p.product_name
        FROM sales s
        JOIN products p
        ON s.product_id = p.id
        GROUP BY p.product_name
        ORDER BY SUM(s.quantity_sold) DESC
        LIMIT 1
        """
    )

    top_product = cursor.fetchone()

    cursor.close()

    return render_template(
        'sales.html',
        products=products,
        sales=sales_data,
        today_sales=today_sales,
        monthly_sales=monthly_sales,
        total_revenue=total_revenue,
        top_product=top_product[0] if top_product else None
    )
if __name__ == '__main__':
    app.run(debug=True)
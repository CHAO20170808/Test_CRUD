
from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
from flask_cors import CORS  # 引入 CORS

#app = Flask(__name__)
app = Flask(__name__)
CORS(app)  # 啟用全局 CORS

# MySQL configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'demo'

mysql = MySQL(app)


# Create
@app.route('/create', methods=['POST'])
def create():
    data = request.json
    name = data['name']
    price = data['price']
    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO products (name, price) VALUES (%s, %s)", (name, price))
    mysql.connection.commit()
    return jsonify({"message": "Product created successfully!"})

# Read
@app.route('/read', methods=['GET'])
def read():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM products")
    rows = cursor.fetchall()
    return jsonify(rows)

# Update
@app.route('/update/<int:id>', methods=['PUT'])
def update(id):
    data = request.json
    name = data['name']
    price = data['price']
    cursor = mysql.connection.cursor()
    cursor.execute("UPDATE products SET name = %s, price = %s WHERE id = %s", (name, price, id))
    mysql.connection.commit()
    return jsonify({"message": "Product updated successfully!"})

# Delete
@app.route('/delete/<int:id>', methods=['DELETE'])
def delete(id):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM products WHERE id = %s", (id,))
    mysql.connection.commit()
    return jsonify({"message": "Product deleted successfully!"})

#if __name__ == '__main__':
 #   app.run(debug=True)

@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    app.run(debug=True)

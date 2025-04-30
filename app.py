

from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
from flask_cors import CORS  # 引入 CORS


import mohawk
from functools import wraps
import re


app = Flask(__name__)
CORS(app)  # 啟用全局 CORS

hawk_credentials = {
    '8577961': {'key': '3r45e4b8-9f3c-4a2d-8f1d-2f5b7c9a6e0d', 'algorithm': 'sha256'},
    # 更多憑證
}
# MySQL configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'demo'

mysql = MySQL(app)

def get_hawk_id_from_header(authorization_header):
    match = re.search(r'id="([^"]*)"', authorization_header)
    if match:
        return match.group(1)
    return None


def hawk_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        authorization_header = request.headers.get('Authorization')
        if not authorization_header:
            return jsonify({"error": "Authorization header is missing"}), 401

        hawk_id_from_header = get_hawk_id_from_header(authorization_header)
        if not hawk_id_from_header:
            return jsonify({"error": "Invalid Authorization header format"}), 400

        credentials = hawk_credentials.get(hawk_id_from_header)
        if not credentials:
            return jsonify({"error": "Invalid Hawk ID"}), 401

        print(f"request.method 的值: {request.method}")
        print(f"request.method 的類型: {type(request.method)}")
        print(f"request.url 的值: {request.url}")
        print(f"request.url 的類型: {type(request.url)}")

        try:
            hawk_test = mohawk.Receiver(
                credentials,
                request.url,
               'POST'
            )
            # str(request.method)
            print("簡化的 mohawk.Receiver 實例創建成功")
        except TypeError as e:
            print(f"創建簡化的 mohawk.Receiver 實例時發生 TypeError: {e}")
            raise

        try:
            # str(request.method),  # 顯式轉換為字串
            hawk = mohawk.Receiver(
                credentials,
                request.url,
                'POST' , # 直接使用字面值 'POST'
                content=request.get_data(),
                content_type=request.content_type
            )
         # 驗證成功，可以存取 hawk 的屬性，例如 hawk.id
            return func(*args, **kwargs)
        except Exception as e:
            if "hawk" in str(e).lower():
                return jsonify({"error": f"Hawk authentication failed: {str(e)}"}), 401
            else:
                return jsonify({"error": f"An error occurred: {str(e)}"}), 500
        #except mohawk.HawkAuthError as e:  # 直接從 mohawk 導入並使用
         #   return jsonify({"error": f"Hawk authentication failed: {str(e)}"}), 401
        #except Exception as e:
        #    return jsonify({"error": f"An error occurred: {str(e)}"}), 500
    return decorated_function




@app.route('/api/spcuser', methods=['POST'])
@hawk_required
def add_special_user():
    if request.content_type == 'application/json':
        data = request.get_json()
        account = data.get('帳號')
        user_level = data.get('使用者等級')
        is_active = data.get('是否激活', False)

        if not account or user_level is None:
            return jsonify({"error": "帳號和使用者等級是必填欄位"}), 400

        # ... (新增使用者的資料庫操作)
        return jsonify({"message": "特殊使用者新增成功!"}), 201
    else:
        return jsonify({"error": "Content-Type must be application/json"}), 415

@app.route('/api/spcuser', methods=['POST'])
@hawk_required
def add_special_user():
    print("進入 add_special_user 函數")
    if request.content_type == 'application/json':
        print("Content-Type 是 application/json")
        data = request.get_json()
        print(f"接收到的資料: {data}")
        account = data.get('帳號')
        user_level = data.get('使用者等級')
        is_active = data.get('是否激活', False)

        if not account or user_level is None:
            print("帳號或使用者等級是必填欄位")
            return jsonify({"error": "帳號和使用者等級是必填欄位"}), 400

        print("準備進行資料庫操作")
        # ... (新增使用者的資料庫操作)
        print("資料庫操作完成")
        return jsonify({"message": "特殊使用者新增成功!"}), 201
    else:
        print("Content-Type 不是 application/json")
        return jsonify({"error": "Content-Type must be application/json"}), 415


if __name__ == '__main__':
    app.run(debug=True, port=5000)


# 接收使用者表單資料並新增到 users 表
@app.route('/api/data', methods=['POST'])
def add_user():
    if request.content_type == 'application/json':
        data = request.get_json()
        account = data.get('帳號')
        user_level = data.get('使用者等級')
        is_active = data.get('是否激活', False)  # 預設為 False

        if not account or user_level is None:
            return jsonify({"error": "帳號和使用者等級是必填欄位"}), 400

        cursor = mysql.connection.cursor()
        try:
            cursor.execute("INSERT INTO users (帳號, 使用者等級, 是否激活) VALUES (%s, %s, %s)", (account, user_level, is_active))
            mysql.connection.commit()
            return jsonify({"message": "使用者新增成功!", "user_id": cursor.lastrowid}), 201
        except Exception as e:
            mysql.connection.rollback()
            return jsonify({"error": f"新增使用者失敗: {str(e)}"}), 500
        finally:
            cursor.close()
    else:
        return jsonify({"error": "Content-Type 必須是 application/json"}), 415

@app.route('/api/users/<int:user_id>', methods=['GET'])
# 如果需要 Hawk 驗證，在這裡添加裝飾器，例如 @hawk_required
def get_user(user_id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT ID, 帳號, 使用者等級, 是否激活 FROM users WHERE ID = %s", (user_id,))
    user = cursor.fetchone()
    cursor.close()

    if user:
        user_dict = {
            'ID': user[0],
            '帳號': user[1],
            '使用者等級': user[2],
            '是否激活': bool(user[3])  # 將 BOOLEAN 轉換為 Python 的 bool
        }
        return jsonify(user_dict), 200
    else:
        return jsonify({"error": "找不到該使用者"}), 404

@app.route('/api/all', methods=['GET'])
# 如果需要 Hawk 驗證，在這裡添加裝飾器
def get_all_users():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT ID, 帳號, 使用者等級, 是否激活 FROM users")
    users = cursor.fetchall()
    cursor.close()

    user_list = []
    for user in users:
        user_dict = {
            'ID': user[0],
            '帳號': user[1],
            '使用者等級': user[2],
            '是否激活': bool(user[3])
        }
        user_list.append(user_dict)

    return jsonify(user_list), 200

# 以下是您原有的路由，可以保留或根據需要修改
# Create Product
@app.route('/create', methods=['POST'])
def create_product():
    data = request.json
    name = data['name']
    price = data['price']
    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO products (name, price) VALUES (%s, %s)", (name, price))
    mysql.connection.commit()
    return jsonify({"message": "Product created successfully!"})

# Read Products
@app.route('/read', methods=['GET'])
def read_products():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM products")
    rows = cursor.fetchall()
    return jsonify(rows)

# Update Product
@app.route('/update/<int:id>', methods=['PUT'])
def update_product(id):
    data = request.json
    name = data['name']
    price = data['price']
    cursor = mysql.connection.cursor()
    cursor.execute("UPDATE products SET name = %s, price = %s WHERE id = %s", (name, price, id))
    mysql.connection.commit()
    return jsonify({"message": "Product updated successfully!"})

# Delete Product
@app.route('/delete/<int:id>', methods=['DELETE'])
def delete_product(id):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM products WHERE id = %s", (id,))
    mysql.connection.commit()
    return jsonify({"message": "Product deleted successfully!"})

@app.route('/')
def hello_world():
    return 'Hello World!'

if __name__ == '__main__':
    app.run(debug=True, port=5000)


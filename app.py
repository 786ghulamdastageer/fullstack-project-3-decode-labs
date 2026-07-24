from flask import Flask, request, jsonify, render_template
from database import get_connection, init_db

app = Flask(__name__)
init_db()

@app.route('/')
def index():
    return render_template('index.html')

# ---------- CATEGORY ----------
@app.route('/api/categories', methods=['POST'])
def create_category():
    data = request.get_json()
    conn = get_connection()
    try:
        cur = conn.execute("INSERT INTO category (name) VALUES (?)", (data.get('name'),))
        conn.commit()
        return jsonify({"category_id": cur.lastrowid}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        conn.close()

@app.route('/api/categories', methods=['GET'])
def get_categories():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM category").fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows]), 200

# ---------- SUPPLIER ----------
@app.route('/api/suppliers', methods=['POST'])
def create_supplier():
    data = request.get_json()
    conn = get_connection()
    try:
        cur = conn.execute(
            "INSERT INTO supplier (name, contact) VALUES (?, ?)",
            (data.get('name'), data.get('contact'))
        )
        conn.commit()
        return jsonify({"supplier_id": cur.lastrowid}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        conn.close()

@app.route('/api/suppliers', methods=['GET'])
def get_suppliers():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM supplier").fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows]), 200

# ---------- PRODUCT (CRUD) ----------
@app.route('/api/products', methods=['POST'])
def create_product():
    data = request.get_json()
    conn = get_connection()
    try:
        cur = conn.execute(
            "INSERT INTO product (name, sku, price, quantity, category_id) VALUES (?, ?, ?, ?, ?)",
            (data.get('name'), data.get('sku'), data.get('price'),
             data.get('quantity'), data.get('category_id'))
        )
        product_id = cur.lastrowid

        conn.execute(
            "INSERT INTO product_detail (product_id, description, warranty_months) VALUES (?, ?, ?)",
            (product_id, data.get('description', ''), data.get('warranty_months', 0))
        )

        for sid in data.get('supplier_ids', []):
            conn.execute(
                "INSERT INTO product_supplier (product_id, supplier_id) VALUES (?, ?)",
                (product_id, sid)
            )

        conn.commit()
        return jsonify({"product_id": product_id}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        conn.close()

@app.route('/api/products', methods=['GET'])
def get_products():
    conn = get_connection()
    rows = conn.execute("""
        SELECT p.*, c.name AS category_name
        FROM product p
        LEFT JOIN category c ON p.category_id = c.category_id
    """).fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows]), 200

@app.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    conn = get_connection()
    product = conn.execute("SELECT * FROM product WHERE product_id = ?", (product_id,)).fetchone()
    if not product:
        conn.close()
        return jsonify({"error": "Product not found"}), 404

    detail = conn.execute("SELECT * FROM product_detail WHERE product_id = ?", (product_id,)).fetchone()
    suppliers = conn.execute("""
        SELECT s.supplier_id, s.name FROM supplier s
        JOIN product_supplier ps ON s.supplier_id = ps.supplier_id
        WHERE ps.product_id = ?
    """, (product_id,)).fetchall()
    conn.close()

    result = dict(product)
    result['detail'] = dict(detail) if detail else None
    result['suppliers'] = [dict(s) for s in suppliers]
    return jsonify(result), 200

@app.route('/api/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    data = request.get_json()
    conn = get_connection()
    try:
        cur = conn.execute("""
            UPDATE product SET name = ?, sku = ?, price = ?, quantity = ?, category_id = ?
            WHERE product_id = ?
        """, (data.get('name'), data.get('sku'), data.get('price'),
              data.get('quantity'), data.get('category_id'), product_id))

        if cur.rowcount == 0:
            conn.close()
            return jsonify({"error": "Product not found"}), 404

        conn.execute("""
            UPDATE product_detail SET description = ?, warranty_months = ?
            WHERE product_id = ?
        """, (data.get('description', ''), data.get('warranty_months', 0), product_id))

        conn.commit()
        return jsonify({"message": "Product updated"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        conn.close()

@app.route('/api/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    conn = get_connection()
    try:
        conn.execute("DELETE FROM product_supplier WHERE product_id = ?", (product_id,))
        conn.execute("DELETE FROM product_detail WHERE product_id = ?", (product_id,))
        cur = conn.execute("DELETE FROM product WHERE product_id = ?", (product_id,))
        conn.commit()

        if cur.rowcount == 0:
            return jsonify({"error": "Product not found"}), 404
        return jsonify({"message": "Product deleted"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        conn.close()

if __name__ == '__main__':
    import logging
    logging.basicConfig(level=logging.INFO)
    from waitress import serve
    serve(app, host='127.0.0.1', port=5000)
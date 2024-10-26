from sql_connection import get_sql_connection

def get_all_products():
    cnx=get_sql_connection()
    cursor=cnx.cursor()
    querry=("SELECT p.product_id,p.name,u.uom_name,p.price_per_unit FROM products p  INNER JOIN uom u ON p.uom_id=u.uom_id")
    cursor.execute(querry)
    response=[]

    for (product_id,name,uom_name,price_per_unit) in cursor:
        response.append(
            {'product_id':product_id, 'name':name, 'uom_name':uom_name, 'price_per_unit':price_per_unit}
        )
    cnx.close()
    return  response


def insert_new_product(product):
    cnx=get_sql_connection()
    cursor=cnx.cursor()
    query=("INSERT INTO products (name,uom_id,price_per_unit) VALUES  (%s ,%s ,%s)")
    data=(product['product_name'],product['uom_id'],product['price_per_unit'])
    cursor.execute(query,data)
    cnx.commit()
    return cursor.lastrowid


def delete_product(product_id):
    cnx = get_sql_connection()
    cursor = cnx.cursor()

    # Correct SQL query
    query = "DELETE FROM gs.products WHERE product_id = %s"

    # Correctly pass the parameters as a tuple
    cursor.execute(query, (product_id,))

    # Commit the transaction
    cnx.commit()

    # Return the number of rows affected
    return cursor.rowcount


if __name__ =='__main__':
    print(get_all_products())



























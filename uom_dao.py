from sql_connection import get_sql_connection
def get_uoms():
    cnx=get_sql_connection()
    cursor=cnx.cursor()
    query="SELECT * FROM uom"
    cursor.execute(query)
    response=[]
    for (uom_id,uom_name) in cursor:
        response.append({
            'uom_id':uom_id,'uom_name':uom_name
        })

    return response

if __name__ =='__main__':
    pass



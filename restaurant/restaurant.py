from flask import jsonify
from flask_restful import Resource, reqparse
from restaurant import mssqlcur,mail


import json

from flask_mail import Mail, Message

parser = reqparse.RequestParser()




class Restaurant(Resource):
    # @jwt_required
    def __init__(self):
        parser.add_argument(
            'name',  required=False)
        parser.add_argument(
            'address',  required=False)

        parser.add_argument('uid',  required=False)

        parser.add_argument('status',required=False)
        parser.add_argument('email', required=False)
        parser.add_argument('phone', required=False)
        parser.add_argument('restaurant_id', required=False)


        # self.uid = get_jwt_identity()
        # self.user = get_jwt_claims()

    # creating database and insertion of client
    def post(self):
        # #print("client")
        res_data = parser.parse_args()

        try:

            cursor = mssqlcur.conn.cursor()

            cursor.execute("insert into restaurant(name, address, status,email, phone) VALUES (%s,%s,%s,%s,%s)", (
                str(res_data['name']), str(res_data['address']),
               str(res_data['status']), str(res_data['email']),
                str(res_data['phone'])
            ))


            mssqlcur.conn.commit()
            #print("inserted")
            return {"message": "success", "statusCode": 1}
        except Exception as e:
            #print("exc",e)
            return {"message": e, "statusCode": 0}




    def get(self):

        mydata = parser.parse_args()

        cursor = mssqlcur.conn.cursor()

        cursor.execute("select * from restaurant ")

        data = cursor.fetchall()
        result = []
        tables_data=[]
        menu_data=[]
        for i in data:

            cursor.execute("select * from menu where restaurant_id="+str(i[0])+" ")
            menu_d=cursor.fetchall()
            for k in menu_d:
                menu_data.append({'menu_id': k[0], 'name': k[1],
                           'course': k[2],
                           'price': k[3], 'description': k[4], 'restaurant': k[5]
                           })
            cursor.execute("select * from tables where restaurant_id=" + str(i[0]) + " ")
            table_d = cursor.fetchall()
            for w in table_d:
                #print(w)
                tables_data.append({'table_id': w[0], 'name': w[1],
                           'restaurant': w[2],
                           'availability_status': w[3]

                           })
            result.append({'restaurantId': i[0], 'name': i[1],
                           'email': i[2],
                           'phone': i[3],  'status': i[4],
                           'address': i[5],"menus":menu_data,"tables":tables_data

                           })
        if result != []:
            return {"data": result, "statusCode": 1}
        else:
            return {"message": "no data found", "statusCode": 0}

    def put(self):
        #print("started")
        try:

            data = parser.parse_args()


            cursor = mssqlcur.conn.cursor()
            cursor.execute("UPDATE appointments SET name='" + str(data['name']) + "', email='" + str(
                data['email']) + "', mobile='" + str(data['mobile']) + "', product_type='" + str(
                data['productType']) + "', appointment_type='" + str(data['appointmentType']) + "', remarks='" + str(
                data['remarks']) + "', status='" + str(data['status']) + "', time_='" + str(
                data['time']) + "',updated_by='" + str(data['updatedBy']) + "'  WHERE appointment_id='" + str(
                data['appointmentId']) + "'")

            mssqlcur.conn.commit()
            return {"message": "success", "statusCode": 1}
        except Exception as e:
            return {"message": e, "statusCode": 0}

    def delete(self):

        try:

            data = parser.parse_args()

            cursor = mssqlcur.conn.cursor()

            cursor.execute("delete from restaurant where  id='" + str(data['restaurant_id']) + "'")

            mssqlcur.conn.commit()
            return {"message": "success", "statusCode": 1}
        except Exception as e:
            return {"message": e, "statusCode": 0}
class Menu(Resource):
    # @jwt_required
    def __init__(self):
        parser.add_argument(
            'name',  required=False)
        parser.add_argument(
            'course',  required=False)
        parser.add_argument('price', required=False)
        parser.add_argument('description',  required=False)
        parser.add_argument('restaurant_id', required=False)
        parser.add_argument('menu_id', required=False)


    # creating database and insertion of client
    def post(self):
        # #print("client")
        res_data = parser.parse_args()
        #print(res_data)
        #print(type(res_data))
        try:

            cursor = mssqlcur.conn.cursor()
            #print("going to insert")
            cursor.execute("insert into menu(name, course, price, description, restaurant_id)values(%s,%s,%s,%s,%s)",
                (str(res_data['name']),str(res_data['course']),
                 str(res_data['price']), str(res_data['description']),str(res_data['restaurant_id'])) )
            #print("committ")
            mssqlcur.conn.commit()
            #print("inserted")
            return {"message": "success", "statusCode": 1}
        except Exception as e:
            #print("exc",e)
            return {"message": e, "statusCode": 0}




    def get(self):

        mydata = parser.parse_args()
        #print("cominggg")
        cursor = mssqlcur.conn.cursor()

        cursor.execute("select * from menu")

        data = cursor.fetchall()
        result = []
        for i in data:
            result.append({'menu_id': i[0], 'name': i[1],
                           'course': i[2],
                           'price': i[3], 'description': i[4], 'restaurant': i[5]
                           })
        if result != []:
            return {"data": result, "statusCode": 1}
        else:
            return {"message": "no data found", "statusCode": 0}

    def put(self):
        #print("started")
        try:

            data = parser.parse_args()


            cursor = mssqlcur.conn.cursor()
            cursor.execute("UPDATE menu SET name='" + str(data['name']) + "', course='" + str(
                data['course']) + "', price='" + str(data['price']) + "', description='" + str(
                data['description']) + "'  WHERE id='" + str(
                data['menu_id']) + "'")

            mssqlcur.conn.commit()
            return {"message": "success", "statusCode": 1}
        except Exception as e:
            return {"message": e, "statusCode": 0}

    def delete(self):

        try:

            data = parser.parse_args()

            cursor = mssqlcur.conn.cursor()

            cursor.execute("delete from menu where  id='" + str(data['menu_id']) + "'")

            mssqlcur.conn.commit()
            return {"message": "success", "statusCode": 1}
        except Exception as e:
            return {"message": e, "statusCode": 0}

class Tables(Resource):
    # @jwt_required
    def __init__(self):
        parser.add_argument(
            'name',  required=False)
        parser.add_argument(
            'restaurant_id',  required=False)
        parser.add_argument('availability_status', required=False)
        parser.add_argument('table_id', required=False)

        # self.uid = get_jwt_identity()
        # self.user = get_jwt_claims()

    # creating database and insertion of client
    def post(self):
        # #print("client")
        res_data = parser.parse_args()
        #print(res_data)
        #print(type(res_data))
        try:

            cursor = mssqlcur.conn.cursor()
            #print("going to insert")
            cursor.execute("insert into tables(name, restaurant_id, availability_status)values(%s,%s,%s)",
                (str(res_data['name']),str(res_data['restaurant_id']),
                 str(res_data['availability_status'])) )
            #print("committ")
            mssqlcur.conn.commit()
            #print("inserted")
            return {"message": "success", "statusCode": 1}
        except Exception as e:
            #print("exc",e)
            return {"message": e, "statusCode": 0}




    def get(self):

        mydata = parser.parse_args()
        #print("cominggg")
        cursor = mssqlcur.conn.cursor()

        cursor.execute("select * from tables")

        data = cursor.fetchall()
        result = []
        for i in data:
            result.append({'table_id': i[0], 'name': i[1],
                           'restaurant': i[2],
                           'availability_status': i[3]

                           })
        if result != []:
            return {"data": result, "statusCode": 1}
        else:
            return {"message": "no data found", "statusCode": 0}

    def put(self):
        #print("started")
        try:

            data = parser.parse_args()

            data['updatedBy'] = "A"
            cursor = mssqlcur.conn.cursor()
            cursor.execute("UPDATE tables SET name='" + str(data['name']) + "', availability_status='" + str(
                data['availability_status']) + "'  WHERE id='" + str(
                data['table_id']) + "'")

            mssqlcur.conn.commit()
            return {"message": "success", "statusCode": 1}
        except Exception as e:
            return {"message": e, "statusCode": 0}

    def delete(self):

        try:

            data = parser.parse_args()

            cursor = mssqlcur.conn.cursor()

            cursor.execute("delete from tables where  id='" + str(data['table_id']) + "'")

            mssqlcur.conn.commit()
            return {"message": "success", "statusCode": 1}
        except Exception as e:
            return {"message": e, "statusCode": 0}
class Booking(Resource):
    # @jwt_required
    def __init__(self):
        parser.add_argument(
            'user',  required=False)
        parser.add_argument(
            'table',  required=False)
        parser.add_argument('menu', required=False)
        parser.add_argument('total',  required=False)
        parser.add_argument('paid_amount', required=False)
        parser.add_argument('payment_id', required=False)
        parser.add_argument('payment_status', required=False)


    # creating database and insertion of client
    def post(self):
        # #print("client")
        res_data = parser.parse_args()

        try:

            cursor = mssqlcur.conn.cursor()

            cursor.execute("insert into booking(total,paid_amount,payment_id,payment_status,menu_id,table_id,user_id) VALUES (%s,%s,%s,%s,%s,%s,%s)", (
                str(res_data['total']), str(res_data['paid_amount']),
                str(res_data['payment_id']), str(res_data['payment_status']),
                str(res_data['menu']),  str(res_data['table']),  str(res_data['user'])
            ))

            mssqlcur.conn.commit()

            cursor.execute("select username,email from user where id="+str(res_data['user'])+"")
            user_data=cursor.fetchone()

            msg = Message('Restaurant booking', sender='preethireethu14@gmail.com', recipients=[user_data[1]])
            msg.body = "Hello!! Your booking is successfully done"
            mail.send(msg)

            return {"message": "success", "statusCode": 1}
        except Exception as e:
            #print("exc",e)
            return {"message": e, "statusCode": 0}




    def get(self):

        mydata = parser.parse_args()
        #print("cominggg")
        cursor = mssqlcur.conn.cursor()

        cursor.execute("select id,total,paid_amount,payment_id,payment_status,menu_id,table_id,user_id from booking")

        data = cursor.fetchall()
        result = []
        for i in data:
            result.append({'booking_id': i[0], 'user': i[7],
                           'table': i[6],
                           'menu': i[5], 'total': i[1], 'paid_amount': i[2],"payment_id":i[3],"payment_status":i[4]
                           })
        if result != []:
            return {"data": result, "statusCode": 1}
        else:
            return {"message": "no data found", "statusCode": 0}

    def put(self):
        #print("started")
        try:

            data = parser.parse_args()


            cursor = mssqlcur.conn.cursor()
            cursor.execute("UPDATE menu SET user='" + str(data['user']) + "', table='" + str(
                data['table']) + "', menu='" + str(data['menu']) + "', total='" + str(
                data['total']) + "' , paid_amount='" + str(
                data['paid_amount']) + "' , payment_status='" + str(
                data['payment_status']) + "' , payment_id='" + str(
                data['payment_id']) + "'  WHERE id='" + str(
                data['booking_id']) + "'")

            mssqlcur.conn.commit()
            return {"message": "success", "statusCode": 1}
        except Exception as e:
            return {"message": e, "statusCode": 0}

    def delete(self):

        try:

            data = parser.parse_args()

            cursor = mssqlcur.conn.cursor()

            cursor.execute("delete from booking where  id='" + str(data['booking_id']) + "'")

            mssqlcur.conn.commit()
            return {"message": "success", "statusCode": 1}
        except Exception as e:
            return {"message": e, "statusCode": 0}
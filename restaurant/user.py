from flask import jsonify
from flask_restful import Resource, reqparse
from restaurant import bcrypt, jwt
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required,
                                jwt_refresh_token_required, get_jwt_identity, get_raw_jwt, get_jwt_claims,
                                get_current_user)


import json
import p#print
import datetime
from restaurant import mssqlcur
parser = reqparse.RequestParser()

def hashPassword(password):
    return bcrypt.generate_password_hash(password).decode('utf-8')


class UserObject:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


@jwt.user_claims_loader
def add_claims_to_access_token(user):
    return user.__dict__


@jwt.user_identity_loader
def user_identity_lookup(user):
    #print("user",user)
    return user.id


class UserLogin(Resource):
    def __init__(self, app=None):
        parser.add_argument(
            'username', help='Email id or user id required', required=True)
        parser.add_argument(
            'password', help='Password is required', required=True)

    def post(self):
        args = parser.parse_args()

        username, password = args['username'], args['password']
        cursor = mssqlcur.conn.cursor()
        #print(username,password)

        cursor.execute("select id,password from user where id="+str(username)+"")
        data =cursor.fetchone()
        #print(data)
        if data and bcrypt.check_password_hash(data[1], password):


            user = UserObject(
                id=data[0], password=password)
            expires = datetime.timedelta(days=1)
            access_token = create_access_token(identity=user, expires_delta=expires)


            ret = {

                'access_token': access_token,

                'class': 'success',
                # "data": mongoIdToStr(data),

                'statusCode': 1,

                "uid": data[1]
            }

            return ret, 200

        else:
            return {"message": "Invalid email/uid or password", 'statusCode': 0}, 401




class Users(Resource):

    def __init__(self):
        parser.add_argument('username', required=False)
        parser.add_argument('password', required=False)
        parser.add_argument('email', required=False)
        parser.add_argument('phone', required=False)
        parser.add_argument('user_id', required=False)


    def post(self):
        data = parser.parse_args()
        try:
            cursor = mssqlcur.conn.cursor()

            #print(data['password'])
            data['password'] = hashPassword(data['password'])

            cursor.execute(
                "insert into user(username, email, phone, password) "
                "values(%s,%s,%s,%s)",
                (data['username'], data['email'], data['phone'], data['password']
                 ))
            mssqlcur.conn.commit()
            return {"message": "success", "statusCode": 1}
        except Exception as e:
            #print("exc",e)
            return {"message": e, "statusCode": 0}

    def get(self):
        #print("-------")
        # mysqlcur.cursor.execute("select * from features")
        data = parser.parse_args()
        #print("123", data)
        cursor = mssqlcur.conn.cursor()
        #print("345")
        if data.get("uid") != None:

            cursor.execute("select * from user where id='" + str(data['user_id']) + "'")

        else:
            cursor.execute("select * from user")
        data = cursor.fetchall()

        result = []
        for i in data:
            #print("ii", i)

            result.append({"user_id": i[0], "name": i[1], "email": i[2], "phone": i[3],
                          })
        if result != []:
            return {"data": result, "statusCode": 1}
        else:
            return {"message": "no data found", "statusCode": 0}

    def put(self):
        try:
            data = parser.parse_args()
            cursor = mssqlcur.conn.cursor()
            cursor.execute("update user"
                           " set name='" + str(data['name']) + "',email='" + str(
                data['email']) + "',phone='" + str(data['phone']) + "' where id='" + str(data['user_d']) + "' ")
            mssqlcur.conn.commit()
            return {"message": "success", "statusCode": 1}
        except Exception as e:
            return {"message": e, "statusCode": 0}

    def delete(self):
        #print("started")
        try:
            #print("-----")
            data = parser.parse_args()
            #print(data)
            cursor = mssqlcur.conn.cursor()

            cursor.execute("delete from user where  id='" + str(data['user_id']) + "'")

            mssqlcur.conn.commit()
            return {"message": "success", "statusCode": 1}
        except Exception as e:
            return {"message": e, "statusCode": 0}



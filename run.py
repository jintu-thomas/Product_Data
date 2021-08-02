from flask import Flask,jsonify
from flask.wrappers import Response
from flask_restful import Api, Resource,reqparse
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydb.db'

api = Api(app)
db =  SQLAlchemy()

@app.before_first_request
def create_tables():
    db.create_all() 

class Product(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    user_id = db.Column(db.Integer)
    rating = db.Column(db.Integer)
    desc = db.Column(db.String)

    def __init__(self,user_id,rating,desc):
        self.user_id = user_id
        self.rating = rating
        self.desc = desc

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def json(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'rating': self.rating,
            'desc': self.desc
        }

    @classmethod
    def find_by_id(cls,_id):
        return cls.query.filter_by(id = _id).first()
    
    def json(self):
        return {
            'id':self.id,
            'user_id': self.user_id,
            'rating': self.rating,
            'desc': self.desc
        }

class Data(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('user_id',
        type =int,
        required= True,
        help = "this field can not be left as blank "
    )
    parser.add_argument('rating',
        type =int,
        required= True,
        help = "this field can not be left as blank "
    )
    parser.add_argument('desc',
        type =str,
        required= True,
        help = "this field can not be left as blank "
    )
    
    def post(self):
        data = Data.parser.parse_args()
        product = Product(**data)
        product.save_to_db()
        return jsonify({ 'user_id': data['user_id'], 'rating':data['rating'], 'desc':data['desc']})

class Data1(Data):
    def get(self,id):
        pro = Product.find_by_id(id)
        if pro:
            return pro.json()           
        return {"message": "not found"}

    def put(self,id):
        data = Data.parser.parse_args()
        product= Product.find_by_id(id)
        
        if product:
            product.user_id = data['user_id'],
            product.rating = data['rating'],
            product.desc = data['desc']
        product.save_to_db()
        return product.json()

    def delete(self,id):
        product = Product.find_by_id(id)
        if product:
            product.delete_from_db()
        return {"message": "deleted successfully"}
    
api.add_resource(Data,'/data')
api.add_resource(Data1,'/data/<int:id>')

if __name__=='__main__':
    db.init_app(app)        #circular imports
    app.run(port = 5000,debug=True)
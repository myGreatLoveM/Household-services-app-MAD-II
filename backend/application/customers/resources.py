from flask_restful import Resource


class BookAPI(Resource):

    def get(self, cust_id):
        return {"msg": "booking successful"}
    
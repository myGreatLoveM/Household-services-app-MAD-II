from flask_restful import Resource


class ServiceAPI(Resource):

    def get(self, prov_id):
        return {"msg": "service listed successfully"}
    
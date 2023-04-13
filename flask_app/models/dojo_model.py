from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask_app.models.ninja_model import Ninja


class Dojo:
    def __init__(self, data):
        self.id = data["id"]
        self.name = data["name"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.list_of_ninjas = []

    @classmethod
    def get_all(cls):
        query = """ 
        SELECT *
        FROM dojos;
        """

        result = connectToMySQL(DATABASE).query_db(query)

        list_of_dojos = []
        for row in result:
            list_of_dojos.append(cls(row))

        return list_of_dojos

    @classmethod
    def get_one(cls, data):
        query = """ 
        SELECT *
        FROM dojos
        WHERE id = %(id)s;
        """
        result = connectToMySQL(DATABASE).query_db(query, data)
        current_dojo = cls(result[0])
        return current_dojo

    @classmethod
    def get_one_with_ninjas(cls, data):
        query = """ 
        SELECT *
        FROM dojos d LEFT JOIN ninjas n
        ON d.id = n.dojo_id
        WHERE n.dojo_id = %(id)s;
        """

        result = connectToMySQL(DATABASE).query_db(query, data)
        if len(result) > 0:
            current_dojo = cls(result[0])
        else:
            return cls.get_one(data)

        for row in result:
            if row["n.id"] != None:
                current_ninja = {
                    "id": row["n.id"],
                    "first_name": row["first_name"],
                    "last_name": row["last_name"],
                    "age": row["age"],
                    "dojo_id": row["dojo_id"],
                    "created_at": row["n.created_at"],
                    "updated_at": row["n.updated_at"],
                }
                current_dojo.list_of_ninjas.append(Ninja(current_ninja))

        return current_dojo

    @classmethod
    def create_one(cls, data):
        query = """ 
        INSERT INTO dojos (name)
        VALUES (%(name)s)
        """

        return connectToMySQL(DATABASE).query_db(query, data)

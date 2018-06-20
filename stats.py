from flask_restful import Resource, reqparse
import sqlite3


class Stats(Resource):
    parser = reqparse.RequestParser()

    @classmethod
    def get(self):
        connection = sqlite3.connect('docs.db')
        cursor = connection.cursor()
        query = "SELECT COUNT(*) FROM documents"
        result = cursor.execute(query)
        row = result.fetchone()
        connection.close()
        if row:
            return {'document_count:': row[0]}

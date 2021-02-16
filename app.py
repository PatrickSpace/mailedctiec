from flask import Flask, jsonify, request
from flask_cors import cross_origin,CORS

app= Flask(__name__)

@app.route('/hello', methods=['GET'])
@cross_origin(origin='*')
def main():
    return "Hello"


if __name__ == '__main__':
	app.run(port=5000,debug=False)

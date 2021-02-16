from flask import Flask, jsonify, request, render_template, redirect, url_for
from flask_cors import cross_origin
import os

import functions 


app= Flask(__name__)


UPLOAD_FOLDER = 'static/files'
app.config['UPLOAD_FOLDER'] =  UPLOAD_FOLDER

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

# Get the uploaded files
@app.route("/", methods=['POST'])
def uploadFiles():
      # get the uploaded file
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
          # set the file path
        uploaded_file.save(file_path)
          # save the file
        functions.createContactsList(uploaded_file.filename)
    return redirect(url_for('uploadFiles'))

@app.route('/contacts/profesor/all', methods=['GET'])
def api_all():
    return jsonify(functions.contactList[0][1])

@app.route('/contacts/profesor', methods=['GET'])
def api_id():
    # Check if an ID was provided as part of the URL.
    # If ID is provided, assign it to a variable.
    # If no ID is provided, display an error in the browser.
    if 'id' in request.args:
        id = int(request.args['id'])
    else:
        return "Error: No id field provided. Please specify an id."

    # Create an empty list for our results
    results = []

    # Loop through the data and match results that fit the requested ID.
    # IDs are unique, but other fields might return many results
    for contact in functions.contactList[0][1]:
        if contact['id'] == id:
            results.append(contact)

    # Use the jsonify function from Flask to convert our list of
    # Python dictionaries to the JSON format.
    return jsonify(results)

@app.route('/hello', methods=['GET'])
@cross_origin(origin='*')
def main():
    return "Hello"


if __name__ == '__main__':
	app.run(port=5000,debug=False)

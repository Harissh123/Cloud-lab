from os import name
from pymysql import connections
import helper
from flask import Flask, request, Response
import json
from flaskext.mysql import MySQL
import decimal


app = Flask(__name__)

mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'todo'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

@app.route('/')
def hello_world():
   return 'Hello World!'

@app.route('/item/new', methods = ['POST'])
def add_item():
   #Get item from the POST body
   req_data = request.get_json()
   item = req_data['item']
   
   #Add item to the list
   res_data = helper.add_to_list(item)

   #Return error if item not added
   if res_data is None:
      response = Response("{'error': 'Item not added - '}"  + item, status=400 , mimetype='application/json')
      return response
   
   #Return response
   response = Response(json.dumps(res_data), mimetype='application/json')
   
   return response

@app.route('/items/due')
def get_all_items_due():
   # Get items from the helper
   res_data = helper.get_all_items_due()
   response = Response(json.dumps(res_data), mimetype='application/json')
   return response

@app.route('/items/overdue')
def get_all_items_overdue():
   # Get items from the helper
   res_data = helper.get_all_items_overdue()
   print(res_data)
   response = Response(json.dumps(res_data), mimetype='application/json')
   return response

@app.route('/items/finished')
def get_all_items_finished():
   # Get items from the helper
   res_data = helper.get_all_items_finished()
   print(res_data)
   response = Response(json.dumps(res_data), mimetype='application/json')
   return response

@app.route('/items/all')
def get_all_items():
   # Get items from the helper
   res_data = helper.get_all_items()
   print(res_data)
   response = Response(json.dumps(res_data), mimetype='application/json')
   return response

@app.route('/item/status', methods=['GET'])
def get_item():
   #Get parameter from the URL
   item_name = request.args.get('name')
   
   # Get items from the helper
   status = helper.get_item(item_name)
   
   #Return 404 if item not found
   if status is None:
      response = Response("{'error': 'Item Not Found - '}"  + item_name, status=404 , mimetype='application/json')
      return response

   #Return status
   res_data = {
      'status': status
   }

   response = Response(json.dumps(res_data), status=200, mimetype='application/json')
   return response

@app.route('/item/update', methods = ['PUT'])
def update_status():
   #Get item from the POST body
   req_data = request.get_json()
   item = req_data['item_name']
   status = req_data['status']
   
   #Update item in the list
   res_data = helper.update_status(item, status)
   if res_data is None:
      response = Response("{'error': 'Error updating item - '" + item + ", " + status   +  "}", status=400 , mimetype='application/json')
      return response
   
   #Return response
   response = Response(json.dumps(res_data), mimetype='application/json')
   
   return response

@app.route('/item/remove', methods = ['DELETE'])
def delete_item():
   #Get item from the POST body
   req_data = request.get_json()
   item = req_data['item']
   
   #Delete item from the list
   res_data = helper.delete_item(item)
   if res_data is None:
      response = Response("{'error': 'Error deleting item - '" + item +  "}", status=400 , mimetype='application/json')
      return response
   
   #Return response
   response = Response(json.dumps(res_data), mimetype='application/json')
   
   return response
# create a app route that calls change status fn of helper.
  # item name and status change has to be the request parameters.
if __name__ == '__main__':
    app.run(debug=True)
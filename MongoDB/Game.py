import pymongo
from flask import Flask,jsonify,render_template,request
from bson import json_util
app = Flask(__name__)

client = pymongo.MongoClient("mongodb://admin:QCEhtg52239@10.100.2.118:27017")
#client = pymongo.MongoClient("mongodb://admin:QCEhtg52239@node9141-advweb-03.app.ruk-com.cloud:11157")

db = client["MongoDB"]


####### index ###############
@app.route("/")
def index():
    texts = "Welcome to MongoDB"
    return texts

########## GET ALL #################
@app.route("/Game", methods=['GET'])
def get_allGame():
    game = db.Game
    dlc = db.DLC
    output = []
    outputdlc = []
    for x in game.find():
        output.append({'_id' : x['_id'],
                       'name' : x['name'],
                       'price' : x['price'],
                        'type' : x['type'],
                        'download' : x['download']})
    for y in dlc.find():
        output.append({'iddlc' : y['iddlc'],
                        'DLC' : y['DLC'],
                        'type' : y['type'],
                        'pricedlc' : y['pricedlc']})
         
    return jsonify(output,outputdlc)

############## GET ONE ############################
@app.route("/Game/<name>", methods=['GET'])
def get_oneGame(name):
    game = db.Game
    x = game.find_one({'name' : name})
    if x:
        output = {'name' : x['name'],
                  'price' : x['price'],
                    'type' : x['type'],
                    'download' : x['download']}
    else:
        output = "No such name"
    return jsonify(output)

############# JOIN  ###############

@app.route("/Join", methods=['GET'])
def get_join():
    game = db.Game
    output = game.aggregate([
        {
            '$lookup':
                {
                    'from': "DLC",
                    'localField': '_id',
                    'foreignField': 'iddlc',
                    'as': "DLC"
                }
        }
    ])
    
    return json_util.dumps(output)

############## JOIN name,nameweapon ###############

@app.route("/JoinDLC", methods=['GET'])
def get_joinDLC():
    game = db.Game
    output = game.aggregate([
        {
            '$lookup':
                {
                    'from': "DLC",
                    'localField': '_id',
                    'foreignField': 'iddlc',
                    'as': "DLC"
                }
        },
        {'$unwind':'$DLC'},
        {
            '$project': {'_id':1,'name':1,
                        'DLC':'$DLC.DLC',
                        'pricedlc':'$DLC.pricedlc'}
        },
    ])
    
    return json_util.dumps(output)
    



######################### INSERT ####################
@app.route('/Game', methods=['POST'])
def add_Game():
  game = db.Game
  name = request.json['name']
  price = request.json['price']
  typee = request.json['type']
  download = request.json['download']

  
  char_id = game.insert({'name': name, 
                         'price': price,
                        'type': typee,
                        'download': download})
  
  new_game = game.find_one({'_id': char_id })
  output = {'name' : new_game['name'], 
                        'price' : new_game['price'],
                        'type' : new_game['type'],
                        'download' : new_game['download'],}
  return jsonify(output)

##################### UPDATE ########################
@app.route('/Game/<name>', methods=['PUT'])
def update_Game(name):
    game = db.Game
    x = game.find_one({'name' : name})
    if x:
        myquery = {'name' : x['name'],'price' : x['price'],
                        'type' : x['type'],
                        'download' : x['download']}

    name = request.json['name']
    price = request.json['price']
    typee = request.json['type']
    download = request.json['download']
    
    newvalues = {"$set" : {'name' : name, 'price' : price,
                        'type' : typee,
                        'download' : download,}}

    char_id = game.update_one(myquery, newvalues)

    output = {'name' : name, 'price' : price,
                        'price' : price,
                        'type' : typee,
                        'download' : download}

    return jsonify(output)

##################### DELETE ############################ 
@app.route('/Game/<name>', methods=['DELETE'])
def delete_Game(name):
    game = db.Game
    x = game.find_one({'name' : name})

    game_id = game.delete_one(x)

    output = "Deleted complete"

    return jsonify(output)


if __name__ == "__main__":
    app.run(host='0.0.0.0',port = 80)
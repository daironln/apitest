from flask import Flask, request, jsonify
import hashlib
import hmac

app = Flask(__name__)

app.config.from_object('config')
app.secret_key = app.config['SECRET_KEY']

def string_generator(data_incoming):
    data = data_incoming.copy()
    del data['hash']
    keys = sorted(data.keys())
    string_arr = []
    for key in keys:
        string_arr.append(key+'='+data[key])
    string_cat = '\n'.join(string_arr)

    return string_cat

@app.route('/gethash', methods=['POST'])
def login():
    if request.method == 'POST':
        data = {
            "id" : request.form['id'],
            "first_name" : request.form['firstName'],
            "last_name" : request.form['lastName'],
            "username" : request.form['username'],
            "auth_date" : request.form['authDate'],
            "photo_url" : request.form['photoUrl'],
            "hash" : request.form['hash']
        }    
        
        data_check = string_generator(data)
        
        secret_key = hashlib.sha256(app.config.get('BOT_TOKEN').encode('utf-8')).digest()
        
        secret_key_bytes = secret_key
        data_check_string_bytes = bytes(data_check,'utf-8')
        hmac_string = hmac.new(secret_key_bytes, data_check_string_bytes, hashlib.sha256).hexdigest()
        
        return jsonify({
            "hash" : hmac_string
        })
            
            
    return jsonify({
        "text" : "Metodo no soportado"
    }), 405
    
    
            
if __name__=="__main__":
    app.run(debug=True,host='0.0.0.0')
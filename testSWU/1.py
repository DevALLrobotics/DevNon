#sever side 
from flask import Flask, request, jsonify
import json
app = Flask(__name__)

@app.route("/receive", methods=["POST"])
def receive():
    data = request.get_json()
    # print(data)
    check = data["data"]
    if check == "1":
        print("test1")
    elif check == "2":
        print("test2")
    elif check == "3":
        print("test3")
    
    return jsonify({
        "you_sent": data,
        "status": "ok"
        
    })
    
@
    

if __name__ == "__main__":
    app.run(debug=True,host='172.20.10.3',port=5000)
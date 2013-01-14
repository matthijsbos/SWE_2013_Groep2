from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "fuck me"
@app.route("/test")
def test():
    return "You posted it didn't you?"
@app.route("/launch",methods=['POST'])
def launch():
    return "Hello Google!"

if __name__ == '__main__':
        app.run()
        

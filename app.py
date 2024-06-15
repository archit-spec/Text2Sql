import flask

import flask_cors



@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run()
    app.run(debug=True)
    app.run(host='0.0.0.0', port=8080)
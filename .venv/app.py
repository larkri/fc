from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def wallet():
    return render_template('wallet.html')

@app.route('/send')
def send():
    return render_template('send.html')

if __name__ == '__main__':
    app.run()

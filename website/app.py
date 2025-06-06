from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')
@app.route('/vex123')
def vex123():
    return render_template('vex123.html')

@app.route('/vexgo')
def vexgo():
    return render_template('vexgo.html')

@app.route('/vexiq')
def vexiq():
    return render_template('vexiq.html')

@app.route('/vexv5')
def vexv5():
    return render_template('vexv5.html')

if __name__ == '__main__':
    app.run(debug=True)

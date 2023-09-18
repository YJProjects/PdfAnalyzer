from Main import locate_response
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        var = request.form.get('var')
        return jsonify(variable=locate_response(var))  # Return the variable as JSON response

    return render_template('index.html')

if __name__ == '__main__':
    app.run()

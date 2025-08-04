from flask import Flask, request, render_template_string

app = Flask(__name__)

HTML = '''
<!doctype html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Laddo - Multiplication Table</title>
</head>
<body>
  <h1>🍬 Laddo's Multiplication Table Generator</h1>
  <form method="post">
    <label for="number">Enter a number:</label>
    <input type="number" name="number" required>
    <button type="submit">Show Table</button>
  </form>

  {% if result %}
    <h2>Table of {{ number }}</h2>
    <ul>
      {% for n, i, product in result %}
        <li>{{ n }} × {{ i }} = {{ product }}</li>
      {% endfor %}
    </ul>
  {% endif %}
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def table():
    number = None
    result = []
    if request.method == 'POST':
        try:
            number = int(request.form['number'])
            result = [(number, i, number * i) for i in range(1, 11)]
        except ValueError:
            result = []
    return render_template_string(HTML, number=number, result=result)

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8000,debug=True)

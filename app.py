from flask import Flask, request, jsonify, send_file
import math
import os

app = Flask(__name__)

class ScientificCalculator:
    def __init__(self):
        self.memory = 0

    def evaluate_expression(self, expression):
        try:
            result = eval(expression, {"__builtins__": None}, {
                'sqrt': math.sqrt,
                'pow': math.pow,
                'log': math.log,
                'log10': math.log10,
                'sin': math.sin,
                'cos': math.cos,
                'tan': math.tan,
                'radians': math.radians,
                'degrees': math.degrees,
                'factorial': math.factorial,
                'pi': math.pi,
                'e': math.e
            })
            return result
        except Exception as e:
            return str(e)

@app.route('/')
def index():
    # Serve index.html from the same folder as app.py
    return send_file(os.path.join(os.path.dirname(__file__), 'index.html'))

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        data = request.get_json()
        if 'expression' not in data:
            return jsonify({"error": "Missing expression parameter"}), 400

        calc = ScientificCalculator()
        expression = data['expression']

        allowed_chars = "0123456789+-*/().^sincosradtanlogsqrtfactorialpie"
        if any(c not in allowed_chars for c in expression.replace(' ', '')):
            return jsonify({"error": "Invalid characters in expression"}), 400

        result = calc.evaluate_expression(expression)

        if isinstance(result, str):
            return jsonify({"error": result}), 400
        return jsonify({"result": result})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

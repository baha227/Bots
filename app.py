from flask import Flask, render_template, request
from flask_restx import Api, Resource

app = Flask(__name__)
api = Api(app)

def add(number_1, number_2):
    return number_1 + number_2

def subtract(number_1, number_2):
    return number_1 - number_2

def multiply(number_1, number_2):
    return number_1 * number_2

def divide(number_1, number_2):
    if number_2 == 0:
        return 'Ошибка: Деление на ноль'
    return number_1 / number_2

def degree(number_1, number_2):
    return number_1 ** number_2

def maximum(number_1, number_2):
    return max(number_1, number_2)

def minimum(number_1, number_2):
    return min(number_1, number_2)

@app.route('/', methods=['GET', 'POST'])
@app.route('/calculator/', methods=['GET', 'POST'])
def calculator():
    result = None
    if request.method == 'POST':
        try:
            num1 = float(request.form['num1'])
            num2 = float(request.form['num2'])
            operation = request.form['operation']
            
            # Отладочный вывод значений
            print(f'num1: {num1}, num2: {num2}, operation: {operation}')
            
            operations = {
                '+': add,
                '-': subtract,
                '*': multiply,
                '/': divide,
                '**': degree,
                'max': maximum,
                'min': minimum
            }
            
            if operation in operations:
                result = operations[operation](num1, num2)
            else:
                result = 'Ошибка: Неизвестная операция'
        except ValueError:
            result = 'Ошибка: Введите корректные числа'
    
    # Отладочный вывод результата
    print(f'Результат: {result}')
    
    return render_template('index.html', result=result)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True, port=5002, host='0.0.0.0')
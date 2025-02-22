import os
import json
import subprocess
from flask import Flask, render_template, request
from flask_restx import Api, Resource

app = Flask(__name__)
api = Api(app)

# --- Основные функции калькулятора ---
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

# --- Основной маршрут калькулятора ---
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

# --- Обработчик webhook ---
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()

    # Логирование полученных данных в файл
    with open('webhook.log', 'a') as f:
        formatted_data = json.dumps(data, indent=4, ensure_ascii=False)
        print(f'Received data: {formatted_data}', file=f)

    # Директория, в которой расположен ваш сайт
    repo_dir = '/home/api/calculator'
    
    # Переходим в директорию репозитория и выполняем команду git pull
    try:
        subprocess.run(['git', 'pull'], cwd=repo_dir, check=True)
        print(f'Successfully updated repository in {repo_dir}')
    except subprocess.CalledProcessError as e:
        print(f'Error updating repository: {e}')

    return 'Webhook received and update triggered', 200

# --- Обработчик ошибки 404 ---
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# --- Запуск приложения ---
if __name__ == '__main__':
    app.run(debug=True, port=5002, host='0.0.0.0')

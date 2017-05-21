#!../env/bin/python

from flask import Flask, jsonify, abort, request, make_response

app = Flask(__name__)
API_URL = '/khanal/todo/api/v1/'

todos = [
    {
        'name': 'Brush my teeth',
        'status': True
    },
    {
        'name': 'Wash my face',
        'status': True
    },
    {
        'name': 'Take a shower',
        'status': False
    }
]
@app.route(API_URL + 'todos/<int:todo_id>', methods=['GET'])
def get_todo_with_id(todo_id):
    print(todo_id)
    if todo_id == 0 or todo_id > len(todos):
        return make_response(jsonify({'error': 'resource not found'}), 404)
    else:
        return jsonify(todos[todo_id-1])

@app.route(API_URL + 'todos', methods=['GET'])
def get_all_todos():
    return jsonify(todos)

@app.route(API_URL + 'todos', methods=['POST'])
def post_a_todo():
    name = 'name'
    status = 'status'
    if not request.json or not name in request.json:
        return make_response(jsonify({'error': 'bad request'}), 400)
    else:
        todo = {}
        todo[name] = request.json[name]
        if status in request.json:
            todo[status] = request.json[status]
        else:
            todo[status] = False
        todos.append(todo)
        todo['id'] = len(todos) - 1
        return jsonify(todo)

@app.route(API_URL + 'todos/<int:todo_id>', methods=['DELETE'])
def delete_a_todo(todo_id):
    if todo_id == 0 or todo_id > len(todos):
        return make_response(jsonify({'error': 'resource not found'}), 404)
    else:
        todos.pop(todo_id - 1)
        return jsonify({'result': 'resource deleted'})

@app.route(API_URL + 'todos/<int:todo_id>', methods=['PUT'])
def update_a_todo(todo_id):
    if todo_id == 0 or todo_id > len(todos):
        return make_response(jsonify({'error': 'resource not found'}), 404)
    else:
        name = 'name'
        status = 'status'
        if not request.json:
            return make_response(jsonify({'error': 'bad request'}), 400)
        else:
            if name in request.json:
                todos[todo_id][name] = request.json[name]
            if status in request.json:
                todos[todo_id][status] = request.json[status]
            todo = todos[todo_id]
            todo['id'] = todo_id
            return jsonify(todo)



if __name__ == '__main__':
    app.run(debug=True)

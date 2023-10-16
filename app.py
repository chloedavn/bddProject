# app.py
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Sample data as a list of dictionaries (you can replace this with your entities)
entities = []

@app.route('/')
def index():
    return render_template('index.html', entities=entities)

@app.route('/create', methods=['POST'])
def create_entity():
    # Validate and process the input data
    # Add your data validation logic here
    entity = {
        'name': request.form.get('name'),
        'age': request.form.get('age'),
        'weight': request.form.get('weight'),
        'is_student': request.form.get('is_student') == 'on'
    }
    entities.append(entity)
    return redirect(url_for('index'))

@app.route('/delete/<int:index>')
def delete_entity(index):
    if 0 <= index < len(entities):
        entities.pop(index)
    return redirect(url_for('index'))

@app.route('/update/<int:index>', methods=['GET', 'POST'])
def update_entity(index):
    if request.method == 'POST':
        # Validate and process the updated data
        # Add your data validation logic here
        updated_entity = {
            'name': request.form.get('name'),
            'age': request.form.get('age'),
            'weight': request.form.get('weight'),
            'is_student': request.form.get('is_student') == 'on'
        }
        if 0 <= index < len(entities):
            entities[index] = updated_entity
        return redirect(url_for('index'))
    elif 0 <= index < len(entities):
        return render_template('update.html', index=index, entity=entities[index])
    else:
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
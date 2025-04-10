from flask import Flask, render_template, request
import pickle
import os

# Initialize Flask app
app = Flask(__name__)

# Load the trained models
model_path = os.path.dirname(os.path.abspath(__file__))
prom_model = pickle.load(open(os.path.join(model_path, 'prom_model.pkl'), 'rb'))
drop_model = pickle.load(open(os.path.join(model_path, 'drop_model.pkl'), 'rb'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        fields = ['projector', 'smart_class', 'digital_library', 'computer_facility',
                  'internet_facility', 'library', 'playground', 'girls_toilet',
                  'boys_toilet', 'electricity', 'drinking_water', 'hand_wash']

        input_values = []
        for field in fields:
            val = request.form.get(field)
            if val is None or val.strip() == "":
                return render_template('index.html', error_message=f"Error: {field.replace('_', ' ').title()} cannot be empty.", request=request)
            input_values.append(float(val))

        # Make predictions
        pred_promotion = prom_model.predict([input_values])[0]
        pred_dropout = drop_model.predict([input_values])[0]

        # Format to 2 decimals
        pred_promotion = f"{pred_promotion:.2f}"
        pred_dropout = f"{pred_dropout:.2f}"

        return render_template('index.html', prediction_promotion=pred_promotion, prediction_dropout=pred_dropout, request=request)

    except ValueError as ve:
        return render_template('index.html', error_message="Error: Please enter valid numeric values.", request=request)

if __name__ == '__main__':
    app.run(debug=True)

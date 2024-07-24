import pickle
from flask import Flask, render_template, request

app = Flask(__name__)

# Load the model
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

# Route to render the home page
@app.route('/')
def home():
    return render_template('home.html')

# Route to render the index page with the prediction form
@app.route('/predict')
def index():
    return render_template('index.html')

# Route to handle form submission and prediction
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get input values from the form and convert to float
        u_q = float(request.form['u_q'])
        coolant = float(request.form['coolant'])
        u_d = float(request.form['u_d'])
        motor_speed = float(request.form['motor_speed'])
        i_d = float(request.form['i_d'])
        i_q = float(request.form['i_q'])
        ambient = float(request.form['ambient'])
        profile_id = float(request.form['profile_id'])
        stator_winding = float(request.form['stator_winding'])
        stator_tooth = float(request.form['stator_tooth'])
        stator_yoke = float(request.form['stator_yoke'])
        torque = float(request.form['torque'])

        # Make a prediction using the loaded model
        prediction = model.predict([[u_q, coolant, stator_winding, u_d, stator_tooth,
                                     motor_speed, i_d, i_q, stator_yoke, ambient, torque, profile_id]])

        # Render the result template with the prediction
        return render_template('result.html', prediction=prediction)

    except ValueError:
        error_message = "Ensure all input fields are filled and valid numbers."
        return render_template('error.html', error_message=error_message)

    except Exception as e:
        error_message = "Error processing prediction: {}".format(e)
        return render_template('error.html', error_message=error_message)

if __name__ == '__main__':
    app.run(debug=True)

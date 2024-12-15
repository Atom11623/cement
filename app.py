from flask import Flask, request, render_template

app = Flask(__name__)

# HTML template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cement Packing Balancer</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f9;
            margin: 0;
            padding: 0;
        }
        .container {
            max-width: 600px;
            margin: 50px auto;
            background: #fff;
            border-radius: 8px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
            padding: 20px;
        }
        h1 {
            text-align: center;
            color: #333;
        }
        form {
            display: flex;
            flex-direction: column;
            gap: 15px;
        }
        label {
            font-weight: bold;
        }
        input {
            padding: 10px;
            border: 1px solid #ccc;
            border-radius: 5px;
            font-size: 16px;
        }
        button {
            padding: 10px;
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 5px;
            font-size: 16px;
            cursor: pointer;
        }
        button:hover {
            background-color: #45a049;
        }
        .result {
            margin-top: 20px;
            padding: 15px;
            background: #e7f5e6;
            border: 1px solid #d4edda;
            border-radius: 5px;
            color: #155724;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Cement Packing Balancer</h1>
        <form method="post">
            <label for="total_bags">Total number of bags in the truck:</label>
            <input type="number" id="total_bags" name="total_bags" required>

            <label for="current_weight">Current truck weight (kg):</label>
            <input type="number" id="current_weight" name="current_weight" step="0.1" required>

            <label for="expected_weight">Expected truck weight (kg):</label>
            <input type="number" id="expected_weight" name="expected_weight" step="0.1" required>

            <button type="submit">Calculate</button>
        </form>

        {% if result %}
        <div class="result">
            <h2>Results:</h2>
            <p>{{ result|safe }}</p>
        </div>
        {% endif %}
    </div>
</body>
</html>
"""

def calculate_adjusted_weight(total_bags, current_weight, expected_weight):
    weight_difference = current_weight - expected_weight

    if weight_difference == 0:
        return "The truck is already balanced at the expected weight."

    adjustment_type = "underweight" if weight_difference < 0 else "overweight"
    weight_difference = abs(weight_difference)

    suggestions = []
    for unload_bags in range(50, total_bags, 50):
        remaining_bags = total_bags - unload_bags
        new_target_weight = (expected_weight - (remaining_bags * (current_weight / total_bags))) / unload_bags
        if 48 <= new_target_weight <= 53:
            suggestions.append(f"Unload {unload_bags} bags. Adjust target weight to {new_target_weight:.2f} kg.")

    if not suggestions:
        return "No valid adjustments found within the target weight range (48kg to 53kg)."

    return f"The truck is {adjustment_type} by {weight_difference} kg. Suggestions:<br>" + "<br>".join(suggestions)

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        total_bags = int(request.form["total_bags"])
        current_weight = float(request.form["current_weight"])
        expected_weight = float(request.form["expected_weight"])
        result = calculate_adjusted_weight(total_bags, current_weight, expected_weight)

    return render_template_string(HTML_TEMPLATE, result=result)

if __name__ == "__main__":
    app.run(debug=True)

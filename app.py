import dash
from dash import dcc, html, Input, Output
import pickle
import pandas as pd


# Load your model and encoder from the same pickle file
with open('income_model.pkl', 'rb') as file:
    model, encoder = pickle.load(file)

# Initialize the Dash app
app = dash.Dash(__name__)
server = app.server


# Include Google Fonts link for Poppins
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        <title>Income Prediction App</title>
        <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">
        {%metas%}
        {%favicon%}
        {%css%}
    </head>
    <body>
        <div id="root">
            {%app_entry%}
        </div>
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# Define your categorical variables
dropdown_categories = {
    'Place of Work': [ 'West Vlaanderen', 'Oost Vlaanderen', 'Antwerpen', 'Brussel', 'Limburg'],      
    'Degree': [ 'Masters', 'Lower than Masters', 'Above Masters'],

    'Experience Category': [ 'Entry-Level (0-5 yrs)', 'Associate (6-10 yrs)', 'Mid-Level(11-15 yrs)',
                            'Senior (16-20 yrs)', 'Lead (21-25 yrs)', 'Principal (26-30 yrs)', 
                            'Director (31-35 yrs)', 'Executive (36- 40 yrs)'],    

    'Education': [ 'Industrial engineering', 'Mechanical engineering ', 
                  'Civil engineering ', 'Electrical engineering','Chemical engineering',
                  'Bio engineering','Environmental engineering','Other'],


    'NACE Category': ['Other', 'C28 - Manufacture of machinery and equipment n.e.c.',
                      'C25 - Manufacture of fabricated metal products, except machinery and equipment',
                      'C10 - Manufacture of food products',
                      'C26 - Manufacture of computer, electronic and optical products',
                      'F41 - Construction of buildings',
                      'F42 - Civil engineering',
                      'C20 - Manufacture of chemicals and chemical products',
                      'D35 - Electricity, gas, steam and air conditioning supply',
                      'C27 - Manufacture of electrical equipment',
                      'F43 - Specialised construction activities',
                      'C24 - Manufacture of basic metals',
                      'C13 - Manufacture of textiles',
                      'C22 - Manufacture of rubber and plastic products',
                      'C21 - Manufacture of basic pharmaceutical products and pharmaceutical preparations',
                      'C32 - Other manufacturing',
                      'C33 - Repair and installation of machinery and equipment',
                      'C29 - Manufacture of motor vehicles, trailers and semi-trailers',
                      'C19 - Manufacture of coke and refined petroleum products',
                      'C16 - Manufacture of products of wood, wood and cork, straw, plaiting materials',
                      'E37 - Sewerage',
                      'C23 - Manufacture of other non-metallic mineral products',
                      'C11 - Manufacture of beverages',
                      'C30 - Manufacture of other transport equipment',
                      'E38 - Waste collection, treatment and disposal activities; materials recovery',
                      'E36 - Water collection, treatment and supply',
                      'C31 - Manufacture of furniture',
                      'C18 - Printing and reproduction of recorded media',
                      'E39 - Remediation activities and other waste management services'],
}

original_columns = {
    'Place of Work': 'zip_workplace1',
    'Degree': 'degree_category',
    'Experience Category': 'experience_category',
    'Education': 'education',
    'NACE Category': 'nace'
}


# Define your benefits
benefits = [
    'Car','Fuel Card', 'Commuting Allowance', 'Phone', 
    'Phone Subscription', 'Computer', 'Meal Vouchers', 
    'Ecocheques', 'Hospitalisation Insurance', 'Group Insurance', 
    '13 month', '14 month', '15 month', 'Bonus', 
    'Commission', 'Compensation', 'Discount on Purchase', 'Telework', 'Internet', 
    'Meals at Company Restaurant', 'Reimbursement', 'Gift Vouchers', 'Stock', 
    'Fitness', 'Tablet', 'Culture and Sports Vouchers', 'Ironing'
]

original_benefits = {
    'Car': 'Benefit_Car',
    'Fuel Card': 'Benefit_Fuel_Card',
    'Commuting Allowance': 'Benefit_Commuting_Allowance',
    'Phone': 'Benefit_Phone',
    'Phone Subscription': 'Benefit_Phone_Subscription',
    'Computer': 'Benefit_Computer', 
    'Meal Vouchers': 'Benefit_Meal Vouchers',   
    'Ecocheques': 'Benefit_Ecocheques',
    'Hospitalisation Insurance': 'Benefit_Hospitalisation Insurance',
    'Group Insurance': 'Benefit_Group Insurance',
    '13 month': 'Benefit_13 month',
    '14 month': 'Benefit_14 month',
    '15 month': 'Benefit_15 month',
    'Bonus': 'Benefit_Bonus',
    'Commission': 'Benefit_Commission',
    'Compensation': 'Benefit_Compensation',
    'Discount on Purchase': 'Benefit_Discount on Purchase',
    'Telework': 'Benefit_Telework',
    'Internet': 'Benefit_Internet',
    'Meals at Company Restaurant': 'Benefit_Meals at Company Restaurant',
    'Reimbursement': 'Benefit_Reimbursement',
    'Gift Vouchers': 'Benefit_Gift',
    'Stock': 'Benefit_Stock',
    'Fitness': 'Benefit_Fitness',
    'Tablet': 'Benefit_Tablet',
    'Culture and Sports Vouchers': 'Benefit_Culture and Sports Vouchers',        
    'Ironing': 'Benefit_Ironing'    
}


# Layout of the Dash app
app.layout = html.Div(
    style={'backgroundColor': 'rgb(244, 244, 244)', 'fontFamily': 'Poppins'},
    children=[
        html.Img(src='assets/elekti_logo.png', style={'width': '10%', 'display': 'inline-block', 'position':'relative','top':'-15px'}),
        html.Img(src='assets/elekti_banner.png', style={'width': '25%', 'display': 'inline-block', 'position': 'relative', 'top': '-50px','left':'977px'}),
        html.Div(
            style={'textAlign': 'center', 'padding': '10px', 'backgroundColor': 'rgb(0, 123, 167)', 'height': '55px','position': 'relative', 'top': '-55px'},
            children=[
                html.H1('Benchmark Analysis: Income Prediction', style={'color': 'white', 'display': 'inline-block', 'paddingLeft': '5px',
                                                                        'font-size':'24px', 'position': 'center'})
            ]
        ),
        html.Div(
            style={'padding': '20px'},
            children=[
                html.Div(
                    id='dropdown-container',
                    children=[
                        html.Div(
                            children=[
                                html.Label(f'Select {var}'),
                                dcc.Dropdown(
                                    id=f'dropdown-{var}',
                                    options=[{'label': i, 'value': i} for i in options],
                                    value=None,
                                    optionHeight=50
                                )
                            ],
                            style={'width': '30%', 'display': 'inline-block', 'padding': '10px'}
                        )
                        for var, options in dropdown_categories.items()
                    ]
                ),
                html.Div(id='selection-warning', style={'textAlign': 'center', 'color': 'red', 'marginTop': '20px'}),
                html.H3('Select Benefits:', style={'textAlign': 'center'}),
                html.Div(
                    children=[
                        html.Div(
                            children=[
                                dcc.Checklist(
                                    id='checklist-benefits',
                                    options=[{'label': benefit, 'value': benefit} for benefit in benefits],
                                    value=[]
                                )
                            ],
                            style={'columns': 3, 'padding': '10px'}
                        )
                    ]
                ),
                html.Div(
                    style={'textAlign': 'center', 'marginTop': '20px'},
                    children=[
                        html.Button('Get The Income Prediction', id='predict-button', n_clicks=0, style={'padding': '10px 20px', 
                                                                                       'fontSize': '16px', 
                                                                                       'border-radius': '12px',
                                                                                       'backgroundColor': 'rgb(71, 68, 66)',
                                                                                       'color': 'white',
                                                                                       'fontFamily': 'Poppins'}),
                        html.Div(id='prediction-output', style={'marginTop': '20px', 'fontSize': '20px'})
                    ]
                )
            ]
        )
    ]
)

# Callback to update warning message and prediction
@app.callback(
    [Output('selection-warning', 'children'),
     Output('prediction-output', 'children')],
    [Input(f'dropdown-{var}', 'value') for var in dropdown_categories.keys()] + [Input('checklist-benefits', 'value')] + [Input('predict-button', 'n_clicks')]
)
def update_prediction(*args):
    n_clicks = args[-1]
    categorical_values = args[:-2]
    selected_benefits = args[-2]

    # Check if any dropdown category is None (not selected)
    if None in categorical_values:
        return 'Please select all dropdown categories for prediction.', ''

    if n_clicks > 0:
        # Map the display names to the original column names
        input_data = pd.DataFrame([categorical_values], columns=dropdown_categories.keys())
        input_data.rename(columns=original_columns, inplace=True)

        # Create a DataFrame for the benefits, setting 1 for selected and 0 for not selected
        benefits_data = pd.DataFrame([[1 if benefit in selected_benefits else 0 for benefit in benefits]], columns=benefits)
        benefits_data.rename(columns=original_benefits, inplace=True)

        # Combine the categorical data and benefits data
        combined_data = pd.concat([input_data, benefits_data], axis=1)



        combined_data = combined_data[['zip_workplace1', 'degree_category', 'experience_category', 'education', 'nace', 'Benefit_Car','Benefit_Fuel_Card', 'Benefit_Commuting_Allowance', 'Benefit_Phone', 
        'Benefit_Phone_Subscription', 'Benefit_Computer', 'Benefit_Meal Vouchers', 
        'Benefit_Ecocheques', 'Benefit_Hospitalisation Insurance', 'Benefit_Group Insurance', 
        'Benefit_13 month', 'Benefit_14 month', 'Benefit_15 month', 'Benefit_Bonus', 
        'Benefit_Commission', 'Benefit_Compensation', 'Benefit_Discount on Purchase', 'Benefit_Telework', 'Benefit_Internet', 
        'Benefit_Meals at Company Restaurant', 'Benefit_Reimbursement', 'Benefit_Gift', 'Benefit_Stock', 
        'Benefit_Fitness', 'Benefit_Tablet', 'Benefit_Culture and Sports Vouchers', 'Benefit_Ironing']] 

        # Encode the combined data
        input_encoded = encoder.transform(combined_data).toarray()

        # Make a prediction
        prediction = round(model.predict(input_encoded)[0], 2)
        pred_results = model.get_prediction(input_encoded)
        pred_ci = pred_results.conf_int(alpha=0.05)
        return '', f'Projected monthly income: €{prediction}, with potential earnings ranging from €{round(pred_ci[0][0],2)} to €{round(pred_ci[0][1],2)}.'

    return '', ''


if __name__ == '__main__':
    app.run_server(debug=True)

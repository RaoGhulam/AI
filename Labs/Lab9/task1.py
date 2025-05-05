import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler

def load_and_prepare_data(filepath):
    df = pd.read_csv(filepath)
    
    for col in df.columns:
        if df[col].dtype == 'object':
            df[col].fillna(df[col].mode()[0], inplace=True)
        else:
            df[col].fillna(df[col].median(), inplace=True)
    
    return df

def prepare_features(df):
    features = ['SquareFootage', 'Bedrooms', 'Bathrooms', 'HouseAge', 'Neighborhood']
    
    df_encoded = pd.get_dummies(df[features], columns=['Neighborhood'], drop_first=True)
    
    scaler = StandardScaler()
    num_cols = ['SquareFootage', 'Bedrooms', 'Bathrooms', 'HouseAge']
    df_encoded[num_cols] = scaler.fit_transform(df_encoded[num_cols])
    
    return df_encoded, df['Price']

def train_and_evaluate(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    print(f"Model Evaluation:")
    print(f"Mean Squared Error: {mse:.2f}")
    print(f"R-squared Score: {r2:.2f}")
    
    return model

def predict_price(model, new_data, feature_columns):
    new_df = pd.DataFrame([new_data])
    new_df_encoded = pd.get_dummies(new_df)
    
    for col in feature_columns:
        if col not in new_df_encoded.columns:
            new_df_encoded[col] = 0
    
    new_df_encoded = new_df_encoded[feature_columns]
    
    predicted_price = model.predict(new_df_encoded)
    return predicted_price[0]

if __name__ == "__main__":
    try:
        df = load_and_prepare_data('E:\OOP\AI_Lab\Lab9\house_prices_dataset.csv')
        X, y = prepare_features(df)
        
        model = train_and_evaluate(X, y)
        
        new_house = {
            'SquareFootage': 1500,
            'Bedrooms': 3,
            'Bathrooms': 2,
            'HouseAge': 10,
            'Neighborhood': 'Suburban'
        }
        
        predicted_price = predict_price(model, new_house, X.columns)
        print(f"\nPredicted price for new house: ${predicted_price:,.2f}")
        
    except FileNotFoundError:
        print("Error: Could not find the data file.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
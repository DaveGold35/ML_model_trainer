from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import pandas as pd
import joblib
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

def train_linear_regression(data_path, upload_folder):
    # load and prepare the dataset
    df = pd.read_csv(data_path)
    
    # Assuming the target variable is in the last column
    X = df.iloc[:, :-1].values
    y = df.iloc[:, -1].values
    
    # Split the dataset into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state=42)
    
    # Initialize and train the linear regression model
    model_filename = 'linear_regression_model.joblib'
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    # Predict on the testing set
    y_pred = model.predict(X_test)
    
    # Calculate the mean squared error as a simple performance metric
    mse = mean_squared_error(y_test, y_pred)
    model_path = os.path.join(upload_folder, model_filename)
    joblib.dump(model, model_path)
    
    return model_filename, mse, model, X, y

def visualize_training(model, X, y, upload_folder):
    plt.scatter(X, y)
    plt.plot(X, model.predict(X), color='red')
    plt.xlabel('X')
    plt.ylabel('y')
    plt.title('Linear Regression Fit')
    plot_filename = 'linear_regression_fit.png'
    plot_path = os.path.join(upload_folder, plot_filename)
    plt.savefig(plot_path)
    plt.close()
    return plot_filename
<font size = 30>Machine Learning Trainer</font>

This project is being built to create a no-code solution to train and test simple data-science related machine learning models.

<font size = 5> FEATURES </font>

Currently only linear regression models are supported, but the project is being built to support other models in the future. The project is also being built to support multiple datasets and models at the same time.

<font size = 5> SETUP </font>

This project is built using python 3.11.5. 

It is also recommended to use a virtual environment to run this project.

To install virtual environment, run the following command in the terminal:

```bash
pip install virtualenv
```

To create a virtual environment, run the following command in the terminal:

```bash
python3 -m venv <env_name>
```

Once the virtual environment is create, activate it by running the following command in the terminal:

```bash
source <env_name>/bin/activate
```

To install the required packages, run the following command in the terminal:

```bash
pip install -r requirements.txt
```

<font size = 5> USAGE </font>

To demonstrait its useage, a file named linear_regression_test_data.csv has been included in the repository, which contains a simple dataset to train a linear regression model.

In order to use the project, run the following command in the terminal from the project root directory:

```bash
python3 app.py
```

This will start the application and provide a link to the web interface that is being hosted locally.  The link will appear in the terminal (on port 5000) and to open the interface, simply copy and paste the link into your web browser, or in VS Code use command/control click on the link to open.

<font size = 5> FUTURE WORK </font>

The project is currently in its early stages and is being built to support more models and datasets. The project is also being built to support more features such as data preprocessing, model evaluation, and model visualization. 
# InsideOut-Backend

This is the backend repository for the InsideOut project, providing a robust and scalable architecture for risk assessment in medical procedures. The backend is built using Python and Flask, leveraging a range of powerful libraries for data processing, machine learning, and database management.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Technologies](#technologies)
- [Environment Variables](#environment-variables)
- [Contributing](#contributing)
- [License](#license)

## Installation

### Prerequisites

- Python 3.12
- pip

### Setup

1. Clone the repository:
    ```bash
    git clone https://github.com/InsideOut-Shenkar/InsideOut-Backend.git
    cd InsideOut-Backend
    ```

2. Create a virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Set up the environment variables:
    - Create a `.env` file in the root directory.
    - Add the following [environment variables](#environment-variables):
      

## Usage

1. Start the Flask server:
    ```bash
    flask run
    ```

2. The backend will be running on `http://127.0.0.1:5000/`.

3. Access various endpoints to interact with the system.


## Technologies

The project utilizes the following libraries and tools:

- **[numpy](https://numpy.org/)**: For numerical computations.
- **[pandas](https://pandas.pydata.org/)**: For data manipulation and analysis.
- **[matplotlib](https://matplotlib.org/)**: For plotting and data visualization.
- **[seaborn](https://seaborn.pydata.org/)**: For statistical data visualization.
- **[scikit-learn](https://scikit-learn.org/stable/)**: For machine learning algorithms.
- **[xgboost](https://xgboost.readthedocs.io/)**: For gradient boosting models.
- **[graphviz](https://graphviz.gitlab.io/)**: For visualizing decision trees.
- **[flask](https://flask.palletsprojects.com/)**: As the web framework.
- **[python-dotenv](https://github.com/theskumar/python-dotenv)**: For managing environment variables.
- **[joblib](https://joblib.readthedocs.io/)**: For saving and loading machine learning models.
- **[pymysql](https://pypi.org/project/PyMySQL/)**: For MySQL database connectivity.
- **[tensorflow](https://www.tensorflow.org/)**: For deep learning models.
- **[imblearn](https://imbalanced-learn.org/)**: For handling imbalanced datasets.
- **[boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)**: For AWS services interaction.
- **[flask-cors](https://flask-cors.readthedocs.io/)**: For handling Cross-Origin Resource Sharing (CORS).

---

## Environment Variables

The following environment variables are required for the application:

- `DATABASE_URL`: The database connection URL.
- `SECRET_KEY`: A secret key used for securing sessions.
- `DB_HOST`: The hostname or IP address of your database server.
- `DB_USER`: The username for the database connection.
- `DB_PASSWORD`: The password for the database connection.
- `DB_NAME`: The name of the database to connect to.
- `DB_PORT`: The port number for the database connection.
- `AWS_ACCESS_KEY_ID`: AWS Access Key ID for accessing AWS services.
- `AWS_SECRET_ACCESS_KEY`: AWS Secret Access Key for accessing AWS services.

You need to set these variables in your `.env` file before running the application.

---

## Authors

- **Lidia Polyakov** - [GitHub](https://github.com/lidiaPolyakov)
- **Asaf Bai** - [GitHub](https://github.com/asafbaibekov)
- **Ibraheem Alnakib** - [GitHub](https://github.com/abrahhem)


## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.
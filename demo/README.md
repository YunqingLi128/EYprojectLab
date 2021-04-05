# Dashboard tool for the FFIEC102 forms

## Prerequisite
1. Install [Python3](https://www.python.org/downloads/) (version >= 3.7)
2. Install [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html)
3. Install [npm](https://www.npmjs.com/get-npm)

## Installing dependencies:
* On macOS and Linux:
  * Flask backend
    ```Shell
    # working on demo folder
    cd EYProjectLab/demo
    
    # Creating and activating virtual environment
    python3 -m venv env
    source env/bin/activate
  
    # Install dependencies
    python3 -m pip install . --upgrade
    ```
  * Vue frontend
    ```Shell
    cd frontend/projectlabdemp
    npm install
    ```

* On Windows:
  * Flask backend
    ```Shell
    # working on demo folder
    cd EYProjectLab\demo
      
    # Creating and activating virtual environment
    py -3 -m venv env
    .\env\Scripts\activate
      
    # Install dependencies
    py -3 -m pip install . --upgrade
    ```
  * Vue frontend
    ```Shell
    cd frontend\projectlabdemp
    npm install
    ```

## Running the app:
### 1. Running backend and frontend separately
 * Start the backend
   * On macOS and Linux:
     ```Shell
     # Working on demo folder
     cd EYProjectLab/demo
          
     # Reactivating virtual environment
     source env/bin/activate
          
     # Set flask environment variables
     export FLASK_APP=backend
     export FLASK_ENV=development
          
     # Run the backend server
     flask run
     ```
   * On Windows:
     ```Shell
     # Working on demo folder
     cd EYProjectLab\demo
      
     # Reactivating virtual environment
     .\env\Scripts\activate
      
     # Set flask environment variables
     set FLASK_APP=backend
     set FLASK_ENV=development
      
     # Run the backend server
     flask run
     ```
   
   In Flask, the default port is `5000`, and API url will be `http://127.0.0.1:5000/api_name`
    
 * Start the frontend:
   ```Shell
   cd frontend/projectlabdemp
   npm run dev
   ```
   Point your web browser to http://localhost:8080/#/home, initial data for six major banks will be automatically download if first use.
### 2. Shell script starting:
 * On macOS and Linux:
   ```Shell
   # Working on demo folder
   cd EYProjectLab/demo
      
   # run the bash script
   bash dashboardRun
   ```
 * On windows:
   ```Shell
   # Working on demo folder
   cd EYProjectLab\demo
      
   # run the batch file
   dashboardRun.bat
   ```  

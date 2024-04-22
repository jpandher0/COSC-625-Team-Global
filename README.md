client:

    cd client
   
	# This command installs all the dependencies listed in the package.json file of client project. These dependencies are necessary for the client-side application to run correctly.
	 npm install
	 
	 # Runs the development server for the client application. This command usually starts a local server which automatically reloads if you make changes to the code. The exact behavior depends on how the dev script is defined in package.json.
    npm run dev

mancala-fastapi(python3.7.9):
    cd mancala-fastapi
	
	# Create a Python virtual environment named venv in the current directory. A virtual environment is an isolated environment for Python projects which allows you to manage dependencies separately for each project.
    python -m venv venv
	
	#Activates the virtual environment. After activation, any Python or pip commands will use the packages and settings from this virtual environment rather than the global Python environment.
    venv\Scripts\activate

    # This command installs all the Python libraries listed in the requirements.txt file. These libraries are dependencies for your FastAPI application.
    pip install -r requirements.txt
	
	#uvicorn will install it to provide services for FastAPI applications
    # pip install uvicorn
	
	# numpy is a popular library for numerical operations
    # pip install numpy
	
    # pip install fastapi

	#Use Uvicorn to run FastAPI applications. main:app tells Uvicorn to find the object main.py specified in the file app to run as an ASGI application. The --reload flag causes the server to automatically restart when a code change is detected.
    uvicorn main:app --reload
	
	


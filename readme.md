# Bank Snap

This is an app I created to analysis bank statements. It is developed using python flask and wrapped around electron through the [electron-flask project](https://github.com/matbloch/electron-flask). 

## Demo


![Bank-Statement-Analysis-Google-C](https://user-images.githubusercontent.com/47830627/100645907-4216b600-3335-11eb-8e50-2667702b5a6a.gif)


## How to run the application
**Start app**
- Windows: `.\node_modules\.bin\electron .`
- Mac OS/Linux: `./node_modules/.bin/electron .`

**Start app with globally installed electron**

- `electron .`

**Run the app through your web browser**

- Start Flask server manually: `python web_app/run_app.py`


## Development history of the application

I started this project at my second year of my cs degree. I didn't put in much thoughts into its architecture and scalability when I started. 
I just used whatever technologies I know at the time to build in the functionalities I want. 
The project first started as a python flask website with a MySQL database which now that I looked back at it, it is honestly a terrible design choice but it was also a nice opportunity for me to learn why that is not the best idea ever.

Now with the attempts to make this more of a user-friendly application, I have wrapped the project with electron that allows it to run as a desktop application and move the database to SQLite so that it can become a standalone desktop application.
from app import create_app
from db_helper import checkIfTableExist, createAnalysisedTable

# NOTE: Explicitly import configuration so that PyInstaller is able to find and bundle it
import config

application = create_app("config.DevelopmentConfig")

if __name__ == "__main__":
    if len(checkIfTableExist()) != 1:
        createAnalysisedTable()
        print("new analysised table created")
    application.run(port=4040)

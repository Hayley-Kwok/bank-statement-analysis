from app import create_app

# NOTE: Explicitly import configuration so that PyInstaller is able to find and bundle it
import config

application = create_app("config.DevelopmentConfig")

if __name__ == "__main__":
    application.run(port=4040)

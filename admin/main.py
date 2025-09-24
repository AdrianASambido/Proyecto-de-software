from dotenv import load_dotenv
import os
from src.web import create_app

load_dotenv()

if __name__ == "__main__":
    env = os.getenv("FLASK_ENV", os.getenv("APP_ENV", "development"))
    app = create_app(env=env)
    app.run(debug=(env == "development"))

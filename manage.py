# -*- coding: utf-8 -*-
import os
from app import create_app
from dotenv import load_dotenv


# Load dotenv in the base root
root_path = os.path.dirname(os.path.abspath(__file__))
load_dotenv(dotenv_path=os.path.join(root_path, '.env'), override=True)

app = create_app()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

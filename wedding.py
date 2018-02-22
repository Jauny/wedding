import os

from dotenv import load_dotenv
from app import app


if __name__ == "__main__":
    if os.environ.get('ENVIRONMENT') is not 'PRODUCTION':
        dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
        load_dotenv(dotenv_path)

    import pdb; pdb.set_trace()
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

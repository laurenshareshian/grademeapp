from app import app
from createdatabase import createdatabase

import sys
import os

if __name__ == '__main__':
    if '--reset' in sys.argv:
        with app.app_context():
            createdatabase(app.config['DATABASE_URL'])
            print('Database recreated')
    else:
        host = os.environ.get('HOST', '0.0.0.0')
        port = int(os.environ.get('PORT', 5000))
        app.run(host=host, port=port)

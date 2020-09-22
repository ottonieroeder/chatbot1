import os

from django.core.wsgi import get_wsgi_application
from dotenv import load_dotenv
from django.conf import settings

if not settings.DEBUG:
    project_folder = os.path.expanduser('~/isabot.pythonanywhere.com')
    load_dotenv(os.path.join(project_folder, '.env'))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "chatbot.settings")

application = get_wsgi_application()

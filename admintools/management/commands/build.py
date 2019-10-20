from django.core.management import BaseCommand
from django.conf import settings
from django.core import management
import os
import subprocess


class Command(BaseCommand):
    help = 'デプロイ環境用のビルドコマンド。'

    def add_arguments(self, parser):
        pass
        # parser.add_argument('opt1', help='必須オプション')
        # parser.add_argument('--opt2', help='任意オプション')

    def handle(self, *args, **options):
        cwd = os.path.join(settings.BASE_DIR, 'frontend')
        env = os.environ.copy()
        env['PUBLIC_URL'] = settings.BASE_URL
        subprocess.run('yarn install', shell=True, cwd=cwd, env=env)
        subprocess.run('yarn build', shell=True, cwd=cwd, env=env)
        management.call_command('collectstatic', '--noinput')

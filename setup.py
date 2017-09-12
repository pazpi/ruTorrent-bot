# setup.py
from distutils.core import setup

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(name='ruTorrent-bot',
      version='0.1',
      description='telegram bot that add torrent to a ruTorrent interface',
      author='@pazpi, @martinotu',
      author_email='pasettodavide@gmail.com',
      url='https://www.github.com/pazpi/ruTorrent-bot',
      # install_requires=requirements,
      packages=['python-telegram-bot', 'requests'],
      )

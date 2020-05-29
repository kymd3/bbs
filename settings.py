# coding: UTF-8

import os
from os.path import join,dirname
dotenv_path = join(dirname(__file__), '.env')
from dotenv import load_dotenv
load_dotenv(dotenv_path, verbose = True)

host= os.environ.get('db_host')
user= os.environ.get('db_user')
passwd= os.environ.get('db_pass')
db= os.environ.get('db_name')

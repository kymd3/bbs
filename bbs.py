#!/usr/bin/python3
# coding: utf-8


import io
import cgi
import sys
import cgitb
cgitb.enable()

import textwrap

sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')

version = sys.version
path = sys.path
import MySQLdb

 

form = cgi.FieldStorage()


    
def print_headers():
    print( "Content-type: text/html; charset=utf-8" )
    print( "" )
    

def print_html():
    source = textwrap.dedent( """<!DOCTYPE html>
    <html lang="ja">
    <head>
    <meta http-equiv="content-type" charset="utf-8">
    <meta http-equiv="Pragma" content="no-cache">
    <meta http-equiv="Cache-Control" content="no-cache">
    <meta http-equiv="Expires" content="0">
    <link rel="stylesheet" href="bbs.css" type="text/css">
    </head>
    <body>
    <div class="header">
    <p><font size="5">ひとこと掲示板</font></p>
    </div>
     <div class="main">
      <form method="POST"><p><font size="4">ニックネーム</font></p><input type="textbox" name="u_name" maxlength="20" /><br>
      <p><font size="4">ひとことメッセージ</p><textarea name="message" /></textarea>
      <button type="submit">送信</button>
     </form>
     <form method="POST">
      <p><font size="4">メッセージ検索</font></p><textarea name="search"></textarea>
      <button type="submit">検索</button>
     </form>
     </div>
     <hr class="border"/>""" )
    print( source )

def print_messages():
    sql = "select * from message_list"
    cursor.execute( sql )

    rows = cursor.fetchall()
    for row in rows:
        source = textwrap.dedent( """
        <div class="text-box1">
          <p>{name}</p>
          <p>{message}</p>
          <p align="right">{date}</p>
        </div>
        </body>
        </html>
        """ ).format( name = row[ 'name' ],
            message = row[ 'message' ],
            date = row[ 'date' ]
        )
        print( source )

def insert_method():
    sql = 'insert into message_list ( name, message ) values ( %s, %s )'
    cursor.execute( sql, ( name, message ) )
    connection.commit()
    

def search_method():
    sql =  "select * from  message_list where message like '%%%s%%'" 
    cursor.execute( sql % search )
    rows = cursor.fetchall()
    for row in rows:
        source = textwrap.dedent( """
        <div class="text-box1">
          <p>{name}</p>
          <p>{message}</p>
          <p align="right">{date}</p>
        </div>
        </body>
        </html>
        """ ).format( name = row[ 'name' ],
            message = row[ 'message' ],
            date = row[ 'date' ])
        print( source )    

def main():

    print_headers()
    print_html()
    
    global name, message, search
    name = form.getvalue('u_name')
    message = form.getvalue('message')
    search = form.getvalue('search')

    global connection, cursor

    connection = MySQLdb.connect(
    host='localhost',
    user='root',
    passwd='ChaPan0022!',
    db='message_list',
    charset='utf8')
    cursor = connection.cursor( MySQLdb.cursors.DictCursor )

    if 'u_name' in form and 'message' in form:
        print( '送信されました' )
        insert_method()
        print_messages()

    elif 'search' in form:
        search_method()
   
    else:
        print_messages()
     
    cursor.close()
    connection.close()
	    

if __name__ == "__main__":
    main()

#!/usr/bin/python3
# coding: utf-8

import io
import cgi
import sys
import textwrap
import settings
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')
version = sys.version
path = sys.path
import MySQLdb

form = cgi.FieldStorage()

def print_headers():
    print( "Content-type: text/html; charset=utf-8" )
    print( "" )
    

def print_html():
    source = textwrap.dedent( """
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
      <form post_method="POST"><p><font size="4">ニックネーム</font></p><input type="textbox" name="u_name" maxlength="20" /><br>
      <p><font size="4">ひとことメッセージ</p><textarea name="post" /></textarea>
      <input type="hidden" name="post_method" value="post">
      <button type="submit">送信</button>
     </form>
     <form post_method="POST">
      <p><font size="4">メッセージ検索</font></p><textarea name="search" value=""></textarea>
      <input type="hidden" name="post_method" value="search">
      <button type="submit">検索</button>
     </form>
     </div>
     <hr class="border"/>""" )
    print( source )

def print_posts():
    sql = "select * from post_list order by post_id desc"
    cursor.execute( sql )

    rows = cursor.fetchall()
    for row in rows:
        source = textwrap.dedent( """
        <div style="padding-bottom:0px;margin-bottom:0px;" class="text-box1">
          <span>{name}</span>
          <span>{post}</span><br>
          <span align="right">{date}</span>
           <form  method="reply" action="">
           <input type="hidden" name="reply_method" value="reply_method">
           <input type="hidden" name="post_id" value="{post_id}">
           <input type="submit" value="返信する" style="background-color:#00ced1;color:#fff;display:inline-block;" ></form>
           <form  method="post" action="">
           <input type="hidden" name="post_method" value="delete_id">
           <input type="hidden" name="delete_id" value="{delete_id}">
           <input  type="submit"  value="削除" style="background-color:#00ced1;color:#fff;display:inline-block;" ></form></div>
        </body>
        """ ).format( name = row[ 'name' ],
            post = row[ 'post' ],
            delete_id = row[ 'post_id' ],
            date = row[ 'date' ],
            post_id = row[ 'post_id' ] )
        print( source )

def post_methods():
    if 'u_name' in form and 'post' in form:
        print( '<p>送信されました</p>' )
        sql = 'insert into post_list ( name, post ) values ( %s, %s )'
        cursor.execute( sql, ( name, post ) )
        connection.commit()
        print_posts()

    elif 'search' in form:
        search_method()

    elif 'delete_id' in form:
        print('<p>削除されました</p>')    
        sql = 'delete from post_list where post_id=%s'
        cursor.execute( sql, ( delete_id, ) )
        connection.commit()
        print_posts()

    else:
        print('<p>入力してください</p>')
        print_posts()

def search_method():
    print( search + ' 検索結果' )
    sql =  "select * from  post_list where post like '%%%s%%'" 
    cursor.execute( sql % search )
    rows = cursor.fetchall()
    for row in rows:
        source = textwrap.dedent( """
        <div class="text-box1">
          <p>{name}</p>
          <p>{post}</p>
          <p align="right">{date}</p>
        </div>
        </body>
        </html>
        """ ).format( name = row[ 'name' ],
            post = row[ 'post' ],
            date = row[ 'date' ])
        print( source ) 

def print_reply_html():
    sql =  "select * from  post_list where post_id=%s" 
    cursor.execute( sql, ( post_id, ) )
    rows = cursor.fetchall()
    for row in rows:
        source = textwrap.dedent( """
    <div style="padding:5px;margin:5px 200px 5px 5px;border:1px solid #00ced1;border-radius:4px;">
     <span style="display:inline">{name}</span>
     <span style="display:inline">{post}</span><br>
     <span>{date}</span>
    </div>
    <div>
    <p><font size="3">この投稿に返信する</font></p>
     <form method="POST">
     <p style="padding-bottom:0px;margin-bottom:0px;"><font size="4">ニックネーム</font></p>
     <input type="hidden" name="reply_method" value="">
     <input type="textbox" name="replyer_name" maxlength="20" /><br>
     <p style="padding-bottom:0px;margin-bottom:0px;"><font size="4">メッセージ</p><textarea name="reply_message" /></textarea>
     <button style="background-color:#00ced1;color:#fff;" type="submit">送信</button></div></form>
    <hr style="border-bottom-style:solid;border-color:#00ced1;" />
      """ ).format(name = row[ 'name' ],
        post = row[ 'post' ],
        date = row[ 'date' ])
        print( source )


def print_replies():
    sql = "select * from reply order by reply_id desc"
    cursor.execute( sql )
    rows = cursor.fetchall()
    for row in rows:
        source = textwrap.dedent( """
        <div class="text-box1">
          <p>{replyer_name}</p>
          <p>{post}</p>
          <p align="right">{date}</p>
           <form  method="post" action="">
           <input type="hidden" name="reply_method" value="delete_reply">
           <input type="hidden" name="delete_reply" value="{reply_id}">
           <input type="submit" value="削除" style="background-color:#00ced1;color:#fff;" ></form></div>
        </body>
        """ ).format( replyer_name = row[ 'replyer_name' ],
            post = row[ 'post' ],
            date = row[ 'date' ],
            reply_id = row[ 'reply_id' ] )

        print( source )

#def reply_methods():
 #   if 'replyer_name' in form and 'reply_message' in form:
  #      print( '<p>送信されました</p>' )
   #     sql = 'insert into reply( post_id, replyer_name, post ) values( %s, %s, %s )'
    #    cursor.execute( sql, ( post_id, replyer_name, reply_message ) )
     #   connection.commit()
      #  print_replies()

#    else:
 #       print_replies()  
  #      print('222')

def main():
    
    print_headers()
    print( """<!DOCTYPE html><html lang="ja">""" )
    global name, post, search, delete_id, post_id, replyer_name, reply_message, reply_id
    name = form.getvalue('u_name')
    post = form.getvalue('post')
    search = form.getvalue('search')
    delete_id = form.getvalue('delete_id')
    post_id = form.getvalue('post_id')
    replyer_name = form.getvalue('replyer_name')
    reply_message = form.getvalue('reply_message')
    reply_id = form.getvalue('delete_reply')
    print(form)
    global connection, cursor

    connection = MySQLdb.connect(
    host= settings.host,
    user= settings.user,
    passwd= settings.passwd,
    db= settings.db,
    charset='utf8')
    cursor = connection.cursor( MySQLdb.cursors.DictCursor )

    if 'post_method' in form:
        print_html()
        post_methods()

    elif 'reply_method' in form:
        if 'replyer_name' in form and 'reply_message' in form:
            print_reply_html()
            print( '<p>送信されました</p>' )
            sql = 'insert into reply( post_id, replyer_name, post ) values( %s, %s, %s )'
            cursor.execute( sql, ( post_id, replyer_name, reply_message ) )
            connection.commit()
            print_replies()

        elif 'delete_reply' in form:
            print_reply_html()
            print('<p>削除されました</p>')    
            sql = 'delete from reply where reply_id=%s'
            
            cursor.execute( sql, ( reply_id, ) )
            connection.commit()
            print_replies()
            
        else:
            print_reply_html()
            print_replies()

    else:
        print_html()
        print_posts()

    print( "</html>" )
    cursor.close()
    connection.close()
   
if __name__ == "__main__":
    main()


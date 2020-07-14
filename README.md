
# bbs

ひと言掲示板

## Description

CGIで実行する、Python + MySQL + HTML + CSS のひと言掲示板です。

## Usage

メッセージの投稿、検索、削除をすることができます。
<img width="951" alt="2020-06-06 (2)" src="https://user-images.githubusercontent.com/65747602/83969919-ab30ea00-a90d-11ea-8bd7-af9000107a84.png">

返信機能を追加しました。
<img width="932" alt="2020-06-06 (3)" src="https://user-images.githubusercontent.com/65747602/84474280-8b127980-acc5-11ea-95f8-cef5649a3961.png">

## Install
  
for Ubuntu  
1. pipのインストール  
```bash
$ sudo apt install python3-pip
```
2. Mysqlclientのインストール  
```bash
$ sudo apt-get install python-pip python-dev libmysqlclient-dev
```

for Centos7
1. python3-develのインストール
```bash
$ sudo yum install python3-devel
```
2. Mysqlclientのインストール
```bash
$ sudo pip3 install mysqlclient
```
## About .env.example

以下を自分の情報に書き換えてください。
```bash
db_host=[yourhost]
db_user=[yourname]
db_pass=[yourpass]
db_name=[yourdb]
```
私のコードではファイル名を .env にする必要があります。

import urllib
import json
import sys
import codecs
import urllib.request
import pprint
import datetime
import time
import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials

api_tag = 'https://alis.to/api/search/articles?tag=%E8%87%B3%E9%AB%98%E3%81%AE%E2%97%8B%E2%97%8B%E3%83%86%E3%82%B9%E3%83%88'
#APIの/search/articlesのパラメーターに「至高の○○テスト」と入力後、queryをtagに変換

url_tag = urllib.request.urlopen(api_tag)
article_tag = json.loads(url_tag.read().decode("utf-8"))
article_id = [article_tags.get('article_id') for article_tags in article_tag]
print(article_id)
#article_idのみ取り出す

user_id = [article_tags.get('user_id') for article_tags in article_tag]
print(user_id)
#user_idのみ取り出す

api_article_id = ["https://alis.to/api/articles/"+article_id for article_id in article_id]
print(api_article_id)
#article_idのapiを使いやすい形にする

user_id_info_api = ["https://alis.to/api/users/"+user_ids+"/info" for user_ids in user_id]
#user_idのapiを使いやすい形にする

user_id_info = [json.loads(urllib.request.urlopen(user_id_info_apis).read().decode("utf-8")) for user_id_info_apis in user_id_info_api]
user_display_name = [user_id_infos.get('user_display_name') for user_id_infos in user_id_info]
for user_display_names in user_display_name:
    print(user_display_names)
    #user_display_nameを取り出す

likes_api = ["https://alis.to/api/articles/"+article_ids+"/likes" for article_ids in article_id]
#likesのapiを使いやすい形にする

like = [json.loads(urllib.request.urlopen(likes_apis).read().decode("utf-8")) for likes_apis in likes_api]
pprint.pprint(like)
likes_count = [likes.get('count') for likes in like]
for likes_counts in likes_count:
    print(likes_counts)
    #like数を取り出す

articles_body = [json.loads(urllib.request.urlopen(api_article_ids).read().decode("utf-8")) for api_article_ids in api_article_id]
pprint.pprint(articles_body)
#記事の本文を取りだす

def get_block(text, start_text, end_text):
    new_texts = []
    for split_text in text.split(start_text):
        if split_text.find(end_text):
            new_texts.append(split_text.split(end_text)[0])
    return new_texts
for articles_bodys in articles_body:
    texts = get_block(articles_bodys.get("body"), "<blockquote>", "</blockquote>")
    print(texts[1])
    #<blockquote>内の文を取り出す

for (article_ids, user_ids) in zip(article_id, user_id):
    article_url="https://alis.to/"+str(user_ids) +"/articles/"+ str(article_ids)
    print(article_url)
    #記事URLを取り出す



scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
#googleスプレッドシートに書き込む準備をする

credentials = ServiceAccountCredentials.from_json_keyfile_name('gspread-sample-31b5a8f7ef13.json', scope)
gc = gspread.authorize(credentials)
workbook = gc.open_by_key('1u3J0zY9CXc4zHPtcrWDeGNkazFaCPVmObpu3CWVVvXA')
#googleスプレッドシートを指定する

worksheet = workbook.sheet1
#sheet1を選択する

u = 1
for articles_bodys in articles_body:
    texts = get_block(articles_bodys.get("body"), "<blockquote>", "</blockquote>")
    u = u+1
    worksheet.update_cell(u, 1, texts[1])
    #スプレッドシートのA列に<blockquote>内の文を書き込む

v = 1
for (article_ids, user_ids) in zip(article_id, user_id):
    article_url="https://alis.to/"+str(user_ids) +"/articles/"+ str(article_ids)
    v = v+1
    worksheet.update_cell(v, 3, article_url)
    #スプレッドシートのC列に記事URLを書き込む

w = 1
for user_display_names in user_display_name:
    w=w+1
    worksheet.update_cell(w, 4, user_display_names)
    #スプレッドシートのD列にユーザー名を書き込む

y = 1
for likes_counts in likes_count:
    y=y+1
    worksheet.update_cell(y, 5, likes_counts)
    #スプレッドシートのE列にLike数を書き込む

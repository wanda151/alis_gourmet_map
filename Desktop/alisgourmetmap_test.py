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
url_tag = urllib.request.urlopen(api_tag)
article_tags = json.loads(url_tag.read().decode("utf-8"))
article_ids = [article_tag.get('article_id') for article_tag in article_tags]
#article idを取り出す

user_ids = [article_tag.get('user_id') for article_tag in article_tags]
#user id を取り出す

api_article_ids = ["https://alis.to/api/articles/"+article_id for article_id in article_ids]
#article_idをAPIで取り出しやすい形にする

user_id_info_apis = ["https://alis.to/api/users/"+user_id+"/info" for user_id in user_ids]
#user_id_infoをAPIで取り出しやすい形にする

user_id_infos = [json.loads(urllib.request.urlopen(user_id_info_api).read().decode("utf-8")) for user_id_info_api in user_id_info_apis]
#/users/{user_id}/infoを取り出す

user_display_names = [user_id_info.get('user_display_name') for user_id_info in user_id_infos]
#user_display_name　を取り出す

likes_apis = ["https://alis.to/api/articles/"+article_id+"/likes" for article_id in article_ids]
#likes_apiをAPIで取り出しやすい形にする
likes = [json.loads(urllib.request.urlopen(likes_api).read().decode("utf-8")) for likes_api in likes_apis]
likes_counts = [like.get('count') for like in likes]
#Like数　を取り出す

articles_bodys = [json.loads(urllib.request.urlopen(api_article_id).read().decode("utf-8")) for api_article_id in api_article_ids]
def get_block(text, start_text, end_text):
    if not text.find(start_text) >= 0:
        return []
    new_texts = []
    for split_text in text.split(start_text):
        if split_text.find(end_text) >= 0:
            new_texts.append(split_text.split(end_text)[0])
    return new_texts




scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
#googleスプレッドシートに書き込む準備をする

credentials = ServiceAccountCredentials.from_json_keyfile_name('gspread-sample-31b5a8f7ef13.json', scope)
gc = gspread.authorize(credentials)
workbook = gc.open_by_key('1u3J0zY9CXc4zHPtcrWDeGNkazFaCPVmObpu3CWVVvXA')
#googleスプレッドシートを指定する

worksheet = workbook.sheet1
#sheet1を選択する

for i, articles_body in enumerate(articles_bodys):
    texts = get_block(articles_body.get("body"), "<blockquote>", "</blockquote>")
    texts = [text for text in texts if text.find("〒") >= 0]
    for text in texts:
        texts = get_block(articles_body.get("body"), "企画名", "<br>料理ジャンル")
    project_name_str = str(texts)
    print(project_name_str.replace(":", "").replace("：", "").replace("['","").replace("']",""))
    project_name = project_name_str.replace(":", "").replace("：", "").replace("['","").replace("']","")
    worksheet.update_cell(i+2, 1, project_name)
    #スプレッドシートのA列に企画名を書き込む

for i, articles_body in enumerate(articles_bodys):
    texts = get_block(articles_body.get("body"), "<blockquote>", "</blockquote>")
    texts = [text for text in texts if text.find("〒") >= 0]
    for text in texts:
        texts = get_block(articles_body.get("body"), "料理ジャンル", "<br>店名")
    food_Genre_str = str(texts)
    print(food_Genre_str.replace(":", "").replace("：", "").replace("['","").replace("']",""))
    food_Genre = food_Genre_str.replace(":", "").replace("：", "").replace("['","").replace("']","")
    worksheet.update_cell(i+2, 2, food_Genre)
    #スプレッドシートのB列に記事URLを書き込む
    
for i, articles_body in enumerate(articles_bodys):
    texts = get_block(articles_body.get("body"), "<blockquote>", "</blockquote>")
    texts = [text for text in texts if text.find("〒") >= 0]
    for text in texts:
        texts = get_block(articles_body.get("body"), "店名：", "<br>住所")
    store_name_str = str(texts)
    print(store_name_str.replace(":", "").replace("：", "").replace("['","").replace("']",""))
    store_name = store_name_str.replace(":", "").replace("：", "").replace("['","").replace("']","")
    worksheet.update_cell(i+2, 3, store_name)
    #スプレッドシートのC列に店名を書き込む

for i, articles_body in enumerate(articles_bodys):
    texts = get_block(articles_body.get("body"), "<blockquote>", "</blockquote>")
    texts = [text for text in texts if text.find("〒") >= 0]
    for text in texts:
        texts = get_block(articles_body.get("body"), "<br>住所：", "</blockquote>")
        texts = [text for text in texts if text.find("〒") >= 0]
    location_str = str(texts)
    print(location_str.replace(":", "").replace("：", "").replace("['","").replace("']",""))
    location = location_str.replace(":", "").replace("：", "").replace("['","").replace("']","")
    worksheet.update_cell(i+2, 4, location)
    #スプレッドシートのD列に住所を書き込む


for i, (article_id, user_id) in enumerate(zip(article_ids, user_ids)):
    article_url="https://alis.to/"+str(user_id) +"/articles/"+ str(article_id)
    worksheet.update_cell(i+2, 5, article_url)
    #スプレッドシートのE列に記事URLを書き込む

for i, user_display_name in enumerate(user_display_names):
    worksheet.update_cell(i+2, 6, user_display_name)
    #スプレッドシートのF列にユーザー名を書き込む


for i, likes_count in enumerate(likes_counts):
    worksheet.update_cell(i+2, 7, likes_count)
    #スプレッドシートのG列にLike数を書き込む

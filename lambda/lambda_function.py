import json, os, requests

TOKEN = os.environ['TOKEN']
ITEM_ID = os.environ['ITEM_ID']

def get_tags():
  per_page=100
  sort_type="count" # countで記事数順、nameで名前順
  base_url = 'https://qiita.com/api/v2/tags?page={page}&per_page={per_page}&sort={sort_type}'
  headers = {'Authorization': 'Bearer {}'.format(TOKEN)}

  tags = []
  for i in range(5):
    try:
      url = base_url.format(page=i+1,per_page=per_page,sort_type=sort_type)
      response = requests.get(url, headers=headers)
      response.raise_for_status()
      tags.extend(json.loads(response.text))
    except Exception as e:
      break

  return tags

def patch_item(tags):
  url = 'https://qiita.com/api/v2/items/{id}'.format(id=ITEM_ID)
  headers = {
    'Authorization': 'Bearer {}'.format(TOKEN),
    'Content-Type': 'application/json'
  }

  try:
    response = requests.get(url)
    response.raise_for_status()
    item_base = json.loads(response.text)

    item = {
      "coediting": item_base['coediting'],
      "private": item_base['private'],
      "tags": item_base['tags'],
      "title": item_base['title']
    }

    row = "| {0} | ![{1}]({2}) | [{1}](https://qiita.com/tags/{1}) | {3} | {4} |\n"
    tagstring = ""
    for i, tag in enumerate(tags):
      tagstring += row.format(i+1,tag['id'],tag['icon_url'],tag['items_count'],tag['followers_count'])

    tagstring2 = ""
    tags.sort(key=lambda x: -x['followers_count'])
    for i, tag in enumerate(tags):
      tagstring2 += row.format(i+1,tag['id'],tag['icon_url'],tag['items_count'],tag['followers_count'])

    item['body']="""
# 記事数上位500タグ一覧
記事数が多い500タグの一覧です。1時間ごとに自動更新しています。

- [記事数順](#記事数順)
- [フォロワー数順](#フォロワー数順)

## 記事数順

| # | アイコン | タグ | 記事数 | フォロワー数 |
| :---: | :---: | :--- | ---: | ---: |
{}

## フォロワー数順

| # | アイコン | タグ | 記事数 | フォロワー数 |
| :---: | :---: | :--- | ---: | ---: |
{}
""".format(tagstring,tagstring2)

    response = requests.patch(url, headers=headers, json=item)
    response.raise_for_status()
  except Exception as e:
    # do noting
    print(e)
  
  pass

def lambda_handler(event, context):
  # APIからデータを取得
  tags = get_tags()
  patch_item(tags)

  return {
    'statusCode': 200,
    'body': json.dumps('Hello from Lambda!')
  }

if __name__ == '__main__':
  # ローカルで実行する用
  lambda_handler(None,None)

# 利用Python全网抓取文字信息

数据库`spider_text_message`：
---

网站表：`website`

| 字段名              | 数据类型| 长度 | 说明       | 描述 |
|:-------------------|:-------|:----|:----------|:----|
|website_id|||| 网站id |
|web_name|||| 网站名|
|domain||||域名|


存储文字信息表：`text_info`

| 字段名              | 数据类型| 长度 | 说明       | 描述 |
|:-------------------|:-------|:----|:----------|:----|
|title||||标题|
|url||||文章url|
|charset||||编码|
|release_time||||发布时间|
|author||||作者|
|keyword||||关键字|
|content||||文章内容|
|website_id||||网站id|

爬取url的表： `urls`

| 字段名              | 数据类型| 长度 | 说明       | 描述 |
|:-------------------|:-------|:----|:----------|:----|
|url||||网址|
|depth||||层级|
|status||||状态（0 todo, 1 doing, 2 done, 3 exception）|
|description||||url描述|
|website_id||||网站id|




 
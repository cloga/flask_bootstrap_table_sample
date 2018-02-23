from flask import render_template
import datetime
from flask import request
from flask import Flask
import json
import pandas as pd
# 导入配置文件
from congfig import ES_BASE_URL
# es 接口
from elasticsearch import Elasticsearch

es = Elasticsearch(ES_BASE_URL, sniff_on_start=True)
today = str(datetime.date.today())

app = Flask(__name__)


"""
A example for creating a Table that is sortable by its header
"""

app = Flask(__name__)
data0 = [{
  "name": "bootstrap-table",
  "commits": "10",
  "attention": "122",
  "uneven": "An extended Bootstrap table"
},
 {
  "name": "multiple-select",
  "commits": "288",
  "attention": "20",
  "uneven": "A jQuery plugin"
}, {
  "name": "Testing",
  "commits": "340",
  "attention": "20",
  "uneven": "For test"
}]
# other column settings -> http://bootstrap-table.wenzhixin.net.cn/documentation/#column-options
columns0 = [
  {
    "field": "name", # which is the field's name of data key 
    "title": "name", # display as the table header's name
    "sortable": True,
  },
  {
    "field": "commits",
    "title": "commits",
    "sortable": True,
  },
  {
    "field": "attention",
    "title": "attention",
    "sortable": True,
  },
  {
    "field": "uneven",
    "title": "uneven",
    "sortable": True,
  }
]


#jdata=json.dumps(data)

# 定义展示的字段
columns = [
  {
    "field": "proxy_timestamp", # which is the field's name of data key 
    "title": "proxy_timestamp", # display as the table header's name
    "sortable": True,
  },
  {
    "field": "user_id",
    "title": "user_id",
    "sortable": True,
  },
  {
    "field": "cuid",
    "title": "cuid",
    "sortable": True,
  },
  {
    "field": "suid",
    "title": "suid",
    "sortable": True,
  },
  {
    "field": "more",
    "title": "more",
    "sortable": True,
  }
]


@app.route('/')
def index():
    return render_template("table.html",
      data=data0,
      columns=columns0,
      title='Flask Bootstrap Table')

@app.route('/get_es_data', methods=['POST', 'GET'])
def get_beijing_sdk_real_data():
    # curl -X POST -H "Content-Type:application/x-www-form-urlencoded"  -d '{"query":{"bool":{"must":[{"match_all":{}}],"must_not":[],"should":[]}},"from":0,"size":10,"sort":[],"aggs":{}}' 'http://10.1.23.190:9200/beijing_sdk_realtime-2018-02-07/_search'
    # 日期控件
    # 几个文本输入框填写搜索es条件
    # es部分搜索使用统配符模式，默认的match是单词匹配
    # query = request.args.get('q')
    if request.method == 'GET':
        # get需要做处理不然无法访问这个页面
        query_name_contains = {'query': {'wildcard': {'user_id': '*'}}, 'size': 100}

    else:
        query = request.form['user_id']
        query_name_contains = {'query': {'wildcard': {'user_id': '*' + query + '*'}}, 'size': 100}
    results = es.search(index="beijing_sdk_realtime-"+today, body=query_name_contains)
    results = [json.loads(r['_source']['@message']) for r in results['hits']['hits']]
    # return results_df.to_html()
    return render_template("table.html",
      data=results,
      columns=columns,
      title='北京sdk实时日志查询')




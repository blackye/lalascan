#-*- coding: utf-8 -*-
import math
import re
#import pymongo
import datetime
from scanui import app
#from scanui.models import NmapTask
#from scanui.tasks import celery_nmap_scan
from flask import Flask,Blueprint, render_template, request, redirect, url_for,session,g,flash
from flask.ext.login import login_required, current_user
from celery.states import READY_STATES
import json

'''
# setting:
MONGODB_SERVER = 'localhost'
MONGODB_PORT = 27017
MONGODB_W_DB = 'wooyun'
MONGODB_H_DB = 'hackerone'
MONGODB_B_DB = 'bug'
MONGODB_COLLECTION_BUGS = 'bug_list'
MONGODB_COLLECTION_HACKERONE_BUGS = 'hackerone_list'
MONGODB_COLLECTION_WOOYUN_BUGS = 'wooyun_list'
MONGODB_COLLECTION_DROPS = 'wooyun_drops'
ROWS_PER_PAGE = 20
'''

# monogodb connection string
'''
connection_string = "mongodb://%s:%d" % (
    app.config['MONGODB_SERVER'], app.config['MONGODB_PORT'])
content = {'by_wooyun_bugs':
           {'mongodb_collection': app.config[
               'MONGODB_COLLECTION_WOOYUN_BUGS'], 'template_html': '/handleui/search_wooyun_bugs.html'},
           'by_hackerone_bugs':
           {'mongodb_collection': app.config[
               'MONGODB_COLLECTION_HACKERONE_BUGS'], 'template_html': '/handleui/search_hackerone_bugs.html'},
			      'by_bobao_bugs':
           {'mongodb_collection': app.config[
               'MONGODB_COLLECTION_BUGS'], 'template_html': '/handleui/search_bobao_bugs.html'}
           }
def get_search_regex(keywords, search_by_html):
    keywords_regex = {}
    kws = [ks for ks in keywords.strip().split(' ') if ks != '']
    field_name = 'html' if search_by_html else 'title'
    if len(kws) > 0:
        reg_pattern = re.compile('|'.join(kws), re.IGNORECASE)
        # keywords_regex[field_name]={'$regex':'|'.join(kws)}
        keywords_regex[field_name] = reg_pattern

    return keywords_regex
def search_wooyun_mongodb(keywords, page, content_search_by, search_by_html):
    client = pymongo.MongoClient(connection_string)
    db = client[app.config['MONGODB_W_DB']]
    keywords_regex = get_search_regex(keywords, search_by_html)
    collection = db[content[content_search_by]['mongodb_collection']]
    # get the total count and page:
    total_rows = collection.find(keywords_regex).count()
    #print total_rows
    total_page = int(
        math.ceil(total_rows / (app.config['ROWS_PER_PAGE'] * 1.0)))
    page_info = {'current': page, 'total': total_page,
                 'total_rows': total_rows, 'rows': []}
    # get the page rows
    if total_page > 0 and page <= total_page:
        row_start = (page - 1) * app.config['ROWS_PER_PAGE']
        cursors = collection.find(keywords_regex)\
            .sort('datetime', pymongo.DESCENDING).skip(row_start).limit(app.config['ROWS_PER_PAGE'])
        for c in cursors:
            c['datetime'] = c['datetime'].strftime('%Y-%m-%d')
            if 'url' in c:
                urlsep = c['url'].split('//')[1].split('/')
                c['url_local'] = '%s-%s.html' % (urlsep[1], urlsep[2])
	    #print "c:%s" % c
            page_info['rows'].append(c)
    client.close()
    #
    return page_info
def search_hackerone_mongodb(keywords, page, content_search_by, search_by_html):
    client = pymongo.MongoClient(connection_string)
    db = client[app.config['MONGODB_H_DB']]
    keywords_regex = get_search_regex(keywords, search_by_html)
    collection = db[content[content_search_by]['mongodb_collection']]
    # get the total count and page:
    total_rows = collection.find(keywords_regex).count()
    print "total:%d" % total_rows
    total_page = int(
        math.ceil(total_rows / (app.config['ROWS_PER_PAGE'] * 1.0)))
    page_info = {'current': page, 'total': total_page,
                 'total_rows': total_rows, 'rows': []}
    # get the page rows
    if total_page > 0 and page <= total_page:
        row_start = (page - 1) * app.config['ROWS_PER_PAGE']
        cursors = collection.find(keywords_regex).limit(app.config['ROWS_PER_PAGE'])
       
        for c in cursors:
	    #print "c:%s" % c
            page_info['rows'].append(c)
    #print "tttt%s" % page_info['rows'][2]
    client.close()
    #
    return page_info
def search_bobao_mongodb(keywords, page, content_search_by, search_by_html):
    client = pymongo.MongoClient(connection_string)
    db = client[app.config['MONGODB_B_DB']]
    keywords_regex = get_search_regex(keywords, search_by_html)
    collection = db[content[content_search_by]['mongodb_collection']]
    # get the total count and page:
    total_rows = collection.find(keywords_regex).count()
    #print total_rows
    total_page = int(
        math.ceil(total_rows / (app.config['ROWS_PER_PAGE'] * 1.0)))
    page_info = {'current': page, 'total': total_page,
                 'total_rows': total_rows, 'rows': []}
    # get the page rows
    if total_page > 0 and page <= total_page:
        row_start = (page - 1) * app.config['ROWS_PER_PAGE']
        cursors = collection.find(keywords_regex).limit(app.config['ROWS_PER_PAGE'])
       
        for c in cursors:
	    #print "c:%s" % c
            page_info['rows'].append(c)
    client.close()
    #
    return page_info
def get_wooyun_total_count():
    client = pymongo.MongoClient(connection_string)
    db = client[app.config['MONGODB_W_DB']]
    collection_wooyun = db[app.config['MONGODB_COLLECTION_WOOYUN_BUGS']]
    total_wooyun_bugs = collection_wooyun.find().count()
    db = client[app.config['MONGODB_H_DB']]
    collection_hackerone = db[app.config['MONGODB_COLLECTION_HACKERONE_BUGS']]
    total_hackerone_bugs = collection_hackerone.find().count()
    db = client[app.config['MONGODB_B_DB']]
    collection_bobao = db[app.config['MONGODB_COLLECTION_BUGS']]
    total_bobao_bugs = collection_bobao.find().count()
    client.close()

    return (total_wooyun_bugs, total_hackerone_bugs,total_bobao_bugs)
'''


app = Flask(__name__)
app.config.from_object(__name__)
appmodule = Blueprint('scan', __name__, url_prefix='/cloudsafe/scan')

@appmodule.route('/results', methods=['GET', 'POST'])
@login_required
def nmap_index():
    return render_template('/handleui/results.html')

@appmodule.route('/results/', methods=['GET', 'POST'])
@login_required
def results():
    return render_template('/handleui/results.html')

'''
@appmodule.route('/scan_index/', methods=['GET', 'POST'])
@login_required
def scan():
    _nmap_tasks = NmapTask.find(user_id=current_user.id)
    return render_template('/handleui/scan.html', tasks = _nmap_tasks)
'''

@appmodule.route('/infaq/',methods=['GET', 'POST'])
@login_required
def infaq():
    return render_template("/handleui/faq.html")
	
	
@appmodule.route('/inabout/', methods=['GET', 'POST'])
@login_required
def inabout():
    return render_template("/handleui/about.html")
	
@appmodule.route('/queue/', methods=['GET', 'POST'])
@login_required
def queue():
    return render_template("/handleui/queue.html")
@appmodule.route('/scan_test/', methods=['GET', 'POST'])
@login_required
def scan_test():
    return render_template("/handleui/scan_test.html")
	
@appmodule.route('/bug_index/', methods=['GET', 'POST'])
@login_required
def bug_index():
    total_wooyun_bugs,total_hackerone_bugs,total_bobao_bugs = get_wooyun_total_count()
    return render_template("/handleui/bug_index.html",total_wooyun_bugs=total_wooyun_bugs, total_hackerone_bugs=total_hackerone_bugs, total_bobao_bugs=total_bobao_bugs,title=u'公开漏洞搜索')		

'''
@appmodule.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    keywords = request.args.get('keywords')
    page = int(request.args.get('page', 1))
    search_by_html = True if 'true' == request.args.get(
        'search_by_html', 'false').lower() else False
	
    content_search_by = request.args.get('content_search_by')
    if content_search_by == 'by_wooyun_bugs':
	if page < 1:
	    page = 1
    #
	page_info = search_wooyun_mongodb(
	keywords, page, content_search_by, search_by_html)
    #
	return render_template(content[content_search_by]['template_html'], keywords=keywords, page_info=page_info, search_by_html=search_by_html, title=u'搜索结果-乌云公开漏洞搜索')
    elif content_search_by == 'by_hackerone_bugs':
	if page < 1:
	    page = 1
    #
	page_info = search_hackerone_mongodb(
	keywords, page, content_search_by, search_by_html)
    #
	return render_template(content[content_search_by]['template_html'], keywords=keywords, page_info=page_info, search_by_html=search_by_html, title=u'搜索结果-Hackerone公开漏洞搜索')
    elif content_search_by == 'by_bobao_bugs':

	    if page < 1:
	        page = 1
	    page_info = search_bobao_mongodb(
	keywords, page, content_search_by, search_by_html)
    #
	    return render_template(content[content_search_by]['template_html'], keywords=keywords, page_info=page_info, search_by_html=search_by_html, title=u'搜索结果-360播报公开漏洞搜索')
	
@appmodule.route('/tasks', methods=['GET', 'POST'])
@login_required
def nmap_tasks():
    scantypes = [ "-sT", "-sT", "-sS", "-sA", "-sW", "-sM",
            "-sN", "-sF", "-sX", "-sU" ]

    if request.method == "POST":
        
        if 'targets' in request.form:
            targets = request.form["targets"]
        else:
            abort(401)

        options = ""
        scani = int(request.form['scantype']) if 'scantype' in request.form else 0
        if 'ports' in request.form and len(request.form['ports']):
            portlist = "-p " + request.form['ports']
        else:
            portlist = ''
        noping = '-P0' if 'noping' in request.form else ''
        osdetect = "-O" if 'os' in request.form else ''
        bannerdetect = "-sV" if 'banner' in request.form else ''
        options = "{0} {1} {2} {3} {4}".format(scantypes[scani],
                                                  portlist,
                                                  noping,
                                                  osdetect,
                                                  bannerdetect)
        _celery_task = celery_nmap_scan.delay(targets=str(targets),
                                              options=str(options))
        NmapTask.add(user_id=current_user.id, task_id=_celery_task.id)
        return redirect(url_for('scan.nmap_tasks'))

    _nmap_tasks = NmapTask.find(user_id=current_user.id)
  
    return render_template('/handleui/scan.html', tasks=_nmap_tasks)
    #_nmap_tasks = str(_nmap_tasks)
    #print type(_nmap_tasks)
    #return _nmap_tasks

@appmodule.route('/jsontasks', methods=['GET', 'POST'])
@login_required
def nmap_tasks_json():
    _nmap_tasks = NmapTask.find(user_id=current_user.id)
    # print _nmap_tasks
    _jtarray = []
    for _ntask in _nmap_tasks:
        tdict = {'id': _ntask.id,
                 'status': _ntask.status,
                 'ready': 0}
        if _ntask.result and 'done' in _ntask.result:
            tdict.update({'progress': float(_ntask.result['done'])})
        elif _ntask.result and 'report' in _ntask.result:
            tdict.update({'progress': 100})
        else:
            tdict.update({'progress': 0})
        if _ntask.status in READY_STATES:
            tdict.update({'ready': 1})
        _jtarray.append(tdict)

    return json.dumps(_jtarray)


@appmodule.route('/report/<report_id>/')
@login_required
def nmap_report(report_id):
    _report = None
    if report_id is not None:
        _report = NmapTask.get_report(task_id=report_id)
    return render_template('/handleui/nmap_report.html', report=_report)
'''

@appmodule.route('/compare')
@login_required
def nmap_compare():
    return render_template('/handleui/nmap_compare.html')


@appmodule.route('/test', methods=['GET', 'POST'])
#@login_required
def test():
    username = "{0}:{1} {2}".format(current_user.id, current_user.username, type(unicode(current_user.id)))
#    if request.method == 'POST':
#        username = request.args.get('username')
    return render_template('test.html', username=username)

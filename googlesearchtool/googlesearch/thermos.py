from datetime import datetime
from flask import Flask, render_template, request, flash, redirect, url_for
import sys
import json
import ast
import os
import googlesearch as lido


from forms import BookmarkForm

app = Flask(__name__)
app.config['SECRET_KEY'] = '~t\x86\xc9\x1ew\x8bOcX\x85O\xb6\xa2\x11kL\xd1\xce\x7f\x14<y\x9e'

bookmarks = []
newstitles = []


def store_bookmark(url, description):
    bookmarks.append(dict(
        url=url,
        description=description,
        user="reindert",
        date=datetime.utcnow()
    ))


def new_bookmarks(num):
    return sorted(bookmarks, key=lambda bm: bm['date'], reverse=True)[:num]


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', new_bookmarks=new_bookmarks(5))


@app.route('/add', methods=['GET', 'POST'])
def add():

    form = BookmarkForm()
    newRecordList = []
    if form.validate_on_submit():


        website = form.website.data







        recordList = lido.start(website)


        print "/////////////////////////////////////////////////////////////"
        print type(recordList)
        #recordList = mc.findTwitterHandles(company.strip(), website.strip())
        result={}

        try:
            if isinstance(recordList,str):
                result["error"]=recordList
                newRecordList.append(result)

            else:

                for b in recordList:
                    result["company"]=b[0]
                    result["comp"]=b[1]
                    result["title"]=b[2]
                    result["source"]=b[3]
                    result["date"]=b[4]
                    result["website"]=b[5]
                    result["desc"]=b[6]


                    print "------------------------------"
                    '''
                    print type(b.encode('ascii', 'ignore'))
                    result = json.loads(b)
                    print type(result)
                    '''
                    newRecordList.append(result)

        except Exception,e:
            print str(e)
            pass


        print ("Came here: something is working")

        return render_template('tweets.html', news_results=newRecordList)




    return render_template('add.html', form=form)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
    # sys.stdout = open('logfortoday.log', 'w')
    app.run(debug=True,host='localhost', port=5000)
    #app.run(debug=True,port=9000)

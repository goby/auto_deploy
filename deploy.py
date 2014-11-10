#!/usr/bin/env python

from flask import *
from git import Repo
import os

app = Flask(__name__)

@app.route('/deploy', methods=['POST'])
def test():
    try:
        # Local code repo 
        target = '/home/www-data/test/new/'
        event = request.headers['X-Github-Event']
        sign  = request.headers['X-Hub-Signature']
        print request.headers['X-Github-Delivery']
        message = request.data
        if event != 'push' or sign != 'sha1=a4e2e31d909ab4a3b318880d2bd0150aaa594dc6':
            return 'Invalid Signature', 401

        pushobject = json.loads(message)
        if pushobject['ref'] != 'refs/heads/master':
            return 'Invalid Branch.', 400

        version = pushobject['head_commit']['id']

        clone_url = pushobject['repository']['clone_url']
        if os.path.exists(target):
            repo = Repo(target)
            remote = repo.remotes.origin
            remote.pull()
        else:
            repo = Repo.clone_from(clone_url, '/home/www-data/test/new')
    except Exception, e:
        return str(e)
    return 'success', 200

# if __name__ == '__main__':
#    app.run(host='0.0.0.0', port=2014, debug=True)

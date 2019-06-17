import base64
import github
from github import Github
from github import InputGitTreeElement
import datetime
import os
import time


user = "git username"
password = "git password"
#p = datetime.datetime.now().date()
#date = str(datetime.datetime.strptime(str(p),'%Y-%m-%d').strftime('%m%d%Y'))
g = Github(user,password)
repo = g.get_user().get_repo('oldtweets')
datesince = "2010-01-01"
date_time_obj = datetime.datetime.strptime(datesince, '%Y-%m-%d').date()
datenow= datetime.datetime.now().date()
while date_time_obj<datenow:
    date_time_obj_tomorrow = date_time_obj+datetime.timedelta(days=1)
    print("today:"+str(date_time_obj))
    print("tomorrow:"+str(date_time_obj_tomorrow))
    os.system("GetOldTweets3 --querysearch \"#cisco lang:en\" --since "+str(date_time_obj)+" --until "+str(date_time_obj_tomorrow)+" --maxtweets 200")
    file_list = [
    'oldtweet/cisco_'+str(date_time_obj)+'.csv'
    ]

    file_names = [
    'cisco_'+str(date_time_obj)+'.csv'
    ]
    commit_message = ' '+str(date_time_obj)+'tweet csv files added'
    master_ref = repo.get_git_ref('heads/master')
    master_sha = master_ref.object.sha
    base_tree = repo.get_git_tree(master_sha)
    element_list = list()
    for i, entry in enumerate(file_list):
        with open(entry) as input_file:
            data = input_file.read()
        if entry.endswith('.png'):
            data = base64.b64encode(data)
        element = InputGitTreeElement(file_names[i], '100644', 'data2', data)
        element_list.append(element)


    tree = repo.create_git_tree(element_list, base_tree)

    parent = repo.get_git_commit(master_sha)
    commit = repo.create_git_commit(commit_message, tree, [parent])
    master_ref.edit(commit.sha)
    print("push success")
    date_time_obj = date_time_obj+datetime.timedelta(days=1)

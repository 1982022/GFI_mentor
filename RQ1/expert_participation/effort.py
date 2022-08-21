import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator
from scipy import stats
import csv


def draw_two_dimensional_distribution(data, x_label, y_label):    

    sns.set(style="darkgrid")
    sns.set(color_codes=True)
    df = pd.DataFrame(data, columns=[x_label, y_label])
    df = df[(np.abs(stats.zscore(df[x_label])) < 3)]
    df = df[(np.abs(stats.zscore(df[y_label])) < 3)]
    sns.jointplot(x=x_label, y=y_label, data=df, kind="hist")
    print(len(set(['%s_%s'%(i[0],i[1]) for i in df.values])))
    plt.savefig("distribution.png")

if __name__ == '__main__':
    comments = {} # issue_id: comment_id, user_id, created_at, type, identity
    file1 = open("../issue_commenter/issue_commenter.csv")
    #issue_id,user_id,comment_id,created_at,identity
    csv_reader = csv.reader(file1)
    next(csv_reader)
    for row in csv_reader:
        if row[0] not in comments.keys():
            if row[2] != '':
                comments[row[0]] = [[row[2], row[1], row[3], 'issue_comment', row[4]]]
        else:
            if row[2] != '':
                comments[row[0]].append([row[2], row[1], row[3], 'issue_comment', row[4]])
    file1.close()
    file2 = open("../issue_pr_commenter/pr_commenter.csv")
    #issue_id,issue_created_at,pr_id,user_id,comment_id,created_at,identity
    csv_reader = csv.reader(file2)
    next(csv_reader)

    for row in csv_reader:
        if row[0] not in comments.keys():
            if row[4] != '':
                comments[row[0]] = [[row[4], row[3], row[5], 'issue_pr_comment', row[6]]]
        else:
            if row[4] != '':
                comments[row[0]].append([row[4], row[3], row[5], 'issue_pr_comment', row[6]])

    file2.close()
    file3 = open("../commit_commenter/commit_commenter.csv")
    #issue_id,issue_created_at,commit_sha,commit_id,user_id,comment_id,created_at,identity
    csv_reader = csv.reader(file3)
    next(csv_reader)
    for row in csv_reader:
        if row[0] not in comments.keys():
            if row[5] != '':
                comments[row[0]] = [[row[5], row[4], row[6], 'issue_commit_comment', row[7]]]
        else:
            if row[5] != '':
                comments[row[0]].append([row[5], row[4], row[6], 'issue_commit_comment', row[7]])
    file3.close()

    #the number of GFI comments associated with issues and pr or commits
    comments_issue_PRandCommit = {}
    #the number of GFI comments from newcomers and experts
    comments_newcomer_expert = {}
    #the number of GFI commenters associated with issues and pr or commits
    commenters_issue_PRandCommit = {}
    #the number of GFI commenters from newcomers and experts
    commenters_newcomer_expert = {}

    file4 = open("../../GFI_selection/GFI_closed.csv")
    csv_reader = csv.reader(file4)
    next(csv_reader)

    for row in csv_reader:
        if row[0] not in comments.keys():
            comments_issue_PRandCommit[row[0]] = [0,0]
            comments_newcomer_expert[row[0]] = [0,0]
            commenters_issue_PRandCommit[row[0]] = [0,0]
            commenters_newcomer_expert[row[0]] = [0,0]
        else:  
            num_issue_comments = 0
            num_PRandCommit_comments = 0
            num_newcomer_comments = 0
            num_expert_comments = 0
            num_issue_commenters = set()
            num_PRandCommit_commenters = set()
            num_newcomer_commenters = set()
            num_expert_commenters = set()
            comments_ = comments[row[0]]
            for item in comments_:               
                if item[3] == 'issue_pr_comment' or item[3] == 'issue_commit_comment':
                    num_PRandCommit_comments += 1
                    num_PRandCommit_commenters.add(item[1])
                if item[3] == 'issue_comment':
                    num_issue_comments += 1
                    num_issue_commenters.add(item[1])
                if item[4] == 'newcomers':
                    num_newcomer_comments += 1
                    num_newcomer_commenters.add(item[1])
                if item[4] == 'expert':
                    num_expert_comments += 1
                    num_expert_commenters.add(item[1])
            comments_issue_PRandCommit[row[0]] = [num_issue_comments, num_PRandCommit_comments]
            comments_newcomer_expert[row[0]] = [num_newcomer_comments, num_expert_comments]
            commenters_issue_PRandCommit[row[0]] = [len(num_issue_commenters), len(num_PRandCommit_commenters)]
            commenters_newcomer_expert[row[0]] = [len(num_newcomer_commenters), len(num_expert_commenters)]
    file4.close()

    comments = []
    for item in comments_newcomer_expert.values():
        if item[0] != 0:
            comments.append([int(item[0]), 'newcomer', 'comments'])
        if item[1] != 0:
            comments.append([int(item[1]), 'expert', 'comments'])
    for item in commenters_newcomer_expert.values():
        if item[0] != 0:
            comments.append([int(item[0]), 'newcomer', 'commenters'])
        if item[1] != 0:
            comments.append([int(item[1]), 'expert', 'commenters'])


    df_comment_commenter = pd.DataFrame(comments,
                columns=['Number', 'Identity', 'Type'])
    
    df_comment_commenter = df_comment_commenter[(np.abs(stats.zscore(df_comment_commenter['Number'])) < 3)]

    print(df_comment_commenter)

    plt.figure().set_size_inches(8,4)
    ax2 = sns.violinplot(x="Type", y="Number", data=df_comment_commenter, palette=['darkorange','dodgerblue'], hue="Identity")
    #ax2.set(yscale="log")
    plt.grid(ls= '-.')
    y_major_locator = MultipleLocator(4)
    ax2.yaxis.set_major_locator(y_major_locator)
    plt.savefig("effort.png")


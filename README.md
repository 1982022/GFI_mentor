# Data and scripts for the paper

This repository contains the main data and scripts used in 'Is It Enough to Recommend Tasks to Newcomers?Understanding Mentoring on Good First Issues‘

## GFI_selection

The folder `GFI_selection` contains the following files.

- **select_GFI.py**

  This file is mainly used for:

  - Select non-forked repos with gfi label from tables: `repo_labels` and `projects`. Save the GFI lable ID and repo ID to `repo_GFIlabel.csv`.
  - Select each GFI in the above repos from tables: `repo_labels`, `projects`, `issue_labels`. Save the issue ID, lable ID, and repo ID to `repo_GFI_distribution.csv`.
  - Get the top 1% repositories with most GFIs ( i.e., #*GF Is* ⩾ 30), including 964 repositories and 68,652 GFIs, saved as `repo_GFI_top1percent.csv`.
  - Filter the GFIs that are still in progress and only keep the closed GFIs, saved as `GFI_closed.csv`.

- **repo_GFIlabel.csv**: Non-forked repos with GFI label.

- **repo_GFI_distribution.csv**: GFI in non-forked repos with GFI label.

- **repo_GFI_top1percent.csv**: The top 1% repositories with most GFIs.

- **GFI_closed.csv**: the closed GFIs.

- **issue_labels.csv**:The issue_labels table in the database.

## RQ1

The folder `RQ1` contains the following files.

**`commit_commenter`**

- **commit_commenter_exp_calculate.py**

  This file is used for:

  - **find_expert:**Calculate the commenters experience who left comments on the related commits of the GFIs.
  - **judge_newcomer:**Determine whether the user is a newcomer.
  - **find_commit_id：**Find the commit ID and SHA.

  The results are stored in `commit_commenter.csv`

**`expert_participation`**

- **effort.py**

  This file is mainly used for counting the number of newcomers and experts Involved in GFI resolution and their comments.

- **expert.py**

  This file is mainly used for looking for GFIs that involve both experts and newcomers, the results are saved in `newcomer_expert_GFIs.csv`.

**`issue_commenter`**

- **issue_commenter_exp_calculate.py**

  This file is mainly used for finding the user identity for each comment.

- **issue_commenter_exp_distribution.py**

  This file is mainly used for counting the number of experts and newcomers participating in each issue and the number of comments made by the experts and newcomers respectively.

- **issue_commenter_exp_distribution.csv**

  Details of each issue, including creation time, number of comments, number of comments created by commenters with different identities, number of commenters with different identities, etc.

- **issue_commenter_exp_distribution1.csv**

  The number of participants with different identities in each issue.

- **issue_commenter_exp_distribution2.csv**

  The URL corresponding to the issue and the type of user participating in the comment.

- **issue_commenter.csv**

  Details of each comment, including the corresponding issue, reviewer ID and identity, creation time, etc.

**`issue_pr_commenter`**

This folder is related to the PullRequest（PR).

- **get_issue_pr**

  This folder stores the script and result data used to find the issue associated PR.

- The rest of the documents count information about PR comments based on the results above, including the number of participating users with different identities.

**`response_time`**

This folder is used to **calculate the proportion of expert response time to total time**

Firstly, put the comments of issue, PR and commit together, and then calculate the corresponding time of the experts in the three kinds of comments.

## RQ2

The files in this directory analyzed 74,201 users' relationship network and the Mentorship structures of 964 repos.

- **picc**

  Mentorship Structures diagrams for about  275 communities.

- **sample**

  Using the data above, we performed an open picture sorting and calculate the graph metrics and project-related metrics for each network.

## RQ3

- **codebook**

  We illustrate the topics discussed by newcomers and experts during the GFI resolution process, combining the quotations of their comments and survey results. We extract 32 codes belonging to two themes and ten sub-themes.

## RQ4

**`Find issue closed by newcomer`**

- **find_GFI_closed_by_newcomer.py**

  For commits that actually modify the code, determine whether the author of the commit is new to the repository. The results are stored in `issue_cbn.csv`.

**`Get some attributes`**

- **repo_attri.py**

  Get attributes of repository via ghtorrent database: authors, commits, issues, month.

- **get_stars.py**

  Get stars of repository via github api.

- **count_label.py**

  Get the number of labels of the issue.

- **get_issue_time.py**

  Get Duration of the issue.

- **comment_info.py**

  Get the comment attributes of the issue.

After all the attributes of the issue are counted, results are stored in: `Q1_info_1020+1020.csv`.This includes 1,020 issues that were solved by newcomers, and 1,020 issues that were not solved by newcomers.

**`Get commit information`**

The SHA value carried in the Closed Events of the issue can determine the commit which closed the issue.

To find the commit that actually solves the issue, we need to make sure that the commit actually made changes to the code, and the author of the changes is the person who solved the issue. So we get the commit information.

- **find_sha.py**

  This file is used for: find sha value. The results are stored in `all_sha.csv`.

- **find_repo_url.py**

  This file is used for: get repo_name and repo_url in the database. The results are stored in `all_sha.csv`

- **clone.py**

  This file is used for: clone The repository via the `repo_url`.

- **git_log.py**

  This file is used for: for each issue, open the issue repository and use git-log to find commit information. The results are stored in `commit.txt`.

- **get_commit_info.py**

  This file is used for: get the number of files and code modified by commit. The results are stored in `commit_info.csv`.

**`RQ4_1_solved and RQ4_2_longterm`**

Two folders contain: RQ4 two problem model fitting scripts and model results.

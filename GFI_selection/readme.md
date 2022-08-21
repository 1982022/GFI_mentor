# Code file:

## select_GFI.py

This file is mainly used for:

### select non-forked repos with gfi label

Select non-forked repos with gfi label from tables:**repo_labels** and **projects**. Save the GFI lable ID and repo ID to **repo_GFIlabel.csv**

### GFI distribution

Select each GFI in the above repos from tables: **repo_labels**,**projects**, **issue_labels**.Save the issue ID, lable ID, and repo ID to **repo_GFI_distribution.csv**

### obatin top 1% repo_id and GFI_id

Get the top 1% repositories with most GFIs (i.e., #*GF Is* ⩾ 30),including 964 repositories and 68,652 GFIs,saved as **repo_GFI_top1percent.csv**.

### choose closed issue

Filter the GFIs that are still in progress and only keep the closed GFIs,saved as **GFI_closed.csv**

# Data file:

**repo_GFIlabel.csv:**non-forked repos with GFI label

**repo_GFI_distribution.csv**:GFI in non-forked repos with GFI label

**repo_GFI_top1percent.csv**:the top 1% repositories with most GFIs 

**GFI_closed.csv**:the closed GFIs

**issue_labels.csv**:The issue_labels table in the database
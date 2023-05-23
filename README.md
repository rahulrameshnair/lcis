# Brightway

### Versions

- Brightway 2.4.2
  - bw2calc 1.8.1
  - bw2data 3.6.5
  - bw2io 0.8.8
  - bw2analyzer 0.1.0
  - bw_migrations 0.1
- ecoinvent: 3.9.1
- python: 3.9

## Getting started

This project hosts all the brightway related files for importing, data analysis, and visualization using
python. The examples used are from the case of the DLR Impuls projekt ALICIA.

## Add your files

- classify files according to their functions. Each folder holds files for a specific funcion. For example, the "imports" folder has all the files required for importing
LCI as excel files
- files can be added as jupyter notebooks and/or python scripts. Modular code structure is preferred for reuse on code and pattern
level. where a jupyter notebook does the main calculation/analyses, with scripts, classes or functions defined for executing the supporting
calculations or references (repeatable code blocks)
- each jupyter notebook must include a "logic" shortly detailing the the purpose of the notebook and its external dependencies.
- please declare variables in human readable forms and comment wherever necessary to ease future references



## Folder structure

- imports - for importing LCI databases as excel files
- graphing - for plotting the the LCA results from activity browser using python
- databases - contains sample LCI databases used by Alicia (will be updated over the course of the project)

## Repo maintainers/contact
Rahul Ramesh Nair, Joana Albano, Rahn Antonia.
## Gitlab collaboration links

- [ ] [Invite team members and collaborators](https://docs.gitlab.com/ee/user/project/members/)
- [ ] [Create a new merge request](https://docs.gitlab.com/ee/user/project/merge_requests/creating_merge_requests.html)
- [ ] [Automatically close issues from merge requests](https://docs.gitlab.com/ee/user/project/issues/managing_issues.html#closing-issues-automatically)
- [ ] [Enable merge request approvals](https://docs.gitlab.com/ee/user/project/merge_requests/approvals/)
- [ ] [Automatically merge when pipeline succeeds](https://docs.gitlab.com/ee/user/project/merge_requests/merge_when_pipeline_succeeds.html)






















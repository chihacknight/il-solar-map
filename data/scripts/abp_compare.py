import csv

current_file = "../raw/ilabp.csv"
previous_file = "../raw/ilabp_previous.csv"

def get_projects(file):
    project_dict = {}
    with open(file) as ilsfa_file:
        projects = csv.DictReader(ilsfa_file)
        for project in projects:
            if project['Project Size AC kW'] != '':
                project['Project Size AC kW'] = float(project['Project Size AC kW'].replace(',', '').strip())
            project_dict[project['Application ID']] = project
    return project_dict

current_projects = get_projects(current_file)
previous_projects = get_projects(previous_file)

for project_id, project in current_projects.items():
    if project_id in previous_projects:
        previous_project = previous_projects[project_id]
        if project['Project Size AC kW'] != previous_project['Project Size AC kW']:
            print(project_id, project['Project Size AC kW'], previous_project['Project Size AC kW'])
    else:
        print(project_id, "is NEW")
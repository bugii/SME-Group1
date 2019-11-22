import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from analysis import load_obj

projects = []

for folder in os.listdir('repositories'):
    project = load_obj('repositories/' + folder + '/project.pkl')
    projects.append({
        'name': project.name,
        'updated': project.last_updated,
        'nr microservices': len(project.microservices),
        'microservices': project.microservices,
        'depends on': project.depends_on
    })

df = pd.DataFrame(projects)

df = df.sort_values(by="updated")
df = df.set_index('updated')

df_avg = df.resample('W').mean()

print(df.head(10))
print(df.tail(10))

df.plot(marker='.', linestyle='None', alpha=0.5, subplots=True)

df_avg.plot(marker='.', linestyle='None', alpha=0.5, subplots=True)


project_sizes = []

for project in projects:
    date = project['updated']
    nr_services = 0
    total_size = 0
    for micro in project['microservices']:
        nr_services += 1
        if micro['size'] != -1 and micro['size'] is not None:
            total_size += micro['size']

    try:
        avg_size = total_size/nr_services/1000000
    except ZeroDivisionError:
        avg_size = 0

    project_sizes.append({
        "date": date,
        "# services": nr_services,
        "total size": total_size/1000000,
        "avg size": avg_size
    })

df_size = pd.DataFrame(project_sizes)
df_size = df_size.set_index("date")
print(df_size.head())

df_size.plot(marker='.', linestyle='None', alpha=0.5, subplots=True)

plt.show()





import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from get_services_size import load_obj

projects = []

for folder in os.listdir('repositories'):
    project = load_obj('repositories/' + folder + '/project.pkl')

    size = 0
    for microservice in project.microservices:
        # this is only temporal, can be deleted once all was run
        if microservice['size'] is not None:
            size += microservice['size']
        else:
            size += 0

    # this is only temporal, can be delted once all was run
    if len(project.microservices) is not 0:
        nr_microservices = len(project.microservices)
    else:
        nr_microservices = 1

    projects.append({
        'name': project.name,
        'created': project.created,
        'updated': project.last_updated,
        'duration': project.last_updated - project.created,
        'nr microservices': nr_microservices,
        'size': size,
        'average size': size/nr_microservices,
        'depends on': project.depends_on,
        'contributors': len(project.contributors),
        'language': project.language
    })



'''
Last updated
'''

df = pd.DataFrame(projects)
df['year'] = df['updated'].dt.year
df = pd.melt(df, id_vars=['year'], value_vars=['nr microservices', 'size', 'average size', 'depends on'])
g = sns.FacetGrid(df, row='variable', sharey=False, aspect=1.5)
g.map(sns.boxplot, 'year', 'value', palette="Set3")

g.savefig('results/last_updated.png')


'''
Influence of language
'''

df2 = pd.DataFrame(projects)
df2['year'] = df2['updated'].dt.year
# print(df2['language'].value_counts())
languages = ['JavaScript', 'PHP', 'Java', 'Python']
df2 = df2[df2['language'].isin(languages)]
df2 = pd.melt(df2, id_vars=['year', 'language'], value_vars=['nr microservices', 'size', 'average size', 'depends on'])
g2 = sns.FacetGrid(df2, row='variable', sharey=False, aspect=1.5, legend_out=True)
g2.map(sns.boxplot, 'year', 'value', 'language', palette="Set3").add_legend()

g2.savefig('results/language.png')


'''
Project Duration
'''

df3 = pd.DataFrame(projects)
df3['duration'] = df3['duration'].dt.days
df3 = pd.melt(df3, id_vars=['duration'], value_vars=['nr microservices', 'size', 'average size', 'depends on'])
g3 = sns.lmplot(data=df3, x='duration', y='value', row='variable', sharey=False, palette="Set3", aspect=1.5)

axes = g3.axes
axes[0][0].set_ylim(0, 100)
axes[3][0].set_ylim(0, 100)

g3.savefig('results/duration.png')

'''
Contributors
'''

df4 = pd.DataFrame(projects)
df4 = pd.melt(df4, id_vars=['contributors'], value_vars=['nr microservices', 'size', 'average size', 'depends on'])
g4 = sns.lmplot(data=df4, x='contributors', y='value', row='variable', sharey=False, palette="Set3", aspect=1.5)

axes = g4.axes
axes[0][0].set_ylim(0, 100)
axes[3][0].set_ylim(0, 100)

g4.savefig('results/contributors.png')


plt.show()

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
        size += microservice['size']
        nr_microservices = len(project.microservices)

    projects.append({
        'name': project.name,
        'created': project.created,
        'updated': project.last_updated,
        'duration': project.last_updated - project.created,
        'nr microservices': nr_microservices,
        'size': size,
        'average size': size/nr_microservices,
        'depends on': project.depends_on,
        'contributors': project.contributors,
        'language': project.language,
        'commits': project.commits
    })


'''
Last updated
'''

df = pd.DataFrame(projects)
df['year'] = df['updated'].dt.year
df = pd.melt(df, id_vars=['year'], value_vars=['nr microservices', 'size', 'average size', 'depends on'])
g = sns.FacetGrid(df, row='variable', sharey=False, aspect=1.5)
g.map(sns.boxplot, 'year', 'value', palette="Set3")

axes = g.axes
axes[0][0].set_ylim(0, 45)
axes[1][0].set_ylim(0, 20000000000)
axes[2][0].set_ylim(0, 2000000000)
axes[3][0].set_ylim(0, 45)

g.savefig('results/last_updated.png')

fig, ax = plt.subplots()
df_last_updated_micro = pd.DataFrame(projects)
df_last_updated_micro['year'] = df_last_updated_micro['updated'].dt.year
sns.boxplot(data=df_last_updated_micro, x='year', y='nr microservices', ax=ax, palette="Set3")

fig.savefig('results/last_updated_micro.png')


'''
Influence of language
'''
df2_line = pd.DataFrame(projects)
df2_box = pd.DataFrame(projects)
df2_box['year'] = df2_box['updated'].dt.year
# print(df2['language'].value_counts())
languages = ['JavaScript', 'PHP', 'Java', 'Python', 'C#']
df2_box = df2_box[df2_box['language'].isin(languages)]
df2_line = df2_line[df2_line['language'].isin(languages)]

df2_box = pd.melt(df2_box, id_vars=['year', 'language'], value_vars=['nr microservices', 'size', 'average size', 'depends on'])
g2_box = sns.FacetGrid(df2_box, row='variable', sharey=False, aspect=1.5, legend_out=True)
g2_box.map(sns.boxplot, 'year', 'value', 'language', palette="Set3").add_legend()

df2_line = pd.melt(df2_line, id_vars=['updated', 'language'], value_vars=['nr microservices', 'size', 'average size', 'depends on'])
g2_line = sns.relplot(x='updated', y='value', data=df2_line, kind='line', hue='language', row='variable', facet_kws={'sharey': False})

axes_line = g2_line.axes
axes_box = g2_box.axes

axes_line[0][0].set_ylim(0, 25)
axes_line[1][0].set_ylim(0, 12000000000)
axes_line[2][0].set_ylim(0, 1200000000)
axes_line[3][0].set_ylim(0, 25)

axes_box[0][0].set_ylim(0, 25)
axes_box[1][0].set_ylim(0, 14000000000)
axes_box[2][0].set_ylim(0, 1400000000)
axes_box[3][0].set_ylim(0, 30)

g2_box.savefig('results/language_box.png')
g2_line.savefig('results/language_line.png')

fig, (ax1, ax2) = plt.subplots(2, sharex=True)
df_last_updated_lang = pd.DataFrame(projects)
df_last_updated_lang = df_last_updated_lang[df_last_updated_lang['language'].isin(languages)]
df_last_updated_lang['year'] = df_last_updated_lang['updated'].dt.year
sns.boxplot(data=df_last_updated_lang, x='year', y='nr microservices', ax=ax1, hue="language", palette="Set3").legend().remove()
sns.boxplot(data=df_last_updated_lang, x='year', y='depends on', ax=ax2, hue="language", palette="Set3")
ax1.set_ylim(0, 25)
ax2.set_ylim(0, 25)

fig.savefig('results/last_updated_lang.png')


'''
Project Duration
'''

df3 = pd.DataFrame(projects)
df3['duration'] = df3['duration'].dt.days
df3 = pd.melt(df3, id_vars=['duration'], value_vars=['nr microservices', 'size', 'average size', 'depends on'])
g3 = sns.lmplot(data=df3, x='duration', y='value', row='variable', sharey=False, palette="Set3", aspect=1.5)

axes = g3.axes
axes[0][0].set_ylim(0, 45)
axes[1][0].set_ylim(0, 40000000000)
axes[2][0].set_ylim(0, 4000000000)
axes[3][0].set_ylim(0, 45)

g3.savefig('results/duration.png')

df = pd.DataFrame(projects)
df['duration'] = df['duration'].dt.days
fig, ax = plt.subplots()
sns.regplot(data=df, x='duration', y='average size', ax=ax)
ax.set_ylim(0, 4000000000)

fig.savefig('results/duration_avg_size.png')


'''
Contributors
'''

df4 = pd.DataFrame(projects)
df4 = pd.melt(df4, id_vars=['contributors'], value_vars=['nr microservices', 'size', 'average size', 'depends on'])
g4 = sns.lmplot(data=df4, x='contributors', y='value', row='variable', sharey=False, palette="Set3", aspect=1.5)

axes = g4.axes
axes[0][0].set_ylim(0, 45)
axes[1][0].set_ylim(0, 40000000000)
axes[2][0].set_ylim(0, 4000000000)
axes[3][0].set_ylim(0, 45)

g4.savefig('results/contributors.png')


'''
Commits
'''

df5 = pd.DataFrame(projects)
# delete one clear outlier
df5 = df5[df5['commits'] < 25000]

df5 = pd.melt(df5, id_vars=['commits'], value_vars=['nr microservices', 'size', 'average size', 'depends on'])
g5 = sns.lmplot(data=df5, x='commits', y='value', row='variable', sharey=False, palette="Set3", aspect=1.5)

axes = g5.axes
axes[0][0].set_ylim(0, 45)
axes[1][0].set_ylim(0, 40000000000)
axes[2][0].set_ylim(0, 4000000000)
axes[3][0].set_ylim(0, 45)

g5.savefig('results/commits.png')

fig, (ax1, ax2) = plt.subplots(2, sharex=True)

df = pd.DataFrame(projects)
df = df[df['commits'] < 25000]
sns.regplot(data=df, x='commits', y='size', ax=ax1)
sns.regplot(data=df, x='commits', y='depends on', ax=ax2)
ax1.set_ylim(0, 30000000000)
ax2.set_ylim(0, 45)

fig.savefig('results/commits_size_deps.png')


# nr microservices vs dependencies between them
df = pd.DataFrame(projects)
fig, ax = plt.subplots()
sns.regplot(data=df, x='nr microservices', y='depends on', ax=ax)

fig.savefig('results/mirco_vs_deps.png')


# plt.show()

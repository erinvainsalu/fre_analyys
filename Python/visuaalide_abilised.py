import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import seaborn as sns
import numpy as np
import math

#custom_params = {"axes.spines.right": False, "axes.spines.top": False}
#sns.set_theme(style = 'whitegrid', rc = custom_params)

def maara_raporti_stiil():

    sns.set_theme(style='whitegrid')

    plt.rcParams.update({
        # font
        #"font.family": "sans-serif",
        'font.size': 10,
        'axes.titlesize': 13,
        'axes.labelsize': 10,

        # telgede stiil
        'axes.spines.top': False,
        'axes.spines.right': False,
        'axes.spines.left': False,

        # grid
        #"axes.grid": True,
        'grid.linestyle': '--',
        'grid.alpha': 0.4,

        # legend
        'legend.frameon': False,

        # figure
        #"figure.dpi": 120
    })
    
    return {
        # Defineeri värvipalett
    #PALETTE = ["#3B5BA5", "#55A868", "#C44E52", "#8172B3", "#CCB974"]
    # PALETTE = ["#1B1F3B", "#00429D", "#006D5B", "#2E7D32", "#8E24AA", '#B71C1C', '#C05600', '#37474F'] # dark palette

        'PALETTE': [
            '#3B5BA5',  # blue (original)
            '#2A9D8F',  # teal (clearly different from blue)
            '#55A868',  # green (original)
            '#C44E52',  # red (original anchor)
            '#F4A261',  # muted orange
            '#8172B3',  # purple (original)
            '#8D6E63',  # muted brown
            '#7F7F7F'   # neutral grey
        ],
        'PRIMARY_COLOR': '#3B5BA5'
    }

# Defineeri ühtne graafikute stiil
def create_fig(figsize=(7, 5)):
    fig, ax = plt.subplots(figsize=figsize)

    # ühtne spacing kõigile
    fig.subplots_adjust(bottom=0.2)

    return fig, ax

def leia_sildi_mapping(df_koodid, tunnus):
     return (
        df_koodid[df_koodid['kysimus'] == tunnus]
        .set_index('kood')['vastus_lyhike']
        .to_dict()
    )

# Loo ühe tunnuse osas andmetabel vastuste absoluut- ja suhtarvudega
def sagedustabel(df_data, df_koodid, tunnus, use_full_codebook=True):
    
    # --- counts from data ---
    counts = df_data[tunnus].value_counts()

    if use_full_codebook:
        # use full list of possible answers
        df_map = df_koodid[df_koodid['kysimus'] == tunnus].copy()

        # ensure all codes appear
        df_map['vastuste_arv'] = df_map['kood'].map(counts).fillna(0).astype(int)

    else:
        # use only observed values (partial mode)
        df_map = counts.reset_index()
        df_map.columns = ['kood', 'vastuste_arv']

        # optionally merge labels if available
        labels = df_koodid[df_koodid['kysimus'] == tunnus][['kood', 'vastus_lyhike']]
        df_map = df_map.merge(labels, on='kood', how='left')

    # --- percentages ---
    total = df_map['vastuste_arv'].sum()
    df_map['protsent'] = (df_map['vastuste_arv'] / total * 100).round(0).astype(int) if total > 0 else 0
    df_map['protsent_str'] = df_map['protsent'].map(lambda x: f'{x:.0f}%')

    return df_map[['kood', 'vastus_lyhike', 'vastuste_arv', 'protsent', 'protsent_str']]

# Loo mitmikvastusega tunnuse osas andmetabel vastuste absoluut- ja suhtarvudega
def mitmikvastuse_sagedustabel(df_data, df_koodid, tunnus):
    # Leia võimalike vastusevariantide arv
    ridade_arv = len(df_koodid[df_koodid['kysimus'] == tunnus])
    
    # Leia vastajate arv (kes valis vähemalt ühe vastuse)
    cols = [f'{tunnus}_{i}' for i in range(1, ridade_arv+1)]
    vastajate_arv = (df_data[cols].sum(axis=1) > 0).sum()
    
    # Filtreeri koodid
    df_tunnus = df_koodid[df_koodid['kysimus'] == tunnus].copy()
    
    # Loo tulemustabel
    tulemus = pd.DataFrame({
        'kood': range(1, ridade_arv+1),
        'vastus_lyhike': df_tunnus['vastus_lyhike'].values,
        'vastuste_arv': [df_data[f'{tunnus}_{i}'].sum() for i in range(1, ridade_arv+1)]
    })
    
    tulemus['protsent'] = (tulemus['vastuste_arv'] / vastajate_arv * 100).round(0).astype(int) if vastajate_arv > 0 else 0
    tulemus['protsent_str'] = tulemus['protsent'].astype(int).astype(str) + '%'
    
    return tulemus

# Loo kahe tunnuse risttabel
def loo_risttabel(df, df_koodid, tunnus_rida, tunnus_veerg, normalize=False):
    if normalize:
        risttabel = pd.crosstab(
            index=df[tunnus_rida],
            columns=df[tunnus_veerg],
            normalize='index'
        ) * 100
        risttabel = risttabel.round(0)
    else:
        risttabel = pd.crosstab(
            index=df[tunnus_rida],
            columns=df[tunnus_veerg]
        )
    
    # Leia koodide tabelist koodidele vastavad nimetused ridade/veergude pealkirjadeks
    row_map = leia_sildi_mapping(df_koodid, tunnus_rida)
    col_map = leia_sildi_mapping(df_koodid, tunnus_veerg)

    # Asenda koodid neile vastavate nimetustega
    risttabel.index = risttabel.index.map(lambda x: row_map.get(x, x))
    risttabel.columns = risttabel.columns.map(lambda x: col_map.get(x, x))

    return risttabel

# Loo kahe tunnuse risttabel, kus üks tunnustest on mitmikvalikuga

# Loo vertikaalne tulpdiagramm
def loo_tulpdiagramm(df, title, style_config, hue=None, percent=True, sort=False):
    
    # Vajadusel sorteeri andmestik
    if sort:
        df = df.sort_values("protsent", ascending=False)
    
    #print('Vastuste jaotus:')
    #print(df.to_string(index=False))
    
    fig, ax = create_fig()

    # Loo diagramm
    sns.barplot(
        data=df,
        x='vastus_lyhike',
        y='protsent' if percent else 'vastuste_arv', # kasutaja kas suhtarve või absoluutseid väärtuseid
        hue=hue,
        color=style_config['PRIMARY_COLOR'],
        ax=ax
    )
    
    # Lisa pealkiri
    ax.set_title(title, weight='bold', loc='left', pad=15)
    
    # Eemalda telgede nimed
    ax.set(xlabel=None, ylabel=None)

    # Kui diagrammil kuvatud suhtarvud, siis muuda y-telg protsentideks
    if percent:
        ax.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=0))
        # Seadista graafiku max
        ax.set_ylim(0, df['protsent'].max() * 1.15)
        #ax.set_ylim(0, max(100, df["protsent"].max() * 1.15))
    
    # Kuva minimalistlik grid
    ax.grid(axis="x", visible=False)
 
    # Lisa diagrammile tekstilised annotatsioonid
    for idx, row in enumerate(df.itertuples()):
        label = f'{row.protsent:.0f}% ({row.vastuste_arv})'
        
        ax.text(
            idx,
            row.protsent + 1,
            label,
            horizontalalignment='center',
            verticalalignment='bottom',
            fontsize=10
        )
    
    plt.tight_layout()
    
    return fig, ax

# Loo horisontaalne tulpdiagramm
def loo_hor_tulpdiagramm(df, title, style_config, percent=True, sort=False):
    
    # Vajadusel sorteeri andmestik
    if sort:
        df = df.sort_values("protsent", ascending=False)
    
    #print('Vastuste jaotus:')
    #print(df.to_string(index=False))
    
    fig, ax = create_fig()

    # Loo diagramm
    sns.barplot(
        data=df,
        x='protsent' if percent else 'vastuste_arv', # kasutaja kas suhtarve või absoluutseid väärtuseid
        y='vastus_lyhike',
        color=style_config['PRIMARY_COLOR'],
        ax=ax
    )
    
    # Lisa pealkiri
    ax.set_title(title, weight='bold', loc='left', pad=15)
    
    # Eemalda telgede nimed
    ax.set(xlabel=None, ylabel=None)

    # Kui diagrammil kuvatud suhtarvud, siis muuda x-telg protsentideks
    if percent:
        ax.xaxis.set_major_formatter(mtick.PercentFormatter(decimals=0))
        # Seadista graafiku max
        ax.set_xlim(0, df['protsent'].max() * 1.15)
    
    # Kuva minimalistlik grid
    ax.grid(axis='y', visible=False)
 
    # Lisa diagrammile tekstilised annotatsioonid
    for idx, row in enumerate(df.itertuples()):
        label = f'{row.protsent:.0f}% ({row.vastuste_arv})'
        
        ax.text(
            row.protsent + 0.5,
            idx,
            label,
            horizontalalignment='left',
            verticalalignment='center',
            fontsize=10
        )
    
    plt.tight_layout()
    
    return fig, ax

# Loo vertikaalne "stacked" tulpdiagramm
def loo_stacked_tulpdiagramm(df, title, style_config, normalize=True):
    if normalize:
        # Teisenda absoluutarvud protsentideks
        df_plot = df.div(df.sum(axis=1), axis=0)
    else:
        df_plot = df.copy()
    
    #print(f'\nVastuste arv: {df.sum().sum()}')
    #print(f'Vastuste arv tunnuste kaupa:')
    #print(df.sum(axis=1))

    # Loo stacked tulpdiagramm
    fig, ax = create_fig()
    
    df_plot.plot(
        kind='bar',
        stacked=True,
        color=style_config['PALETTE'],
        ax=ax,
        width=0.8
    )

    ax.set_title(title, weight='bold', loc='left', pad=15)
    ax.set(xlabel=None, ylabel=None)
    #ax.set_xlabel('Vanusegrupp', fontsize=13, fontweight='bold')
    #ax.set_ylabel('Protsent (%)', fontsize=13, fontweight='bold')

    # Kui diagrammil kuvatud suhtarvud, siis muuda y-telg protsentideks
    if normalize:
        ax.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1))
        ax.set_ylim(0, 1)
    
    # x-telg
    ax.set_xticklabels(df.index, rotation=0, ha='center')

    # Lisa segmentidele neile vastavad protsendid sildina
    for container in ax.containers:
        # Kuva silte ainult juhul kui >5
        labels = [f'{v*100:.0f}%' if v*100 > 5 else '' for v in container.datavalues]
        ax.bar_label(
            container,
            labels=labels,
            label_type='center',
            fontsize=9
        )

    max_cols = 4  # mitu legendi elementi maksimaalselt ühel real
    ncol = math.ceil(len(df.columns) / 2)

    # Legendi stiil
    ncol = math.ceil(len(df.columns) / 2)  # jagab kaheks reaks
    ax.legend(
        bbox_to_anchor=(0.5, -0.1),
        loc="upper center",
        fontsize=9,
        ncol=ncol,
        columnspacing=1.2,
        handletextpad=0.5
    )

    # Lisa diagrammile x-telje alla vastuste arvudele vastavad sildid
    #for i, (grupp, count) in enumerate(df.sum(axis=1).items()):
    #    ax.text(
    #        i,
    #        -0.12,
    #        f'n={count}',
    #        ha='center',
    #        #va='top', 
    #        fontsize=9,
    #        style='italic',
    #        color='gray'
    #    )

    plt.tight_layout()
    #plt.savefig('/mnt/user-data/outputs/stacked_bar_final.png', dpi=300, bbox_inches='tight', facecolor='white')

    return fig, ax

# Loo horisontaalne "stacked" tulpdiagramm
def loo_hor_stacked_tulpdiagramm(df, title, style_config, normalize=True, sort=True):
    
    if normalize:
        # Teisenda absoluutarvud protsentideks
        df_plot = df.div(df.sum(axis=1), axis=0)
    else:
        df_plot = df.copy()
    
    # Vajadusel sorteeri andmestik
    if sort:
        df = df.loc[df.sum(axis=1).sort_values(ascending=True).index]
    
    #print(f'\nVastuste arv: {df.sum().sum()}')
    #print(f'Vastuste arv tunnuste kaupa:')
    #print(df.sum(axis=1))

    # Loo stacked tulpdiagramm
    fig, ax = create_fig()
    
    df_plot.plot(
        kind="barh",
        stacked=True,
        color=style_config['PALETTE'],
        ax=ax
    )

    #ax.margins(y=0.1)

    ax.set_title(title, weight='bold', loc='left', pad=15)
    ax.set(xlabel=None, ylabel=None)

    # Kui diagrammil kuvatud suhtarvud, siis muuda x-telg protsentideks
    if normalize:
        ax.xaxis.set_major_formatter(mtick.PercentFormatter(xmax=1))
        ax.set_xlim(0, 1)

    # y-telg
    ax.set_yticklabels(df.index)
    if not sort:
        ax.invert_yaxis()

    # Lisa segmentidele neile vastavad protsendid sildina
    for container in ax.containers:
        labels = [
            f'{v*100:.0f}%' if (normalize and v*100 > 5)
            else (f'{int(v)}' if not normalize and v > 0 else '')
            for v in container.datavalues
        ]
        
        ax.bar_label(
            container,
            labels=labels,
            label_type='center',
            fontsize=8
        )

    # Legendi stiil
    ncol = math.ceil(len(df.columns) / 2)  # jagab kaheks reaks
    ax.legend(
        bbox_to_anchor=(0.5, -0.1),
        loc="upper center",
        fontsize=9,
        ncol=ncol,
        columnspacing=1.2,
        handletextpad=0.5
    )

    # Lisa absoluutarvude sildid vasakule
    totals = df.sum(axis=1)
    
    # Lisa diagrammile y-telje juurde vastuste arvudele vastavad sildid
    #for i, (grupp, count) in enumerate(totals.items()):
    #    ax.text(
    #        -0.03,
    #        i-0.5,
    #        f'(n={count})',
    #        transform=ax.get_yaxis_transform(),
    #        ha='right',
    #        va='center',
    #        fontsize=8,
    #        style='italic',
    #        color='gray'
    #    )

    # --- clean grid ---
    #ax.grid(axis='x', linestyle='--', alpha=0.4)
    #ax.grid(axis='y', visible=False)

    plt.tight_layout()

    return fig, ax

# Loo heatmap
def loo_heatmap(df, title, cmap='coolwarm_r', fmt='.0f'):
    fig, ax = create_fig()
    
    # Loo diagramm
    sns.heatmap(
        data=df,
        cmap=cmap,
        linewidths=1,
        #linecolor='gray',
        annot=True
        #square= True
    )

    # Lisa pealkiri
    ax.set_title(title, weight='bold', loc='left', pad=15)

    plt.xticks(rotation=45)
    ax.set(xlabel=None)
    ax.set(ylabel=None)

    # Eemalda telgede nimed
    #ax.set(xlabel=None, ylabel=None)

    # Kuva minimalistlik grid
    #ax.grid(axis="x", visible=False)
    
    plt.tight_layout()
    
    return fig, ax
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from matplotlib.colors import to_hex
import seaborn as sns
import numpy as np
import math

#custom_params = {"axes.spines.right": False, "axes.spines.top": False}
#sns.set_theme(style = 'whitegrid', rc = custom_params)

def maara_raporti_stiil():

    sns.set_theme(style='whitegrid')

    sns.set_palette(palette='coolwarm_r')

    plt.rcParams.update({
        # font
        'font.family': 'sans-serif',
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
        'BAR_PALETTE': plt.get_cmap('coolwarm_r')(1.0),
        'STACKED_BAR_PALETTE': 'coolwarm_r'
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
def loo_risttabel(df_data, df_koodid, tunnus_rida, tunnus_veerg, normalize=False):
    if normalize:
        risttabel = pd.crosstab(
            index=df_data[tunnus_rida],
            columns=df_data[tunnus_veerg],
            normalize='index'
        ) * 100
        risttabel = risttabel.round(0)
    else:
        risttabel = pd.crosstab(
            index=df_data[tunnus_rida],
            columns=df_data[tunnus_veerg]
        )
    
    # Leia koodide tabelist koodidele vastavad nimetused ridade/veergude pealkirjadeks
    row_map = leia_sildi_mapping(df_koodid, tunnus_rida)
    col_map = leia_sildi_mapping(df_koodid, tunnus_veerg)

    # Asenda koodid neile vastavate nimetustega
    risttabel.index = risttabel.index.map(lambda x: row_map.get(x, x))
    risttabel.columns = risttabel.columns.map(lambda x: col_map.get(x, x))

    return risttabel

# Loo kahe tunnuse risttabel, kus üks tunnustest on mitmikvalikuga
def loo_mitmikvastuse_risttabel(df_data, df_koodid, tunnus_single, tunnus_multiselect, normalize=False):
    """
    Loo risttabel mitmikvastusega ja ühe valikvastusega tunnuse vahel.
    Tagastab risttabeli, kus read = mitmikvastuse valikud, veerud = ühe valikvastuse kategooriad
    """
    
    # eia mitmikvastuse veergude arv ja nimed
    ridade_arv = len(df_koodid[df_koodid['kysimus'] == tunnus_multiselect])
    multiselect_cols = [f'{tunnus_multiselect}_{i}' for i in range(1, ridade_arv + 1)]
    
    # Leia mitmikvastuse vastuste sildid (lühikesed)
    multiselect_labels = (
        df_koodid[df_koodid['kysimus'] == tunnus_multiselect]
        .set_index('kood')['vastus_lyhike']
        .to_dict()
    )
    
    # Loo veergude mapping (K22_peamised_valjakutsed_1 -> sildile)
    veerud_mapping = {
        f'{tunnus_multiselect}_{kood}': label 
        for kood, label in multiselect_labels.items()
    }
    
    # Leia ühe valikvastuse kategooriate sildid
    single_labels = leia_sildi_mapping(df_koodid, tunnus_single)
    
    # Grupeeri andmed ja summeeri
    risttabel = (
        df_data[[tunnus_single, *multiselect_cols]]
        .groupby(tunnus_single)
        .sum()
    )
    
    # Nimeta veerud ümber vastuse teksivariandiks
    risttabel = risttabel.rename(columns=veerud_mapping)
    
    # Nimeta read ümber vastuse teksivariandiks
    risttabel.index = risttabel.index.map(single_labels)
        
    # Vajadusel teisenda protsentideks
    if normalize:
        # Protsendid ridade lõikes
        risttabel = risttabel.div(risttabel.sum(axis=1), axis=0).mul(100).round(0)
    
    return risttabel

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
        color=style_config['BAR_PALETTE'],
        ax=ax
    )
    
    # Lisa pealkiri
    ax.set_title(title, weight='bold', loc='left', pad=15)
    
    # Eemalda telgede nimed
    ax.set(xlabel=None, ylabel=None)

    ax.tick_params(axis='x', labelsize=10)
    ax.tick_params(axis='y', labelsize=10)

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
        color=style_config['BAR_PALETTE'],
        ax=ax
    )
    
    # Lisa pealkiri
    ax.set_title(title, weight='bold', loc='left', pad=15)
    
    # Eemalda telgede nimed
    ax.set(xlabel=None, ylabel=None)

    ax.tick_params(axis='x', labelsize=10)
    ax.tick_params(axis='y', labelsize=10)

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

    # Leia veergude arvule vastav värvide jaotus
    colors = plt.get_cmap(style_config['STACKED_BAR_PALETTE'])(np.linspace(0.2, 0.9, len(df.columns)))

    # Loo stacked tulpdiagramm
    fig, ax = create_fig()
    
    df_plot.plot(
        kind='bar',
        stacked=True,
        color=colors,
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
    
    # telgede tekstid
    ax.set_xticklabels(df.index, rotation=0, ha='center', size=10)
    ax.tick_params(axis='y', labelsize=10)

    # Lisa segmentidele neile vastavad protsendid sildina
    for container in ax.containers:
        # Kuva silte ainult juhul kui >5
        labels = [f'{v*100:.0f}%' if v*100 > 5 else '' for v in container.datavalues]
        ax.bar_label(
            container,
            labels=labels,
            label_type='center',
            fontsize=10
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
def loo_hor_stacked_tulpdiagramm(df, title, style_config, normalize=True, sort=False):
    
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

    # Leia veergude arvule vastav värvide jaotus
    colors = plt.get_cmap(style_config['STACKED_BAR_PALETTE'])(np.linspace(0.25, 0.85, len(df.columns)))

    # Loo stacked tulpdiagramm
    fig, ax = create_fig()
    
    df_plot.plot(
        kind="barh",
        stacked=True,
        color=colors,
        ax=ax
    )

    #ax.margins(y=0.1)

    ax.set_title(title, weight='bold', loc='left', pad=15)
    ax.set(xlabel=None, ylabel=None)

    # Kui diagrammil kuvatud suhtarvud, siis muuda x-telg protsentideks
    if normalize:
        ax.xaxis.set_major_formatter(mtick.PercentFormatter(xmax=1))
        ax.set_xlim(0, 1)

    # telgede tekstid
    ax.set_yticklabels(df.index, size=10)
    if not sort:
        ax.invert_yaxis()
    ax.tick_params(axis='x', labelsize=10)

    # Lisa segmentidele neile vastavad protsendid sildina
    for container in ax.containers:
        labels = [
            f'{v*100:.0f}%' if (normalize and v*100 > 5)
            else (f'{int(v)}' if not normalize and v > 5 else '')
            for v in container.datavalues
        ]
        
        ax.bar_label(
            container,
            labels=labels,
            label_type='center',
            fontsize=10
        )

    # Legendi stiil
    ncol = math.ceil(len(df.columns) / 2)  # jagab kaheks reaks
    ax.legend(
        bbox_to_anchor=(0.5, -0.1),
        loc='upper center',
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
    
    cmap = sns.color_palette(cmap, as_cmap=True)
    colors = [to_hex(cmap(x)) for x in np.linspace(0.5, 1, 8)]

    # Loo diagramm
    sns.heatmap(
        data=df,
        cmap=colors,
        linewidths=1,
        #linecolor='gray',
        annot=df.astype(int).astype(str) + '%',
        fmt=''
        #square= True
    )

    ax.invert_yaxis()  # Pööra y-telg ümber

    # Lisa pealkiri
    ax.set_title(title, weight='bold', loc='left', pad=15)

    plt.xticks(rotation=45, ha='right', rotation_mode='anchor', size=10)
    plt.yticks(size=10)
    ax.set(xlabel=None)
    ax.set(ylabel=None)

    # Eemalda telgede nimed
    #ax.set(xlabel=None, ylabel=None)

    # Kuva minimalistlik grid
    #ax.grid(axis="x", visible=False)
    
    plt.tight_layout()
    
    return fig, ax

def loo_diverging_stacked_tulpdiagramm(df, title, style_config, neutral_col=None, normalize=True, show_labels=True, min_label_pct=5):
    """
    Loo diverging stacked bar chart (Likert-skaala jaoks).
    
    Negatiivse poolega veerud kuvatakse vasakul, positiivsed paremal,
    neutraalsed (kui on) jagunevad keskelt pooleks.
    
    Parameters:
    -----------
    df : DataFrame
        Risttabel, kus read = kategooriad, veerud = vastusevariandid
    title : str
        Graafiku pealkiri
    style_config : dict
        Stiili konfiguratsioon (PALETTE, PRIMARY_COLOR)
    neutral_col : str or int, optional
        Neutraalse veeru nimi või indeks (nt 'Pole kindel', 2)
        Kui None, siis eeldatakse, et neutraalne on keskel
    normalize : bool
        Kui True, siis kuvatakse protsendid (default: True)
    show_labels : bool
        Kui True, kuvatakse protsendid segmentidel (default: True)
    min_label_pct : float
        Minimaalne protsent, mille puhul silt kuvatakse (default: 5)
    
    Returns:
    --------
    tuple
        (fig, ax) matplotlib objektid
        
    Example:
    --------
    # Näide Likert-skaalaga: Täiesti ei nõustu | Pigem ei nõustu | Neutraalne | Pigem nõustun | Täiesti nõustun
    risttabel = loo_risttabel(data, koodid, 'K3_vanus', 'K30_valmisolek', normalize=True)
    fig, ax = loo_diverging_stacked_tulpdiagramm(
        df=risttabel,
        title='Valmisolek sorteerida vanuse järgi',
        style_config=style_config,
        neutral_col=2  # Kolmas veerg on neutraalne
    )
    """
    
    if normalize:
        df_plot = df.div(df.sum(axis=1), axis=0) * 100
    else:
        df_plot = df.copy()
    
    n_cols = len(df_plot.columns)
    
    # Defineeri, millised veerud on negatiivse/positiivse poolega
    if neutral_col is not None:
        # Kui neutraalne veerg on määratud
        if isinstance(neutral_col, str):
            neutral_idx = df_plot.columns.get_loc(neutral_col)
        else:
            neutral_idx = neutral_col
        
        neg_cols = df_plot.columns[:neutral_idx]
        neutral = df_plot.columns[neutral_idx]
        pos_cols = df_plot.columns[neutral_idx + 1:]
    else:
        # Kui neutraalne veerg puudub, jaga pooleks
        mid = n_cols // 2
        neg_cols = df_plot.columns[:mid]
        pos_cols = df_plot.columns[mid:]
        neutral = None
    
    # Loo joonis
    fig, ax = create_fig(figsize=(10, len(df_plot) * 0.5 + 2))
    
    # Arvuta offset'id diverging effect'i jaoks
    # Negatiivne pool läheb vasakule (miinus väärtused)
    df_plot_neg = df_plot[neg_cols].copy()
    df_plot_neg = -df_plot_neg  # Tee negatiivseks
    
    # Positiivne pool läheb paremale
    df_plot_pos = df_plot[pos_cols].copy() if len(pos_cols) > 0 else pd.DataFrame()
    
    y_pos = np.arange(len(df_plot))
    
    # Joonista negatiivne pool (vasakule)
    left_start = df_plot_neg.sum(axis=1).values
    
    for i, col in enumerate(reversed(neg_cols)):
        values = df_plot_neg[col].values
        bars = ax.barh(
            y_pos,
            values,
            left=left_start - values,
            color=style_config['PALETTE'][i % len(style_config['PALETTE'])],
            label=col,
            height=0.8
        )
        
        # Lisa annotatsioonid
        if show_labels:
            for idx, (bar, val) in enumerate(zip(bars, values)):
                abs_val = abs(val)
                if abs_val >= min_label_pct:
                    # Arvuta segmendi keskkoht
                    x_center = bar.get_x() + bar.get_width() / 2
                    ax.text(
                        x_center,
                        bar.get_y() + bar.get_height() / 2,
                        f'{abs_val:.0f}%',
                        ha='center',
                        va='center',
                        fontsize=8,
                        color='white',
                        weight='bold'
                    )
        
        left_start = left_start - values
    
    # Joonista neutraalne (kui on) - jaga pooleks
    if neutral is not None:
        neutral_values = df_plot[neutral].values
        half_neutral = neutral_values / 2
        
        # Vasak pool
        bars_left = ax.barh(
            y_pos,
            half_neutral,
            left=-half_neutral,
            color='#D3D3D3',  # Hall värv neutraalsele
            label=neutral,
            height=0.8,
            alpha=0.7
        )
        
        # Parem pool
        bars_right = ax.barh(
            y_pos,
            half_neutral,
            left=0,
            color='#D3D3D3',
            height=0.8,
            alpha=0.7
        )
        
        # Lisa annotatsioonid (ainult ühele poolele, et mitte dubleerida)
        if show_labels:
            for idx, (bar, val) in enumerate(zip(bars_right, neutral_values)):
                if val >= min_label_pct:
                    # Kuvame terve väärtuse, mitte poolt
                    ax.text(
                        0,  # Keskele
                        bar.get_y() + bar.get_height() / 2,
                        f'{val:.0f}%',
                        ha='center',
                        va='center',
                        fontsize=8,
                        color='black',
                        weight='bold'
                    )
        
        right_start = half_neutral
    else:
        right_start = np.zeros(len(df_plot))
    
    # Joonista positiivne pool (paremale)
    for i, col in enumerate(pos_cols):
        values = df_plot_pos[col].values
        bars = ax.barh(
            y_pos,
            values,
            left=right_start,
            color=style_config['PALETTE'][(len(neg_cols) + (1 if neutral else 0) + i) % len(style_config['PALETTE'])],
            label=col,
            height=0.8
        )
        
        # Lisa annotatsioonid
        if show_labels:
            for idx, (bar, val) in enumerate(zip(bars, values)):
                if val >= min_label_pct:
                    x_center = bar.get_x() + bar.get_width() / 2
                    ax.text(
                        x_center,
                        bar.get_y() + bar.get_height() / 2,
                        f'{val:.0f}%',
                        ha='center',
                        va='center',
                        fontsize=8,
                        color='white',
                        weight='bold'
                    )
        
        right_start = right_start + values
    
    # Stiil
    ax.set_title(title, weight='bold', loc='left', pad=15)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(df_plot.index)
    ax.set(xlabel=None, ylabel=None)
    
    # X-telg
    if normalize:
        # Näita protsente
        max_val = max(abs(df_plot_neg.sum(axis=1).min()), df_plot_pos.sum(axis=1).max() if len(pos_cols) > 0 else 0)
        if neutral is not None:
            max_val = max(max_val, (df_plot[neutral] / 2).max())
        
        ax.set_xlim(-max_val * 1.1, max_val * 1.1)
        
        # Formateeri x-telg protsendina
        ax.xaxis.set_major_formatter(mtick.FuncFormatter(lambda x, p: f'{abs(x):.0f}%'))
    
    # Null-joon
    ax.axvline(0, color='black', linewidth=0.8, linestyle='-', alpha=0.3)
    
    # Grid
    ax.grid(axis='y', visible=False)
    ax.grid(axis='x', linestyle='--', alpha=0.4)
    
    # Legend
    # Pööra legend ümber, et negatiivne oleks vasakul
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(
        handles[::-1],
        labels[::-1],
        bbox_to_anchor=(0.5, -0.1),
        loc='upper center',
        fontsize=9,
        ncol=min(4, len(df_plot.columns)),
        columnspacing=1.2,
        handletextpad=0.5
    )
    
    plt.tight_layout()
    
    return fig, ax


# Lihtsustatud versioon 5-punkti Likert-skaalale
def loo_likert_tulpdiagramm(df, title, style_config, normalize=True, show_labels=True, min_label_pct=5):
    """
    Lihtsustatud versioon Likert-skaala jaoks (5 või 7 punkti).
    Eeldab, et veerud on järjekorras: väga negatiivne → neutraalne → väga positiivne
    
    Parameters:
    -----------
    df : DataFrame
        Risttabel veergedega järjekorras (negatiivne → positiivne)
    title : str
        Graafiku pealkiri
    style_config : dict
        Stiili konfiguratsioon
    normalize : bool
        Kui True, kuvatakse protsendid
    show_labels : bool
        Kui True, kuvatakse protsendid segmentidel
    min_label_pct : float
        Minimaalne protsent annotatsioonide jaoks
        
    Returns:
    --------
    tuple
        (fig, ax) matplotlib objektid
    """
    
    n_cols = len(df.columns)
    neutral_idx = n_cols // 2  # Leia keskmine veerg
    
    return loo_diverging_stacked_tulpdiagramm(
        df=df,
        title=title,
        style_config=style_config,
        neutral_col=neutral_idx,
        normalize=normalize,
        show_labels=show_labels,
        min_label_pct=min_label_pct
    )
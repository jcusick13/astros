import pandas as pd


def summarize():
    """Summarize data by OBP for both trash can bangs and
    no bangs for each player. Remove batters with less than
    50 at bats."""
    df = pd.read_csv('data/astros_bangs_20200127.csv')

    # Tally if an at bat has bangs
    df['has_bangs_int'] = df.has_bangs.apply(lambda x: 1 if x == 'y' else 0)
    df = (
        df.groupby(['batter', 'at_bat_event', 'atbat_playid'])
        .has_bangs_int.sum()
        .reset_index()
    )

    # Create boolean for bangs
    df['has_bangs'] = df.has_bangs_int.apply(lambda x: 1 if x > 0 else 0)

    # Create boolean for on base
    on_base = ('Single', 'Walk', 'Double', 'Home Run', 'Hit By Pitch', 'Triple')
    df['on_base'] = df.at_bat_event.apply(lambda x: 1 if x in on_base else 0)

    # Summarize percentage of bangs at bat
    df_n = (
        df.groupby('batter')
        .agg({'atbat_playid': 'count', 'has_bangs': 'sum'})
        .reset_index()
        .rename(columns={'atbat_playid': 'n'})
    )
    df_n['has_bangs_perc'] = df_n.has_bangs / df_n.n
    df_n = df_n.drop(columns='has_bangs')

    # Summarize OBP by bangs/no bangs
    df_bangs = df[df.has_bangs == 1]
    df_no_bangs = df[df.has_bangs == 0]

    df_bangs = (
        df_bangs.groupby('batter')
        .agg({'atbat_playid': 'count', 'on_base': 'sum'})
        .reset_index()
        .rename(columns={'atbat_playid': 'n_bangs', 'on_base': 'on_base_bangs'})
    )
    df_bangs['obp_bangs'] = df_bangs.on_base_bangs / df_bangs.n_bangs

    df_no_bangs = (
        df_no_bangs.groupby('batter')
        .agg({'atbat_playid': 'count', 'on_base': 'sum'})
        .reset_index()
        .rename(columns={'atbat_playid': 'n_no_bangs', 'on_base': 'on_base_no_bangs'})
    )
    df_no_bangs['obp_no_bangs'] = df_no_bangs.on_base_no_bangs / df_no_bangs.n_no_bangs

    df_obp = pd.merge(df_bangs, df_no_bangs, how='inner', on='batter')

    # Combine both summaries
    df_summary = (
        pd.merge(df_n, df_obp, how='inner', on='batter')
        .sort_values('n', ascending=False)
        .query('n > 50')
        .reset_index(drop=True)
    )
    df_summary.to_csv('data/astros_bangs_summary.csv', index=False)
    print(df_summary)


if __name__ == '__main__':
    summarize()

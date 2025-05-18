import pandas as pd
import numpy as np

df = pd.read_csv('input_data/preferences_cleaned.csv', index_col=0)
missing_preferences = pd.read_csv('input_data/people_missing.csv', header=None)
people_to_ignore = missing_preferences[0].tolist()

def get_preferences(df):
    preferences = {}
    for person, row in df.iterrows():
        # Get columns sorted by the person's preference (ascending rank)
        ordered_dates = row.sort_values().index.tolist()
        preferences[person] = ordered_dates
    return preferences

def get_random_order(people, people_to_ignore):
    people = list(people)
    add_to_end = list(people_to_ignore)
    # Remove people_to_ignore from people
    people = [p for p in people if p not in add_to_end]
    order = np.random.permutation(people)
    order = list(order)
    return order + add_to_end

def assign_dates(df, preferences):
    people = get_random_order(df.index, people_to_ignore)
    sum = 0
    final_df = pd.DataFrame(index=df.index, columns=['Assignment', 'Rank'])
    available_dates = df.columns
    available_dates = list(available_dates)
    for person in people:
        preson_pref = preferences[person]
        # this is a list in order of the persons preference
        for pref in preson_pref:
            if pref in available_dates:
                # if the date is available, assign it to the person
                final_df.loc[person, 'Assignment'] = pref
                # remove the date from available dates
                available_dates.remove(pref)
                rank = df.loc[person, pref]
                sum += rank
                final_df.loc[person, 'Rank'] = rank
                break
    return final_df, sum

def run_simulation(df, n_simulations=10000):
    best_assignments = None
    best_score = float('inf')
    preferences = get_preferences(df)
    for _ in range(n_simulations):
        assignments, score = assign_dates(df, preferences)
        if score < best_score:
            best_score = score
            best_assignments = assignments
            print(f"New best score: {best_score} at iteration {_}")
    best_assignments.to_csv('output_data/assignments.csv', index=True)
    return True

run_simulation(df, n_simulations=10000)

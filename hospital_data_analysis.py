import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

pd.set_option('display.max_columns', None)

# Read CSV files from 3 hospitals
general = pd.read_csv('test\general.csv', encoding='utf-8')
prenatal = pd.read_csv('test\prenatal.csv', encoding='utf-8')
sports = pd.read_csv('test\sports.csv', encoding='utf-8')

# Change columns + merge tables + delete unnamed columns and empty rows + standardize gender to f/m
general.drop(columns='Unnamed: 0', inplace=True)
prenatal.drop(columns='Unnamed: 0', inplace=True)
sports.drop(columns='Unnamed: 0', inplace=True)

columns = ['hospital', 'gender', 'age', 'height', 'weight', 'bmi', 'diagnosis',
           'blood_test', 'ecg', 'ultrasound', 'mri', 'xray', 'children', 'months']

prenatal.columns = columns
sports.columns = columns
sports['height'] =  sports['height'] / 3.28084
df = pd.concat([general, prenatal, sports], ignore_index=True)

# Fill NaN values
df.dropna(axis=0, thresh=3, inplace=True)
df['gender'].replace(['male', 'man'], "m", inplace=True)
df['gender'].replace(['woman', 'female'], "f", inplace=True)
# condition = (df['hospital'] == 'prenatal') & (df['gender'].isnull())
df['gender'].fillna('f', inplace=True)
df.fillna(0 ,inplace=True)

sampled_df = df.sample(n=20, random_state=30)

# What share of the patients in the general hospital
# suffers from stomach-related issues? Round the result to the third decimal place.
highest_number = df.hospital.mode()[0]
stomach = df.loc[(df['diagnosis'] == 'stomach') & (df['hospital'] == 'general')]
share_stomach = (stomach.hospital.count() / (df.loc[(df['hospital'] == 'general')]).hospital.count())

# What share of the patients in the sports hospital suffers
# from dislocation-related issues? Round the result to the third decimal place.
dislocation = df.loc[(df["diagnosis"] == 'dislocation') & (df['hospital'] == 'sports')]
share_dislocation = (dislocation.hospital.count()) / (df.loc[(df['hospital'] == 'sports')]).hospital.count()

# What is the difference in the median ages of the patients in the general and sports hospitals?
groups = df.groupby(['hospital']).agg({'age':'median'})
diff = (groups.values[0] - groups.values[2])[0]

# After data processing at the previous stages, the blood_test column has three values:
# t= a blood test was taken, f= a blood test wasn't taken, and 0= there is no information.
# In which hospital the blood test was taken the most often (there is the biggest number of t
# in the blood_test column among all the hospitals)? How many blood tests were taken?
x = df[df.blood_test == 't']
blood = x.groupby(['hospital']).agg({'blood_test':'count'})
blood_hospital = blood['blood_test'].idxmax()

blood_number = blood.max()


print(f'The answer to the 1st question is {highest_number}\n'
        f'The answer to the 2nd question is {share_stomach.round(3)}\n'
        f'The answer to the 3rd question is {share_dislocation.round(3)}\n'
        f'The answer to the 4th question is {int(diff)}\n'
        f'The answer to the 5th question is {blood_hospital}, {blood_number.values[0]} blood tests')

# 1. What is the most common age of a patient among all hospitals?
# 2. What is the most common diagnosis among patients in all hospitals?
# 3. What is the most common diagnosis among patients in all hospitals?
def histo():
    bins = [0, 15, 35, 55, 70, 80]
    fig, axes = plt.subplots()

    plt.hist(df['age'], color='black', edgecolor='white', bins=bins, label='Age of patients')
    plt.title('The most common age of a patient')
    plt.ylabel("Number of people")
    plt.xlabel("Age")
    axes.set_xticks(bins)
    plt.legend()
    plt.show()


def pie_chart():

    pie_data = df.diagnosis.value_counts()
    indexes = pie_data.index.tolist()
    values = pie_data.tolist()
    colors = ['#66c2a5', '#fc8d62', '#8da0cb', '#e78ac3', '#a6d854', '#ffd92f', '#e5c494']
    explode = [0.1 if x == max(values) else 0 for x in values]
    plt.figure(figsize=(7, 7))
    chart = plt.pie(values, labels=indexes,shadow=True,autopct='%.1f%%',
                    colors=colors, explode=explode)
    plt.title('The most common diagnosis')
    plt.show()

def violin():
    sns.violinplot(df, x = 'hospital', y='height')
    plt.title('height distribution by hospitals')

    plt.show()
histo()
pie_chart()
violin()

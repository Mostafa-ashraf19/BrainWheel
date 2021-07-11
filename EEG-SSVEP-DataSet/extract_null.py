import pandas as pd


if __name__ == '__main__':
    df = pd.read_csv('U0000aii.csv')
    df_null = df[df['Label']==1]

    print(df_null.shape)

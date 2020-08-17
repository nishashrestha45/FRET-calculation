import pandas as pd
import numpy as np
import glob

from pandas.core.dtypes.missing import array_equivalent


def getDuplicateColumns(df):
    '''
    Get a list of duplicate columns.
    It will iterate over all the columns in dataframe and find the columns whose contents are duplicate.
    :param df: Dataframe object
    :return: List of columns whose contents are duplicates.
    '''
    duplicateColumnNames = set()
    # Iterate over all the columns in dataframe
    for x in range(df.shape[1]):
        # Select column at xth index.
        col = df.iloc[:, x]
        # Iterate over all the columns in DataFrame from (x+1)th index till end
        for y in range(x + 1, df.shape[1]):
            # Select column at yth index.
            otherCol = df.iloc[:, y]
            # Check if two columns at x 7 y index are equal
            if col.equals(otherCol):
                duplicateColumnNames.add(df.columns.values[y])

    return list(duplicateColumnNames)


def duplicate_columns(frame):
    groups = frame.columns.to_series().groupby(frame.dtypes).groups
    dups = []
    for t, v in groups.items():
        dcols = frame[v].to_dict(orient="list")

        vs = dcols.values()
        ks = dcols.keys()
        lvs = len(vs)

        for i in range(lvs):
            for j in range(i + 1, lvs):
                if vs[i] == vs[j]:
                    dups.append(ks[i])
                    break

    return dups


def main():
    all_data = pd.DataFrame()

    # # Creating an empty Dataframe with column names only
    # output_data = pd.DataFrame(columns=['TimePoint', 'Objects', 'IDD', 'IDA', 'IAA', 'Fc', 'EAPP'])
    #
    # time_data = pd.DataFrame(columns=['Index', 'TimePoint'])

    a = 0.12
    d = 0.02
    G = 1.159

    for f in glob.glob("data/lab*.xlsx"):
        df = pd.read_excel(f, 'Sheet1') # , header=[1]
        all_data = all_data.append(df, ignore_index=True, sort=False)

        all_data.columns = all_data.columns.str.split('.').str[0]
        # print(all_data)

        object_df = all_data.groupby(all_data.columns, axis=1)
        # print(object_df)
        for k in object_df.groups.keys():
            # print(k)
            if k != 'TimePoint':
                fc = []
                eapp = []
                for row in object_df.get_group(k).itertuples():
                    # print(row)
                    # print(row.Index, row._1, row._2, row._3)

                    # Append rows in Empty Dataframe by adding dictionaries
                    fc_val = row._2 - (a * row._3) - (d * row._1)
                    fc.append(fc_val)
                    # print(fc_val)
                    # return
                    eapp.append(fc_val / (fc_val + (G * fc_val)))

                # print(fc)
                all_data[k + '_Fc'] = fc
                all_data[k+'_EAPP'] = eapp

        # all_data['e'] = all_data['Object 0']/all_data['Object 1']
        # all_data.loc[:, 'new_col'] = all_data['A']/all_data['sum']

    # print(all_data)
    #    # now save the data frame
    writer = pd.ExcelWriter('data/output.xlsx')
    all_data.to_excel(writer, 'Sheet1', index=True)
    writer.save()


if __name__ == '__main__':
    main()

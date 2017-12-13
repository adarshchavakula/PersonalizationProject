import pandas as pd
import numpy as np
import datetime
from itertools import product

# create combinations
# need to remove duplicates to have only distinct combinations
temp = pd.DataFrame(list(product(df['userid'].drop_duplicates(),
                                 df['trackartist_weekend'].drop_duplicates())),
                   columns = ['userid', 'trackartist_weekend'])
len(temp)

# create dense matrix with all combinations
dense_data = temp.merge(df, how='left',
                      on=['userid', 'trackartist_weekend'])

# create indicator variable to signify whether a value was imputed
dense_data['missing'] = dense_data['skipped'].isnull().astype('int')

# impute missing values
# potentially calculate artist-level probability first,
# then impute that
dense_data = dense_data.fillna(1)

# delete temp dataframe to clear space
del temp

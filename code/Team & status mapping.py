# -*- coding: utf-8 -*-
"""
Created on Thu Apr 22 16:37:13 2021

@author: Tirth Patel
"""
import pandas as pd

# Main df
df1 = pd.read_excel('df1 file.xlsx')

# Df with only Player, Status and Team column
df2 = pd.read_excel('df2 file.xlsx')

# Left join
df = pd.merge(df1, df2, on = 'Player', how = 'left')

df.to_excel('output file.xlsx', index=False)
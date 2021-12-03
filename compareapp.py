import pandas as pd
import numpy as np
import streamlit as st

Path=st.sidebar.file_uploader('Excelファイル')
MODO1=st.sidebar.radio('計算方法',("割り算","引き算"))
MOOD2=st.sidebar.radio('欠損値',("削除","1に置換"))
mzmin=st.sidebar.number_input('最小m/z',value=50)
mzMAX=st.sidebar.number_input('最大m/z',value=260)
span=st.sidebar.number_input('m/z刻み',value=0.02)
option=st.sidebar.checkbox('強度に下限を設定')
if option==True:
    limit=st.sidebar.number_input('下限値',value=1000)
    
if Path is not None:
    Data=pd.ExcelFile(Path)
    Sheet_names=Data.sheet_names
    select1=st.sidebar.selectbox("基準",Sheet_names,0)
    select2=st.sidebar.selectbox("比較",Sheet_names,1)
    
    df1=pd.read_excel(Path,sheet_name=select1)
    df1=df1.drop(df1.loc[df1["m/z"]>=mzMAX].index)
    if option==True:
        df1=df1.drop(df1.loc[df1["Intensity"]<=limit].index)
    df1["label"]=df1["m/z"]-(df1["m/z"]%span)
    df1=df1.groupby("label").sum()["Intensity"]
      
    df2=pd.read_excel(Path,sheet_name=select2)
    df2=df2.drop(df2.loc[df2["m/z"]>=mzMAX].index)
    if option==True:
        df2=df2.drop(df2.loc[df2["Intensity"]<=limit].index)
    df2["label"]=df2["m/z"]-(df2["m/z"]%span)
    df2=df2.groupby("label").sum()["Intensity"]
    
    df=pd.concat([df1,df2],axis=1)
    df.columns=[select1,select2]
    if MOOD2=="削除":
        df=df.dropna()
    else:
        df=df.fillna(1)
    if MODO1=="割り算":
        df["score"]=df[select2]/df[select1]
        calc=" ÷ "
    else:
        df["score"]=df[select2]-df[select1]
        calc=" - "

    st.dataframe(df)
    

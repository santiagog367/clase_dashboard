# -*- coding: utf-8 -*-
"""
Created on Fri Jul 16 16:40:25 2021

@author: santi
"""
#Importar paquetes --> pip install "nombre del paquete"
import streamlit as st
import pandas as pd
import pydeck as pdk
import plotly.express as px
import plotly.graph_objects as go
import base64 


st.set_page_config(layout='wide')
st.markdown("<h1 style= 'text-align: center; color: #F32E07;' >Histórico de disparos en Nueva York 🗽💥</h1>", unsafe_allow_html=True)

@st.cache(persist=True) #Paraque quede guardada la tabla en la memoria caché 
def load_data(url): # para cargar siempre la misma base 
    df= pd.read_csv(url)
    df['OCCUR_DATE']= pd.to_datetime(df['OCCUR_DATE'])
    df['OCCUR_TIME']= pd.to_datetime(df['OCCUR_TIME'],format='%H:%M:%S')
    df['YEAR']=df['OCCUR_DATE'].dt.year
    df['HOUR']= df['OCCUR_TIME'].dt.hour
    df['YEARMONTH']= df['OCCUR_DATE'].dt.strftime('%y%m')
    df.columns=df.columns.map(str.lower)
    return df

# Función para descargar base de datos
def get_table_download_link(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
    href = f'<a href="data:file/csv;base64,{b64}" download="datos.csv">Descargar archivo csv</a>'
    return href


#Aplicar la función
df=load_data('NYPD_Shooting_Incident_Data__Historic_.csv')

#----------------------------------------------------------------
#Crear indicadores al inicio
c1,c2,c3,c4,c5= st.beta_columns((1,1,1,1,1))
c1.markdown("<h3 style= 'text-align: left; color: gray;' >Top Sexo</h3>", unsafe_allow_html=True)

top_perp_name=(df['perp_sex'].value_counts().index[0] )#El sexo que más aparece
top_perp_num=(round(df['perp_sex'].value_counts()/df['perp_sex'].value_counts().sum(),2)*100)[0]
top_vic_name=(df['vic_sex'].value_counts().index[0] )#El sexo que más aparece
top_vic_num=(round(df['vic_sex'].value_counts()/df['vic_sex'].value_counts().sum(),2)*100)[0]

c1.text('Atacante: ' + str(top_perp_name) + ', '+ str(top_perp_num))
c1.text('Victima: ' + str(top_vic_name) + ', '+ str(top_vic_num))

c2.markdown("<h3 style= 'text-align: left; color: gray;' >Top Raza</h3>", unsafe_allow_html=True)

top_perp_name=(df['perp_race'].value_counts().index[0] ).capitalize()#El sexo que más aparece
top_perp_num=(round(df['perp_race'].value_counts()/df['perp_race'].value_counts().sum(),2)*100)[0]
top_vic_name=(df['vic_race'].value_counts().index[0] ).capitalize()#El sexo que más aparece
top_vic_num=(round(df['vic_race'].value_counts()/df['vic_race'].value_counts().sum(),2)*100)[0]

c2.text('Atacante: ' + str(top_perp_name) + ', '+ str(top_perp_num))
c2.text('Victima: ' + str(top_vic_name) + ', '+ str(top_vic_num))

c3.markdown("<h3 style= 'text-align: left; color: gray;' >Top Edad</h3>", unsafe_allow_html=True)

top_perp_name=(df['perp_age_group'].value_counts().index[0] )#El sexo que más aparece
top_perp_num=(round(df['perp_age_group'].value_counts()/df['perp_age_group'].value_counts().sum(),2)*100)[0]
top_vic_name=(df['vic_age_group'].value_counts().index[0] )#El sexo que más aparece
top_vic_num=(round(df['vic_age_group'].value_counts()/df['vic_age_group'].value_counts().sum(),2)*100)[0]

c3.text('Atacante: ' + str(top_perp_name) + ', '+ str(top_perp_num)+'%')
c3.text('Victima: ' + str(top_vic_name) + ', '+ str(top_vic_num) + '%')

c4.markdown("<h3 style= 'text-align: left; color: gray;' >Top Barrio</h3>", unsafe_allow_html=True)

top_perp_name=(df['boro'].value_counts().index[0] ).capitalize()#El sexo que más aparece
top_perp_num=(round(df['boro'].value_counts()/df['boro'].value_counts().sum(),2)*100)[0]

c4.text('Barrio: ' + str(top_perp_name) + ', '+ str(top_perp_num))

c5.markdown("<h3 style= 'text-align: left; color: gray;' >Top Barrio</h3>", unsafe_allow_html=True)

top_perp_name=(df['hour'].value_counts().index[0] )#El sexo que más aparece
top_perp_num=(round(df['hour'].value_counts()/df['hour'].value_counts().sum(),2)*100)[0]

c5.text('Hora: ' + str(top_perp_name) + ', '+ str(top_perp_num))


#-----------------------------------------------------------------
#st.write(df) que muestre la base

#Dividir el layout en partes
c1,c2= st.beta_columns((1,1))

#Hacer código de primera columna
c1.markdown("<h3 style= 'text-align: center; color: white;' >Donde han ocurrido disparos en Nueva York </h3>", unsafe_allow_html=True)
year= c1.slider('Año en el que se presentó el suceso', 2006,2020) #Saca valor minimo y máximo y lo que hay entre ellos 
c1.map(df[df['year']==year][['latitude','longitude']])

#Hacer código de la segunda columna
c2.markdown("<h3 style= 'text-align: center; color: white;' >A que horas ocurren los disparos en Nueva York </h3>", unsafe_allow_html=True)
hour= c2.slider('hora en la que se presentó el suceso', 0,23) #Saca valor minimo y máximo y lo que hay entre ellos
df2=df[df['hour']==hour]
c2.write(pdk.Deck(
    
    map_style='mapbox://styles/mapbox/light-v9',
    initial_view_state={
        'latitude' : df2['latitude'].mean(),        
        'longitude' : df2['longitude'].mean(),        
        'zoom' : 9.5,
        'pitch' : 50},
    
    layers = [pdk.Layer(
        'HexagonLayer', ##aqui haremos las barras 
        data=df2[['latitude','longitude']],
        get_position = ['longitude', 'latitude'], # x,y
        radius=100,
        extruded=True,
        elevation_scale = True,
        elevation_range= [0,1000])]
    ))

st.markdown("<h3 style= 'text-align: center; color: white;' >¿Cómo ha sido la evolución de disparos por año?</h3>", unsafe_allow_html=True)

df3 = df.groupby(['yearmonth','boro'])[['incident_key']].count().reset_index().rename(columns={'incident_key':'Disparos'})
fig = px.line(df3, x = 'yearmonth', y ='Disparos', color = 'boro', width= 1100, height=450)

fig.update_layout(
    
    #paper_bgcolor = 'rgb(0,0,0)',
    plot_bgcolor= 'rgb(0,0,0)',
    template= 'simple_white',
    xaxis_title='<b>Año/mes<b>',
    yaxis_title='<b>Cantidad de accidentes<b>',
    legend_title_text='',
    
    legend= dict(
        orientation = 'h',
        xanchor= 'right',
        yanchor= 'bottom',
        y=1.02,
        x=0.8
        ))

st.plotly_chart(fig)

#####################################################

c3, c4, c5, c6 = st.beta_columns((1,1,1,1))

# Edad de los atacantes
c3.markdown("<h3 style = 'text-align: center; color: white;'>¿Qué edad tienen los atacantes?</h3> ",unsafe_allow_html = True)
df2 = df.groupby(['perp_age_group'])[['incident_key']].count().reset_index().sort_values('incident_key')
df2['perp_age_group'] = df2['perp_age_group'].replace({'940':'UNKNOWN',
                                                       '224':'UNKNOWN',
                                                       '1020':'UNKNOWN'})

df2['perp_age_group2'] = df2['perp_age_group'].replace({'<18':'1',
                                                       '18-24':'2',
                                                       '25-44':'3',
                                                       '45-64':'4',
                                                       '65+': '5',
                                                       'UNKNOWN':'6'})

df2['perp_age_group'] = df2['perp_age_group'].replace({'UNKNOWN':'N/A'})

# hacer gráfica
df2 = df2.sort_values('perp_age_group2', ascending = False)
fig = px.bar(df2, x = 'incident_key', y ='perp_age_group', orientation = 'h',
             width = 340, height = 310)

fig.update_layout(

    template = 'simple_white',
    plot_bgcolor = 'rgba(0,0,0,0)',
    xaxis_title = '<b>Atacante<b>',
    yaxis_title = '<b>Edades<b>',
    legend_title_text = '',

    )

c3.plotly_chart(fig)

##########################################################
# Edad de las victimas 
c4.markdown("<h3 style = 'text-align: center; color: white;'>¿Qué edad tienen las victimas?</h3> ",unsafe_allow_html = True)
df2 = df.groupby(['vic_age_group'])[['incident_key']].count().reset_index().sort_values('incident_key')
df2['vic_age_group'] = df2['vic_age_group'].replace({'940':'UNKNOWN',
                                                       '224':'UNKNOWN',
                                                       '1020':'UNKNOWN'})

df2['vic_age_group2'] = df2['vic_age_group'].replace({'<18':'1',
                                                       '18-24':'2',
                                                       '25-44':'3',
                                                       '45-64':'4',
                                                       '65+': '5',
                                                       'UNKNOWN':'6'})

df2['vic_age_group'] = df2['vic_age_group'].replace({'UNKNOWN':'N/A'})

# hacer gráfica
df2 = df2.sort_values('vic_age_group2', ascending = False)
fig = px.bar(df2, x = 'incident_key', y ='vic_age_group', orientation = 'h',
             width = 340, height = 310)

fig.update_layout(

    template = 'simple_white',
    plot_bgcolor = 'rgba(0,0,0,0)',
    xaxis_title = '<b>Victima<b>',
    yaxis_title = '<b>Edades<b>',
    legend_title_text = '',

    )

c4.plotly_chart(fig)

#######################################################
c5.markdown("<h3 style = 'text-align: center; color: white;'>¿Cuál es el sexo del atacante?</h3> ",unsafe_allow_html = True)
df2= df.groupby(['perp_sex'])[['incident_key']].count().reset_index()
fig= px.pie(df2,values='incident_key',names='perp_sex',
            width=300,height=300)

fig.update_layout(
    
    #paper_bgcolor = 'rgb(0,0,0)',
    plot_bgcolor= 'rgb(0,0,0)',
    template= 'simple_white',
    
    legend= dict(
        orientation = 'h',
        xanchor= 'center',
        yanchor= 'bottom',
        y=-0.4,
        x=0.5
        ))
c5.plotly_chart(fig)
#######################################################
c6.markdown("<h3 style = 'text-align: center; color: white;'>¿Cuál es el sexo de la victima?</h3> ",unsafe_allow_html = True)
df2= df.groupby(['vic_sex'])[['incident_key']].count().reset_index()
fig= px.pie(df2,values='incident_key',names='vic_sex',
            width=300,height=300)

fig.update_layout(
    
    #paper_bgcolor = 'rgb(0,0,0)',
    plot_bgcolor= 'rgb(0,0,0)',
    template= 'simple_white',
    
    legend= dict(
        orientation = 'h',
        xanchor= 'center',
        yanchor= 'bottom',
        y=-0.4,
        x=0.5
        ))
c6.plotly_chart(fig)
#########################################################
st.markdown("<h3 style = 'text-align: center; color: white;'>Evolución de disparos por años en las horas con más y menos accidentes</h3> ",unsafe_allow_html = True)

#df[df['hour'].isin([23,9])] # Filtrar DF
#df2=df2.groupby(['year','hour'])[['incident_key']].count().reset_index()
#df2['hour']= df2['hour'].astype('category') #para decirle que hora es categ
#df2['year']= df2['year'].astype('category')

#fig= px.bar(df2,x='year',y='incident_key', color='hour', barmode='group',
#            width= 1150, height=450)

#st.plotly_chart(fig)
#Falta

###########################################
# obtener datos
#if st.checkbox('Obtener datos por fecha y barrio', False):
#  
#    
#  df2 = df.groupby(['occur_date','boro'])[['incident_key']].count().reset_index().rename(columns ={'boro':'Barrio','occur_date':'Fecha','incident_key':'Cantidad'})
#  df2['Fecha'] = df2['Fecha'].dt.date
#  
#  
#  
#  fig = go.Figure(data=[go.Table(
#        header=dict(values=list(df2.columns),
#        fill_color='lightgrey',
#        line_color='darkslategray'),
#        
#        
#        cells=dict(values=[df2.Fecha, df2.Barrio, df2.Cantidad],fill_color='white',line_color='lightgrey'))
#       ])
#  fig.update_layout(width=500, height=450)
#
#  st.write(fig)


# Hacer un checkbox
if st.checkbox('Obtener datos por fecha y barrio', False):
    
    # Código para generar el DataFrame
    df2 = df.groupby(['occur_date','boro'])[['incident_key']].count().reset_index().rename(columns ={'boro':'Barrio','occur_date':'Fecha','incident_key':'Cantidad'})
    df2['Fecha'] = df2['Fecha'].dt.date
    
    # Código para convertir el DataFrame en una tabla plotly resumen
    fig = go.Figure(data=[go.Table(
        header=dict(values=list(df2.columns),
        fill_color='lightgrey',
        line_color='darkslategray'),
        cells=dict(values=[df2.Fecha, df2.Barrio, df2.Cantidad],fill_color='white',line_color='lightgrey'))
       ])
    fig.update_layout(width=500, height=450)

# Enviar tabla a streamlit
    st.write(fig)
    
#generar link de descarga 
st.markdown(get_table_download_link(df2),unsafe_allow_html = True)
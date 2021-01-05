import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly import tools
import plotly.offline as py
import plotly.express as px
import matplotlib.pyplot as plt
from plotly.subplots import make_subplots

st.set_page_config(  # Alternate names: setup_page, page, layout
	layout="wide",  # Can be "centered" or "wide". In the future also "dashboard", etc.  # Can be "auto", "expanded", "collapsed"
	page_title=None,  # String or None. Strings get appended with "• Streamlit".
	page_icon=None,  # String, anything supported by st.image, or None.
)




df=pd.read_csv('Region.csv')
df1=pd.read_csv('data_hiv.csv')
incidence=pd.read_csv('incidence.csv')
df_child=pd.read_csv('HIV_Epidemiology_Children_Adolescents_2020.csv')

sex=pd.read_csv('data_hiv_sex.csv')

from PIL import Image
image = Image.open('unnamed.jpg')

st.sidebar.title('Global epidemic - HIV')

st.sidebar.markdown("Human Immunodeficency Virus (HIV) is a virus that attacks cells that help the body fight infection. There's no cure, but it is treatable with medicine.")
st.sidebar.markdown("This dashboard will give us the status of HIV across the world ")

st.sidebar.subheader('Dashboard Password 🔑')
password=st.sidebar.text_input("Please enter the password", value="", type="password")


st.sidebar.image(image)

def main():

	c1, c2, c3 = st.beta_columns([3,5,3])
	c2.title('Trends in the HIV epidemic, 1999-2019')
	from PIL import Image
	image1 = Image.open('people.png')
	image2 = Image.open('queue.png')
	image3 = Image.open('people.png')
	image4= Image.open('ratio.png')
	st.empty()
	st.header('Breakdown of global HIV cases')



	col1, col2, col3, col4, col6, col5  =st.beta_columns(6)

	selected_year=col5.selectbox('Filter by Year',
		(list(range(1999,2020,1))))
	col1.image(image1)
	df_filt = df[(df['Region']=='Global') & (df['year']==selected_year) & (df['type']=='People living with HIV')]
	df_filt.reset_index(drop=True, inplace=True)
	result=df_filt.at[0,'value']
	col1.header(f"{result:,d}")
	col1.markdown('estimated number of people living with HIV')
	col2.image(image2)
	df_filt_1 = df[(df['Region']=='Global') & (df['year']==selected_year) & (df['type']=='New HIV infections')]
	df_filt_1.reset_index(drop=True, inplace=True)
	result1=df_filt_1.at[0,'value']
	col2.header(f"{result1:,d}")
	col2.markdown('people were newly infected with HIV ')
	col3.image(image3)
	df_filt_2 = df[(df['Region']=='Global') & (df['year']==selected_year)& (df['type']=='AIDS-related deaths')]
	df_filt_2.reset_index(drop=True, inplace=True)
	result2=df_filt_2.at[0,'value']
	col3.header(f"{result2:,d}")
	col3.markdown('people died of HIV-related causes')

	col4.image(image4)
	col4.header(round(result2/result,2)*100)
	col4.markdown('Death-Ratio')

	col6.image(image4)
	filt_2 = incidence[(incidence['Region']=='Global') & (incidence['year']==selected_year)]
	filt_2.reset_index(drop=True, inplace=True)
	number=filt_2.at[0,'value']
	col6.header(number*100)
	col6.markdown('Incidence by 1000 Population')

	my_expander = st.beta_expander("Check HIV over the years", expanded=False)
	with my_expander:
		select_region=st.selectbox('Select Area:', (list((df.Region.unique()))))
		data=df[df['Region']==select_region]

		x = data['year']

		type1= data[data['type']=='People living with HIV']
		y=type1['value']

		type2= data[data['type']=='New HIV infections']
		y1=type2['value']

		type3= data[data['type']=='AIDS-related deaths']
		y2=type3['value']

		# Create traces
		fig6 = go.Figure()
		fig6.add_trace(go.Scatter(x=x, y=y, name='People living with HIV',
								 line=dict(color='#d30000', width=4),mode='lines+markers'))

		fig6.add_trace(go.Scatter(x=x, y=y1,
							name='New HIV infections', line=dict(color='#d21f3c', width=4),mode='lines+markers'))
		fig6.add_trace(go.Scatter(x=x, y=y2, name='AIDS-related deaths', line=dict(color='#7c0a02',
																				  width=4),mode='lines+markers'))
		fig6.update_layout(title_text='Trends in the HIV epidemic, 2000-2019',plot_bgcolor="#FFF", xaxis=dict(

				linecolor="#BCCCDC",  # Sets color of X-axis line
				showgrid=False  # Removes X-axis grid lines
			),
			yaxis=dict(
				title="Numbers",
				linecolor="#BCCCDC",  # Sets color of Y-axis line
				showgrid=False), width=1000)  # Removes Y-axis grid lines )

		st.plotly_chart(fig6)

	colum1, colum2 = st.beta_columns([6,1])
	colum1.header('Demographics')

	selected_type=colum2.selectbox('Filter by Type',
		(list((df1.type.unique()))))


		#Visuals
	viz1, viz2 = st.beta_columns([2,3])

	data_viz=df1[(df1['Region']=='Global') & (df1['type']==selected_type) & (df1['year']==selected_year) ]
	fig4 = px.bar(data_viz, y="Age", x="value", color='Age',color_discrete_sequence=px.colors.sequential.RdBu,labels={'value':'Number of cases'},
		 width=800, orientation ='h')
	fig4.update_layout(title_text='HIV Trends by Age category',plot_bgcolor="#FFF", xaxis=dict(
	title="Numbers",
	linecolor="#BCCCDC",  # Sets color of X-axis line
	showgrid=False  # Removes X-axis grid lines
),
yaxis=dict(
	title="Age Category",
	linecolor="#BCCCDC",  # Sets color of Y-axis line
	showgrid=False))  # Removes Y-axis grid lines )
	fig4.update_layout(showlegend=False)
	viz1.plotly_chart(fig4)

	data_year = df[(df['year']==selected_year) & (df['type']==selected_type) & (df['Region']!='Global') ]
	fig = px.bar(data_year, x='Region', y='value', title="HIV by Region",hover_data=['year', 'value'],
		color='value',color_continuous_scale='Reds',text='value',height=650, labels={'value':'Number of cases'},)
	fig.update_layout(barmode='stack', xaxis={'categoryorder':'total descending'},plot_bgcolor="#FFF")
	fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
	fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide', xaxis=dict(
	title="Regions",
	linecolor="#BCCCDC",  # Sets color of X-axis line
	showgrid=False  # Removes X-axis grid lines
),
yaxis=dict(
	title="Numbers",
	linecolor="#BCCCDC",  # Sets color of Y-axis line
	showgrid=False))
	fig.update_layout(showlegend=False)
	viz2.plotly_chart(fig, use_column_width=True)

	df_filter=sex[(sex['Region']=='Global') & (sex['type']==selected_type) & (sex['year']==selected_year) ]
	fig3 = px.pie(df_filter, values='value', names='Sex', hole=.3,color_discrete_sequence=px.colors.sequential.RdBu)
	fig3.update_traces(textposition='inside', textinfo='percent+label')
	fig3.update_layout(showlegend=False)
	viz1.plotly_chart(fig3, use_column_width=True)




	c1, c2 =st.beta_columns([4,1])
	c1.title('While there has been promising progress in the HIV response, children continue to be affected by the epidemic')
	from PIL import Image
	image = Image.open('children.png')
	c2.image(image)
	year=c2.selectbox('Select a Year',
			(list(range(1999,2020,1))))

	co1, co2, co3 = st.beta_columns(3)

	image5= Image.open('child.png')
	co1.image(image5)
		#data
	df_filt = df_child[(df_child['Country']=='Global') & (df_child['Year']==year) & (df_child['Indicator']=='Estimated number of people living with HIV') &
			 (df_child['Age']== 'Age 0-9' ) &  (df_child['Sex']== 'Both' )]
	df_filt.reset_index(drop=True, inplace=True)
	result=df_filt.at[0,'Value']

	filt = df_child[(df_child['Country']=='Global') & (df_child['Year']==year) & (df_child['Indicator']=='Estimated number of people living with HIV') &
			 (df_child['Age']== 'Age 10-19' ) & (df_child['Sex']== 'Both' ) ]
	filt.reset_index(drop=True, inplace=True)
	res=filt.at[0,'Value']

	co1.header('Estimated number of children living with HIV')
	cols = st.beta_columns(6)
	cols[0].write("Children aged 0–9: ")
	cols[1].write(result)
	cols[0].write("Adolescents aged 10–19 :")
	cols[1].write(res)

	image6= Image.open('plus.png')
	#data
	filt1 = df_child[(df_child['Country']=='Global') & (df_child['Year']==year) & (df_child['Indicator']=='Estimated number of annual new HIV infections') &
		 (df_child['Age']== 'Age 0-9' ) & (df_child['Sex']== 'Both' )]
	filt1.reset_index(drop=True, inplace=True)
	result11=filt1.at[0,'Value']

	fil = df_child[(df_child['Country']=='Global') & (df_child['Year']==year) & (df_child['Indicator']=='Estimated number of annual new HIV infections') &
		 (df_child['Age']== 'Age 10-19' ) & (df_child['Sex']== 'Both' ) ]
	fil.reset_index(drop=True, inplace=True)
	res1=fil.at[0,'Value']
	co2.image(image6)
	co2.header('Estimated number of annual new HIV infections')

	cols[2].write(result11)

	cols[2].write(res1)

	image7= Image.open('dead.png')
	#data
	filt1 = df_child[(df_child['Country']=='Global') & (df_child['Year']==year) & (df_child['Indicator']=='Estimated number of annual AIDS-related deaths') &
					 (df_child['Age']== 'Age 0-9' )]
	filt1.reset_index(drop=True, inplace=True)
	result11=filt1.at[0,'Value']

	fil = df_child[(df_child['Country']=='Global') & (df_child['Year']==year) & (df_child['Indicator']=='Estimated number of annual AIDS-related deaths') &
					 (df_child['Age']== 'Age 10-19' )]
	fil.reset_index(drop=True, inplace=True)
	res1=fil.at[0,'Value']
	co3.image(image7)
	co3.header('Estimated number of annual AIDS-related deaths')

	cols[4].write(result11)

	cols[4].write(res1)

	expander = st.beta_expander("Global trends", expanded=False)
	with expander:
		viz=df_child[(df_child['Country']=='Global') &
			       (df_child['Indicator']=='Estimated number of annual new HIV infections') &
			      (df_child['Sex']=='Both') & (df_child['Year'] >1999)]
		filter_age = ['Age 0-9', 'Age 10-19']
		viz=viz[viz.Age.isin(filter_age)]
		fig55 = px.line(viz, x="Year", y="Value", color='Age',color_discrete_sequence=px.colors.sequential.RdBu)
		fig55.update_layout(title_text='Number of annual new HIV infections among children and adolescents',plot_bgcolor="#FFF", xaxis=dict(

							linecolor="#BCCCDC",  # Sets color of X-axis line
							showgrid=False  # Removes X-axis grid lines
						),
						yaxis=dict(
							title="Numbers",
							linecolor="#BCCCDC",  # Sets color of Y-axis line
							showgrid=False), width=1000)  # Removes Y-axis grid lines )

		fig55.update_layout(showlegend=False)
		viz2=df_child[(df_child['Country']=='Global') &
			       (df_child['Indicator']=='Estimated number of annual AIDS-related deaths') &
			      (df_child['Sex']=='Both') & (df_child['Year'] >1999)]
		viz2=viz2[viz2.Age.isin(filter_age)]
		fig33 = px.line(viz, x="Year", y="Value", color='Age',color_discrete_sequence=px.colors.sequential.RdBu)
		fig33.update_layout(title_text='Number of AIDS-related deaths among children and adolescents',plot_bgcolor="#FFF", xaxis=dict(

							linecolor="#BCCCDC",  # Sets color of X-axis line
							showgrid=False  # Removes X-axis grid lines
						),
						yaxis=dict(
							title="Numbers",
							linecolor="#BCCCDC",  # Sets color of Y-axis line
							showgrid=False), width=1000)  # Removes Y-axis grid lines )

		fig33.update_layout(showlegend=False)
		st.plotly_chart(fig55)
		st.plotly_chart(fig33)




if password=='condomready':
    main()
elif password !='condomready':
        st.error("Authentication failed. Please verify your password and try again. ")

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

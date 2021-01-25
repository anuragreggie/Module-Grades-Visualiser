import streamlit as st
import pandas as pd
import plotly.express as px


# Function to read the three csv files.
@st.cache
def load_data():
    departments = pd.read_csv('data/departments.csv')
    master = pd.read_csv('data/master.csv')
    levels = pd.read_csv('data/levels.csv')

    subjects_column = master['Department']
    subjects = subjects_column.unique()

    return departments, master, levels, subjects


if __name__ == '__main__':
    # Load in the data frames.
    departments, master, levels, subjects = load_data()

    # Create title for app using 3 columns.
    # Middle column is empty but stops text from overlapping over image with a narrow viewport.
    col1, mid, col2 = st.beta_columns([1, 1, 20])
    with col1:
        st.image('images/crest.png', width=60)
    with col2:
        st.markdown("## St Andrews Module Grades Visualisation")

    # Creating pages.
    st.sidebar.title("Navigation")
    page = st.sidebar.radio('Select a page:', ('Home', 'Filter Data', 'Data Frames'))
    st.sidebar.subheader("Search for a specific module")
    user_input = st.sidebar.text_input("Type the module code here").upper()

    if user_input:
        result = master.loc[
            master['Code'] == user_input]  # Try to get a pandas series that contains details for that module.
        # If the series is empty module does not exist.
        if result.empty:
            st.sidebar.error("There are no records for this module😞")
        else:
            st.sidebar.info(f"The average grade is {result.iloc[0][3]}")

    st.sidebar.write("")

    my_expander = st.sidebar.beta_expander("How was the data gathered?")
    with my_expander:
        st.write(
            "All the data was gathered from public FOI requests between 2012-2019. "
            "The graphs plotted only contain data from modules where the scores were reported. "
            "Detailed information about this and data on grades for individual years is available at this [link.]"
            "(https://github.com/Leader-board/St-Andrews/blob/master/moduledatabase/St%20Andrews%20Module%20database.pdf)")

    if page == 'Home':

        st.markdown(">  ⬅️ Click the sidebar to do a custom search and navigate")
        
        tip = st.beta_expander("Tip for mobile users")
        with tip:
            st.info("📱 On mobile it is recommended to use landscape mode to easily view graphs.")

        for i in range(2):
            st.write(" ")
        st.subheader("Summary Statistics")
        excluded_df = departments[:-1]  # Remove the overall grades for this graph.
        plotly_fig1 = px.bar(excluded_df, x=excluded_df['Department'], y=excluded_df['Average'],
                             title='Average grades by department',
                             labels=dict(x="Department", y="Average Grade"))
        plotly_fig1.update_traces(marker_color='rgb(221,55,55)')
        # Centre the plot title.
        plotly_fig1.update_layout(
            title={
                'text': 'Average grades by department',
                'y': 0.9,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'})
        st.plotly_chart(plotly_fig1)

        plotly_fig2 = px.bar(levels, x='Level', y='Average',
                             hover_data=['Level', 'Average'], color='Module Count',
                             labels={"Module Count": "Number of modules used"}, height=400,
                             color_continuous_scale=["rgb(221,55,55)", "rgb(137,164,204)", "rgb(30,77,155)"])
        # Centre the plot title.
        plotly_fig2.update_layout(
            title={
                'text': 'Average grades by level',
                'y': 0.9,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'},
            hoverlabel=dict(bgcolor="white", font_size=16))
        st.plotly_chart(plotly_fig2)

        # Use markdown to place the badge at the bottom.
        st.markdown("<div align='center'><br>"
                    "<img src='https://img.shields.io/badge/MADE%20WITH-PYTHON%20-rgb(221,55,55)?style=for-the-badge'"
                    "alt='API stability' height='25'/>"
                    "<img src='https://img.shields.io/badge/DASHBOARDING%20WITH-Streamlit-rgb(30,77,155)?style=for-the-badge'"
                    "alt='API stability' height='25'/></div>", unsafe_allow_html=True)

    elif page == 'Filter Data':

        st.markdown("## **Filter Data**")
        st.subheader("Pick a subject to display data for")
        subject_dropdown = st.selectbox(label="Subject choice", options=subjects)  # Drop down to pick subjects.
        levels_selection = st.multiselect(label="Specify a level if required",  # Multiselect to pick levels.
                                          options=levels['Level'])

        st.subheader("Filtered results")
        master = master[master['Department'] == subject_dropdown]  # Select all data for that subject.
        if levels_selection:
            # If they have specified levels then select all data corresponding to that choice.
            master1 = master[master['Level'].isin(levels_selection)]
        else:
            master1 = master

        # If data exists then plot the graph.
        if not master1.empty:
            plotly_fig = px.bar(x=master1['Code'], y=master1['Average Grade'],
                                title='Average grades for' + str(subject_dropdown),
                                labels=dict(x="Module Code", y="Average Grade"))
            # Centre the plot title.
            plotly_fig.update_layout(
                title={
                    'text': 'Average grades for' + str(subject_dropdown),
                    'y': 0.9,
                    'x': 0.5,
                    'xanchor': 'center',
                    'yanchor': 'top'})
            plotly_fig.update_traces(marker_color='rgb(30,77,155)')
            st.plotly_chart(plotly_fig)
        else:
            st.error("No modules with this criteria have grades recorded 😞")

    elif page == 'Data Frames':
        st.markdown("## **Data Frames**")

        levels_expander = st.beta_expander("Averages By Level", expanded=True)
        with levels_expander:
            st.write(levels)

        department_expander = st.beta_expander("Averages By Department", expanded=True)
        with department_expander:
            st.write(departments)

        master_expander = st.beta_expander("All Data", expanded=True)
        with master_expander:
            st.write(master)

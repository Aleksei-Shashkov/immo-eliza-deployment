import streamlit as st
import pandas as pd

# Set the title and overall layout
st.set_page_config(
    page_title="Possum Dataset Explorer",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Data Loading ---
# Access the uploaded file content.
def load_data():
    """Loads the possum dataset."""
    try:
        df = pd.read_csv("./data/possum.csv")
        return df.dropna() # Drop rows with missing values for cleaner visualization
    except Exception as e:
        st.error(f"Error loading data: {e}. Please ensure 'possum.csv' is available.")
        return pd.DataFrame()

df = load_data()


# --- Main Page Content ---
st.title("🦘 Possum Morphological Data Explorer (Streamlit Native)")
st.markdown("Explore key measurements and demographic data from the possum dataset using **Streamlit's built-in charts**.")
st.write(f"Dataset Size: **{len(df)}** rows and **{len(df.columns)}** columns.")

# --- Sidebar Filters ---
st.sidebar.header("Data Filters & Controls")

# 1. Population Filter
all_populations = df['pop'].unique().tolist()
selected_populations = st.sidebar.multiselect(
    "Select Population Groups:",
    options=all_populations,
    default=all_populations
)

# 2. Age Slider
min_age = int(df['age'].min())
max_age = int(df['age'].max())
age_range = st.sidebar.slider(
    "Select Age Range (Years):",
    min_value=min_age,
    max_value=max_age,
    value=(min_age, max_age),
    step=1
)

# Apply filters
df_filtered = df[
    df['pop'].isin(selected_populations) &
    (df['age'] >= age_range[0]) &
    (df['age'] <= age_range[1])
]

st.sidebar.write(f"Data points after filtering: **{len(df_filtered)}**")

# Show raw data option
if st.sidebar.checkbox('Show Raw Data Table'):
    st.subheader("Raw Data Table")
    st.dataframe(df_filtered)

# Check if the filtered dataframe is empty
if df_filtered.empty:
    st.warning("No data matches the selected filters. Please adjust your selections.")
    st.stop()

# --- Visualization Section (Main Area) ---
st.header("Visual Analysis (Native Streamlit Charts)")

# 1. Scatter Plot: Relationship between two measurements
st.subheader("1. Relationship Between Two Morphological Measurements")
col1, col2 = st.columns(2)

measurements = ['head_l', 'skull_w', 'total_l', 'tail_l']

with col1:
    x_col = st.selectbox("X-axis (Measurement):", options=measurements, index=0, key='x_scatter')
with col2:
    y_col = st.selectbox("Y-axis (Measurement):", options=measurements, index=1, key='y_scatter')

# Prepare data for st.scatter_chart (only numerical columns needed for chart)
chart_data = df_filtered[[x_col, y_col]].copy()

# Rename columns temporarily for cleaner chart labels in Streamlit
chart_data.columns = [
    x_col.replace('_', ' ').title() + ' (X)',
    y_col.replace('_', ' ').title() + ' (Y)'
]

st.scatter_chart(chart_data)
st.caption(f"Scatter chart showing {x_col.replace('_', ' ').title()} vs. {y_col.replace('_', ' ').title()}. Native Streamlit charts do not support categorical coloring.")


st.markdown("---")


# 2. Bar Chart: Mean Total Length by Group
st.subheader("2. Mean Total Length by Sex and Population")

# Calculate the mean total_l grouped by pop and sex
# This aggregation is necessary because native charts are best suited for pre-calculated data
mean_total_l = df_filtered.groupby(['pop', 'sex'])['total_l'].mean().reset_index()

# Combine 'pop' and 'sex' for a single categorical axis
mean_total_l['Group'] = mean_total_l['pop'] + ' (' + mean_total_l['sex'].str.upper() + ')'
mean_total_l = mean_total_l.set_index('Group')

# Use st.bar_chart
st.bar_chart(mean_total_l['total_l'])
st.caption("Bar chart showing the average total length for each population and sex group.")

st.markdown("---")
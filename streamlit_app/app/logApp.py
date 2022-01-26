from app_utils import create_3d_plot, DBHelper
import streamlit as st

DB_PATH = "/tmp/cs.db"

st.title("Crazyswarm Logging")
db = DBHelper()

# ---------------------------------------- Sidebar --------------------------------------------------
st.sidebar.image("logo.png", use_column_width=True)
st.sidebar.text(" ")
st.sidebar.text(" ")
st.sidebar.text(" ")


# let the user choose a past session id
session_ids = db.get_unique_session_ids()
session_oi = st.sidebar.selectbox('Select past logging session', session_ids)

# buttons if a new session should be started
plot_option_button = st.sidebar.button(label="Show plotting options",
                                       help="click here to further select crazyflies etc")

# workaround to get session variables:
if 'start_button_clicked' not in st.session_state:
    st.session_state.start_button_clicked = False

if 'end_button_clicked' not in st.session_state:
    st.session_state.end_button_clicked = False

if 'vis_button_clicked' not in st.session_state:
    st.session_state.vis_button_clicked = False


# --------------------------------Main Panel ------------------------------------------
if plot_option_button:
    st.session_state.vis_button_clicked = True

if st.session_state.vis_button_clicked and session_oi:
    # print the matadata of the respective session
    st.header("Metadata:")
    st.text("TODO: Metadata here") # TODO: print the metadata of the session
    crazyflies = db.get_all_cfs_in_session(session_oi)
    selected_cfs = st.multiselect(label="select crazyflies of interest:", options=crazyflies)

    # get data of interest from database
    session_data = db.get_cfs_data_from_session(session_oi, crazyflies)

    # output plot
    st.header("Plot:")
    if st.button("Show Plot"):
        filtered_data = session_data[session_data.crazyflie_id.isin(selected_cfs)]

        if not filtered_data.empty:
            fig = create_3d_plot(data=filtered_data)
            st.plotly_chart(fig, use_container_width=True)

        else:
            st.text("No session data, are you sure you selected crazyflies?")

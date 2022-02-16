from app_utils import create_3d_plot, DBHelper
import streamlit as st

DB_PATH = "/tmp/cs.db"

st.title("Crazyswarm Logging")
db = DBHelper()

# ---------------------------------------- Sidebar --------------------------------------------------

st.sidebar.image("app/logo.png", use_column_width=True)
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
if 'plot_button_clicked' not in st.session_state:
    st.session_state.plot_button_clicked = False

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

    # again workaround, to generate session variables
    plot_button = st.button("Show Plot")
    if plot_button:
        st.session_state.plot_button_clicked = True

    if st.session_state.plot_button_clicked:
        filtered_data = session_data[session_data.crazyflie_id.isin(selected_cfs)]

        if not filtered_data.empty:
            # timeslider
            filtered_data.ts = filtered_data.ts.apply(lambda x: db.timestamp_to_ms(x))
            time_col = filtered_data.timestamp
            min_time = min(time_col)
            max_time = max(time_col)
            time_oi = st.slider(max_value=max_time - min_time,
                                min_value=0,
                                value=max_time - min_time,
                                label="Time Threshold (miliseconds from start)",
                                )
            filtered_data = filtered_data.loc[time_col < (time_oi + min_time)]
            fig = create_3d_plot(data=filtered_data)
            st.plotly_chart(fig, use_container_width=True)



        else:
            st.text("No session data, are you sure you selected crazyflies?")

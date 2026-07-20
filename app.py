import streamlit as st
import streamlit.components.v1 as components


# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------
st.set_page_config(
    page_title="Carpla Service Dashboard",
    page_icon="🚘",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ---------------------------------------------------------
# WORKSHOP INFORMATION
# Replace or add workshops later
# Coordinates are examples and can be adjusted
# ---------------------------------------------------------
WORKSHOPS = {
    "Hà Nội": {
        "latitude": 21.0285,
        "longitude": 105.8542,
        "branch": "Chi nhánh Hà Nội",
        "workshop": "Carpla Service Hà Nội",
    },
    "Hải Phòng": {
        "latitude": 20.8449,
        "longitude": 106.6881,
        "branch": "Chi nhánh Hải Phòng",
        "workshop": "Carpla Service Hải Phòng",
    },
    "Đà Nẵng": {
        "latitude": 16.0544,
        "longitude": 108.2022,
        "branch": "Chi nhánh Miền Trung",
        "workshop": "Carpla Service Đà Nẵng",
    },
    "TP. Hồ Chí Minh": {
        "latitude": 10.7769,
        "longitude": 106.7009,
        "branch": "Chi nhánh TP. Hồ Chí Minh",
        "workshop": "Carpla Service Tân Cảng",
    },
    "Cần Thơ": {
        "latitude": 10.0452,
        "longitude": 105.7469,
        "branch": "Chi nhánh Cần Thơ",
        "workshop": "Carpla Service Cần Thơ",
    },
}


# ---------------------------------------------------------
# SESSION STATE
# ---------------------------------------------------------
if "selected_location" not in st.session_state:
    st.session_state.selected_location = None


# ---------------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------------
st.markdown(
    """
    <style>
        .stApp {
            background:
                radial-gradient(
                    circle at top left,
                    rgba(25, 72, 116, 0.12),
                    transparent 34%
                ),
                linear-gradient(
                    180deg,
                    #f4f7fa 0%,
                    #ffffff 55%,
                    #eef3f7 100%
                );
        }

        .block-container {
            max-width: 1450px;
            padding-top: 1.2rem;
            padding-bottom: 3rem;
        }

        header[data-testid="stHeader"] {
            background: transparent;
        }

        #MainMenu {
            visibility: hidden;
        }

        footer {
            visibility: hidden;
        }

        .hero-card {
            background: rgba(255, 255, 255, 0.94);
            border: 1px solid rgba(23, 62, 94, 0.12);
            border-radius: 22px;
            padding: 22px 32px;
            box-shadow: 0 16px 40px rgba(20, 52, 78, 0.10);
            margin-bottom: 20px;
            text-align: center;
        }

        .hero-title {
            font-size: 34px;
            font-weight: 800;
            color: #173e5e;
            margin: 4px 0 6px 0;
        }

        .hero-subtitle {
            font-size: 16px;
            color: #657786;
            margin: 0;
        }

        .section-title {
            font-size: 24px;
            font-weight: 750;
            color: #173e5e;
            margin-top: 12px;
            margin-bottom: 4px;
        }

        .section-description {
            color: #71808d;
            margin-bottom: 14px;
        }

        .dashboard-card {
            background: #ffffff;
            border: 1px solid #dfe8ee;
            border-radius: 18px;
            padding: 22px;
            box-shadow: 0 10px 28px rgba(25, 54, 76, 0.08);
            margin-top: 12px;
        }

        .selected-location {
            font-size: 27px;
            font-weight: 800;
            color: #173e5e;
        }

        .selected-detail {
            font-size: 15px;
            color: #687987;
            margin-top: 5px;
        }

        div.stButton > button {
            border-radius: 12px;
            border: 1px solid #c7d6df;
            background: #ffffff;
            color: #173e5e;
            font-weight: 650;
            min-height: 44px;
        }

        div.stButton > button:hover {
            border-color: #173e5e;
            background: #edf4f8;
            color: #173e5e;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# HEADER AND LOGO
# ---------------------------------------------------------
logo_col_1, logo_col_2, logo_col_3 = st.columns([1.8, 1, 1.8])

with logo_col_2:
    try:
        st.image("carpla_logo.png", use_container_width=True)
    except Exception:
        st.markdown(
            """
            <div style="
                text-align:center;
                font-size:36px;
                font-weight:900;
                color:#173e5e;
                padding:10px;
            ">
                CARPLA
            </div>
            """,
            unsafe_allow_html=True,
        )

st.markdown(
    """
    <div class="hero-card">
        <div class="hero-title">CARPLA SERVICE PERFORMANCE DASHBOARD</div>
        <p class="hero-subtitle">
            Select a location on the Vietnam map to view workshop performance.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# MAP SECTION
# ---------------------------------------------------------
st.markdown(
    '<div class="section-title">Carpla Service Network</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="section-description">'
    'Click a red location pin, then select “Open dashboard”.'
    '</div>',
    unsafe_allow_html=True,
)


# Build markers for the HTML map
markers_javascript = ""

for location_name, information in WORKSHOPS.items():
    safe_name = location_name.replace("'", "\\'")
    safe_workshop = information["workshop"].replace("'", "\\'")
    safe_branch = information["branch"].replace("'", "\\'")

    markers_javascript += f"""
        L.marker(
            [{information["latitude"]}, {information["longitude"]}],
            {{icon: redIcon}}
        )
        .addTo(map)
        .bindPopup(`
            <div style="font-family:Arial; min-width:210px;">
                <div style="
                    font-size:17px;
                    font-weight:700;
                    color:#173e5e;
                    margin-bottom:5px;
                ">
                    {safe_name}
                </div>

                <div style="
                    font-size:13px;
                    color:#5f7180;
                    margin-bottom:3px;
                ">
                    {safe_branch}
                </div>

                <div style="
                    font-size:13px;
                    color:#5f7180;
                    margin-bottom:12px;
                ">
                    {safe_workshop}
                </div>

                <div style="
                    font-size:12px;
                    color:#173e5e;
                    font-weight:700;
                ">
                    Use the location buttons below the map to open this dashboard.
                </div>
            </div>
        `);
    """


map_html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8" />

    <link
        rel="stylesheet"
        href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"
    />

    <script
        src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js">
    </script>

    <style>
        html,
        body {{
            margin: 0;
            padding: 0;
            background: transparent;
        }}

        #map {{
            width: 100%;
            height: 620px;
            border-radius: 18px;
        }}
    </style>
</head>

<body>
    <div id="map"></div>

    <script>
        const map = L.map(
            "map",
            {{
                zoomControl: true,
                scrollWheelZoom: false
            }}
        ).setView([16.2, 107.8], 5.2);

        L.tileLayer(
            "https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png",
            {{
                maxZoom: 19,
                attribution: "&copy; OpenStreetMap contributors"
            }}
        ).addTo(map);

        const redIcon = new L.Icon({{
            iconUrl:
                "https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-red.png",
            shadowUrl:
                "https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png",
            iconSize: [25, 41],
            iconAnchor: [12, 41],
            popupAnchor: [1, -34],
            shadowSize: [41, 41]
        }});

        {markers_javascript}
    </script>
</body>
</html>
"""

components.html(
    map_html,
    height=640,
    scrolling=False,
)


# ---------------------------------------------------------
# LOCATION BUTTONS
# Streamlit buttons reliably open each dashboard
# ---------------------------------------------------------
st.markdown(
    '<div class="section-title">Select a workshop</div>',
    unsafe_allow_html=True,
)

location_names = list(WORKSHOPS.keys())
button_columns = st.columns(len(location_names))

for index, location_name in enumerate(location_names):
    with button_columns[index]:
        if st.button(
            f"📍 {location_name}",
            use_container_width=True,
            key=f"location_{index}",
        ):
            st.session_state.selected_location = location_name
            st.rerun()


# ---------------------------------------------------------
# SELECTED WORKSHOP DASHBOARD
# ---------------------------------------------------------
if st.session_state.selected_location is not None:
    selected_name = st.session_state.selected_location
    selected_info = WORKSHOPS[selected_name]

    st.markdown(
        f"""
        <div class="dashboard-card">
            <div class="selected-location">
                {selected_info["workshop"]}
            </div>

            <div class="selected-detail">
                {selected_info["branch"]} · {selected_name}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    metric_1, metric_2, metric_3, metric_4 = st.columns(4)

    with metric_1:
        st.metric(
            label="Repair Orders",
            value="0",
            delta="Waiting for data",
        )

    with metric_2:
        st.metric(
            label="Service Revenue",
            value="0 VND",
            delta="Waiting for data",
        )

    with metric_3:
        st.metric(
            label="Parts Revenue",
            value="0 VND",
            delta="Waiting for data",
        )

    with metric_4:
        st.metric(
            label="Total Revenue",
            value="0 VND",
            delta="Waiting for data",
        )

    st.info(
        "This section will later display the complete dashboard for the "
        f"{selected_info['workshop']} location."
    )

    if st.button(
        "← Return to network map",
        use_container_width=False,
    ):
        st.session_state.selected_location = None
        st.rerun()

else:
    st.info(
        "Select one of the workshop locations above to open its dashboard."
    )

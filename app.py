import time
from datetime import datetime

import folium
import streamlit as st
from streamlit_folium import st_folium


# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="Carpla Service Dashboard",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# DATA CONFIGURATION
# You can adjust workshop names / coordinates later
# =========================================================
LOCATION_DATA = {
    "Hà Nội": [
        {
            "workshop": "Carpla Service Hà Nội",
            "lat": 21.0285,
            "lon": 105.8542,
        }
    ],
    "Tây Bắc Bộ": [
        {
            "workshop": "Carpla Service Tây Bắc Bộ",
            "lat": 21.5942,
            "lon": 103.2153,
        }
    ],
    "Đông Bắc Bộ": [
        {
            "workshop": "Carpla Service Đông Bắc Bộ",
            "lat": 20.8449,
            "lon": 106.6881,
        }
    ],
    "TP. HCM": [
        {
            "workshop": "Carpla Service Tân Cảng",
            "lat": 10.7769,
            "lon": 106.7009,
        }
    ],
    "Cần Thơ": [
        {
            "workshop": "Carpla Service Cần Thơ",
            "lat": 10.0452,
            "lon": 105.7469,
        }
    ],
    "Nghệ An": [
        {
            "workshop": "Carpla Service Nghệ An",
            "lat": 18.6796,
            "lon": 105.6813,
        }
    ],
    "Đà Nẵng": [
        {
            "workshop": "Carpla Service Đà Nẵng",
            "lat": 16.0544,
            "lon": 108.2022,
        }
    ],
}

ALL_BRANCHES = list(LOCATION_DATA.keys())

WORKSHOP_TO_BRANCH = {}
WORKSHOP_COORDS = {}

for branch, workshops in LOCATION_DATA.items():
    for item in workshops:
        WORKSHOP_TO_BRANCH[item["workshop"]] = branch
        WORKSHOP_COORDS[item["workshop"]] = (item["lat"], item["lon"])


# =========================================================
# SESSION STATE
# =========================================================
if "selected_branch" not in st.session_state:
    st.session_state.selected_branch = "Tất cả"

if "selected_workshop" not in st.session_state:
    st.session_state.selected_workshop = "Tất cả"

if "selected_year" not in st.session_state:
    st.session_state.selected_year = 2026

if "selected_month" not in st.session_state:
    st.session_state.selected_month = 7

if "show_transition" not in st.session_state:
    st.session_state.show_transition = False

if "pending_workshop" not in st.session_state:
    st.session_state.pending_workshop = None

if "page_mode" not in st.session_state:
    st.session_state.page_mode = "home"


# =========================================================
# HELPERS
# =========================================================
def get_workshop_options(branch_value):
    if branch_value == "Tất cả":
        workshops = []
        for branch in ALL_BRANCHES:
            for item in LOCATION_DATA[branch]:
                workshops.append(item["workshop"])
        return ["Tất cả"] + workshops
    return ["Tất cả"] + [item["workshop"] for item in LOCATION_DATA[branch_value]]


def start_flight_to(workshop_name):
    st.session_state.pending_workshop = workshop_name
    st.session_state.show_transition = True
    st.rerun()


def render_logo():
    logo_col_1, logo_col_2, logo_col_3 = st.columns([1.2, 1.6, 1.2])
    with logo_col_2:
        try:
            st.image("carpla_services_logo_hd.png", use_container_width=True)
        except Exception:
            st.markdown(
                """
                <div style="
                    text-align:center;
                    font-size:34px;
                    font-weight:800;
                    color:#12395b;
                    margin-bottom:10px;
                ">
                    CARPLA SERVICE
                </div>
                """,
                unsafe_allow_html=True,
            )


def render_global_css():
    st.markdown(
        """
        <style>
            .stApp {
                background:
                    radial-gradient(circle at top left, rgba(37, 84, 124, 0.08), transparent 30%),
                    linear-gradient(180deg, #f3f7fb 0%, #ffffff 45%, #eef3f7 100%);
            }

            header[data-testid="stHeader"] {
                background: transparent;
            }

            .block-container {
                max-width: 1450px;
                padding-top: 1.0rem;
                padding-bottom: 2.5rem;
            }

            .main-title {
                text-align:center;
                font-size:34px;
                font-weight:800;
                color:#173e5e;
                margin-top:4px;
                margin-bottom:6px;
            }

            .main-subtitle {
                text-align:center;
                font-size:16px;
                color:#6b7a89;
                margin-bottom:25px;
            }

            .section-card {
                background: rgba(255,255,255,0.95);
                border: 1px solid #d9e5ee;
                border-radius: 22px;
                padding: 22px;
                box-shadow: 0 12px 28px rgba(22, 55, 82, 0.08);
                margin-bottom: 18px;
            }

            .section-title {
                font-size: 26px;
                font-weight: 800;
                color: #173e5e;
                margin-bottom: 10px;
            }

            .section-note {
                font-size: 15px;
                color: #6b7a89;
                margin-bottom: 18px;
            }

            .location-box {
                background: #ffffff;
                border: 1px solid #dae5ee;
                border-radius: 16px;
                padding: 12px 18px;
                box-shadow: 0 6px 16px rgba(22, 55, 82, 0.05);
            }

            .selected-header {
                background: #ffffff;
                border: 1px solid #dae5ee;
                border-radius: 20px;
                padding: 18px 22px;
                margin-bottom: 16px;
                box-shadow: 0 10px 25px rgba(22, 55, 82, 0.06);
            }

            .selected-title {
                font-size: 24px;
                font-weight: 800;
                color: #173e5e;
                margin-bottom: 4px;
            }

            .selected-detail {
                font-size: 15px;
                color: #6b7a89;
            }

            .small-note {
                font-size: 13px;
                color: #7b8a97;
            }

            .filter-card {
                background: rgba(255,255,255,0.88);
                border: 1px solid #d9e5ee;
                border-radius: 18px;
                padding: 14px 14px 4px 14px;
                margin-bottom: 15px;
            }

            .stButton > button {
                border-radius: 12px;
                border: 1px solid #c9d8e2;
                background: #ffffff;
                color: #173e5e;
                font-weight: 650;
                min-height: 42px;
            }

            .stButton > button:hover {
                border-color: #173e5e;
                background: #edf4f9;
                color: #173e5e;
            }

            .sidebar-title {
                font-size: 20px;
                font-weight: 800;
                color: #173e5e;
                margin-bottom: 8px;
            }

            div[data-testid="stMetric"] {
                background: #ffffff;
                border: 1px solid #dce7ef;
                border-radius: 18px;
                padding: 10px 14px;
                box-shadow: 0 8px 20px rgba(22, 55, 82, 0.05);
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar_filters():
    with st.sidebar:
        st.markdown(
            '<div class="sidebar-title">Bộ lọc</div>',
            unsafe_allow_html=True,
        )
        st.markdown('<div class="filter-card">', unsafe_allow_html=True)

        selected_branch = st.selectbox(
            "Chi nhánh",
            options=["Tất cả"] + ALL_BRANCHES,
            index=(["Tất cả"] + ALL_BRANCHES).index(st.session_state.selected_branch)
            if st.session_state.selected_branch in ["Tất cả"] + ALL_BRANCHES
            else 0,
        )

        workshop_options = get_workshop_options(selected_branch)

        if st.session_state.selected_workshop not in workshop_options:
            st.session_state.selected_workshop = "Tất cả"

        selected_workshop = st.selectbox(
            "Xưởng",
            options=workshop_options,
            index=workshop_options.index(st.session_state.selected_workshop)
            if st.session_state.selected_workshop in workshop_options
            else 0,
        )

        year_options = [2026, 2025, 2024]
        selected_year = st.selectbox(
            "Năm",
            options=year_options,
            index=year_options.index(st.session_state.selected_year)
            if st.session_state.selected_year in year_options
            else 0,
        )

        month_options = list(range(1, 13))
        selected_month = st.selectbox(
            "Tháng",
            options=month_options,
            index=month_options.index(st.session_state.selected_month)
            if st.session_state.selected_month in month_options
            else datetime.now().month - 1,
        )

        st.markdown("</div>", unsafe_allow_html=True)

        st.session_state.selected_branch = selected_branch
        st.session_state.selected_workshop = selected_workshop
        st.session_state.selected_year = selected_year
        st.session_state.selected_month = selected_month


def render_transition_screen(workshop_name):
    branch_name = WORKSHOP_TO_BRANCH.get(workshop_name, "")

    st.markdown(
        f"""
        <style>
            .stApp {{
                background: #000000 !important;
            }}
            .transition-wrap {{
                position: fixed;
                inset: 0;
                z-index: 999999;
                background:
                    radial-gradient(circle at 50% 45%, rgba(22,40,80,0.35), transparent 28%),
                    linear-gradient(180deg, #000000 0%, #02040a 100%);
                overflow: hidden;
            }}
            .transition-stars {{
                position: absolute;
                inset: 0;
                background-image:
                    radial-gradient(2px 2px at 10% 20%, rgba(255,255,255,0.9), transparent),
                    radial-gradient(2px 2px at 20% 80%, rgba(255,255,255,0.8), transparent),
                    radial-gradient(1.5px 1.5px at 35% 25%, rgba(255,255,255,0.7), transparent),
                    radial-gradient(2px 2px at 48% 70%, rgba(255,255,255,0.7), transparent),
                    radial-gradient(1.5px 1.5px at 60% 18%, rgba(255,255,255,0.8), transparent),
                    radial-gradient(2px 2px at 72% 76%, rgba(255,255,255,0.75), transparent),
                    radial-gradient(1.5px 1.5px at 85% 24%, rgba(255,255,255,0.8), transparent),
                    radial-gradient(2px 2px at 92% 64%, rgba(255,255,255,0.85), transparent);
                opacity: 0.9;
            }}
            .earth-scene {{
                position: absolute;
                inset: 0;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                color: white;
                font-family: Arial, sans-serif;
            }}
            .earth-orbit-wrap {{
                position: relative;
                width: 480px;
                height: 480px;
                display: flex;
                justify-content: center;
                align-items: center;
                margin-bottom: 24px;
            }}
            .earth-glow {{
                position: absolute;
                width: 310px;
                height: 310px;
                border-radius: 50%;
                background: radial-gradient(circle, rgba(75,120,255,0.25) 0%, rgba(10,20,45,0) 70%);
                filter: blur(16px);
            }}
            .earth {{
                position: absolute;
                width: 290px;
                height: 290px;
                border-radius: 50%;
                background:
                    radial-gradient(circle at 35% 35%, rgba(130,160,255,0.95) 0%, rgba(70,90,180,0.9) 16%, rgba(24,36,80,1) 48%, rgba(5,8,18,1) 78%),
                    radial-gradient(circle at 55% 60%, rgba(255,214,110,0.15), transparent 35%);
                box-shadow:
                    0 0 35px rgba(80, 120, 255, 0.25),
                    inset -35px -25px 55px rgba(0,0,0,0.55),
                    inset 18px 10px 32px rgba(255,255,255,0.10);
                overflow: hidden;
            }}
            .earth::before {{
                content: "";
                position: absolute;
                inset: 0;
                border-radius: 50%;
                background:
                    radial-gradient(circle at 45% 45%, transparent 0 35%, rgba(255,255,255,0.02) 36%, transparent 40%),
                    radial-gradient(circle at 42% 50%, rgba(255,220,140,0.25) 0 1.5%, transparent 2%),
                    radial-gradient(circle at 52% 47%, rgba(255,220,140,0.22) 0 1.2%, transparent 1.7%),
                    radial-gradient(circle at 58% 54%, rgba(255,220,140,0.22) 0 1.8%, transparent 2.4%),
                    radial-gradient(circle at 48% 57%, rgba(255,220,140,0.18) 0 1.3%, transparent 1.8%),
                    radial-gradient(circle at 39% 59%, rgba(255,220,140,0.15) 0 1.4%, transparent 1.9%),
                    radial-gradient(circle at 63% 43%, rgba(255,220,140,0.18) 0 1.1%, transparent 1.6%);
                opacity: 0.9;
            }}
            .earth::after {{
                content: "";
                position: absolute;
                left: 10%;
                top: 8%;
                width: 85%;
                height: 85%;
                border-radius: 50%;
                border-right: 2px solid rgba(255,255,255,0.10);
                border-top: 2px solid rgba(255,255,255,0.06);
                transform: rotate(-10deg);
            }}
            .orbit-ring {{
                position: absolute;
                width: 400px;
                height: 400px;
                border-radius: 50%;
                border: 1px solid rgba(255,255,255,0.12);
                box-shadow: 0 0 10px rgba(255,255,255,0.05);
            }}
            .plane-orbit {{
                position: absolute;
                width: 400px;
                height: 400px;
                border-radius: 50%;
                animation: spinAround 2.1s linear infinite;
            }}
            .plane {{
                position: absolute;
                left: 50%;
                top: -8px;
                transform: translateX(-50%) rotate(20deg);
                font-size: 30px;
                filter: drop-shadow(0 0 8px rgba(255,255,255,0.45));
            }}
            .travel-text {{
                text-align: center;
                margin-top: 8px;
            }}
            .travel-title {{
                font-size: 28px;
                font-weight: 800;
                letter-spacing: 0.5px;
                margin-bottom: 8px;
            }}
            .travel-subtitle {{
                font-size: 16px;
                color: rgba(255,255,255,0.80);
            }}

            @keyframes spinAround {{
                from {{ transform: rotate(0deg); }}
                to {{ transform: rotate(360deg); }}
            }}
        </style>

        <div class="transition-wrap">
            <div class="transition-stars"></div>
            <div class="earth-scene">
                <div class="earth-orbit-wrap">
                    <div class="earth-glow"></div>
                    <div class="earth"></div>
                    <div class="orbit-ring"></div>
                    <div class="plane-orbit">
                        <div class="plane">✈️</div>
                    </div>
                </div>

                <div class="travel-text">
                    <div class="travel-title">Flying to {workshop_name}</div>
                    <div class="travel-subtitle">{branch_name}</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_map():
    m = folium.Map(
        location=[16.3, 106.0],
        zoom_start=5.4,
        tiles="CartoDB positron",
        control_scale=False,
    )

    for branch, workshops in LOCATION_DATA.items():
        for item in workshops:
            workshop_name = item["workshop"]

            folium.Marker(
                location=[item["lat"], item["lon"]],
                tooltip=workshop_name,
                popup=folium.Popup(
                    f"""
                    <div style="min-width:180px;">
                        <b>{workshop_name}</b><br>
                        Chi nhánh: {branch}<br><br>
                        Chọn pin này rồi bấm nút bên dưới để mở dashboard.
                    </div>
                    """,
                    max_width=240,
                ),
                icon=folium.Icon(color="red", icon="plane", prefix="fa"),
            ).add_to(m)

    map_data = st_folium(
        m,
        width=None,
        height=520,
        returned_objects=["last_object_clicked_tooltip"],
        use_container_width=True,
    )

    clicked_name = None
    if map_data and map_data.get("last_object_clicked_tooltip"):
        clicked_name = map_data["last_object_clicked_tooltip"]

    return clicked_name


def render_homepage():
    render_logo()

    st.markdown(
        '<div class="main-title">CARPLA SERVICE PERFORMANCE DASHBOARD</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="main-subtitle">Select a branch or click a location on the Vietnam map to open the dashboard.</div>',
        unsafe_allow_html=True,
    )

    top_left, top_right = st.columns([2.4, 1.2])

    with top_left:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Carpla Service Network Map</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="section-note">Click a location pin on the map, or use the location buttons below.</div>',
            unsafe_allow_html=True,
        )

        clicked_map_workshop = render_map()

        if clicked_map_workshop:
            start_flight_to(clicked_map_workshop)

        st.markdown("</div>", unsafe_allow_html=True)

    with top_right:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Current Filter</div>', unsafe_allow_html=True)

        branch_text = st.session_state.selected_branch
        workshop_text = st.session_state.selected_workshop
        year_text = st.session_state.selected_year
        month_text = st.session_state.selected_month

        st.markdown(
            f"""
            <div class="location-box">
                <b>Chi nhánh:</b> {branch_text}<br><br>
                <b>Xưởng:</b> {workshop_text}<br><br>
                <b>Năm:</b> {year_text}<br><br>
                <b>Tháng:</b> {month_text}
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("<br>", unsafe_allow_html=True)

        if st.session_state.selected_workshop != "Tất cả":
            if st.button("Mở dashboard theo bộ lọc", use_container_width=True):
                start_flight_to(st.session_state.selected_workshop)
        else:
            st.info("Chọn một xưởng ở sidebar hoặc từ bản đồ.")

        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Select a workshop</div>', unsafe_allow_html=True)

    workshop_list = []
    if st.session_state.selected_branch == "Tất cả":
        for branch in ALL_BRANCHES:
            for item in LOCATION_DATA[branch]:
                workshop_list.append(item["workshop"])
    else:
        for item in LOCATION_DATA[st.session_state.selected_branch]:
            workshop_list.append(item["workshop"])

    if not workshop_list:
        st.warning("Không có xưởng phù hợp với bộ lọc hiện tại.")
    else:
        cols = st.columns(min(4, len(workshop_list)))
        for i, ws in enumerate(workshop_list):
            with cols[i % len(cols)]:
                if st.button(f"📍 {ws}", use_container_width=True, key=f"btn_{ws}"):
                    start_flight_to(ws)

    st.markdown("</div>", unsafe_allow_html=True)


def render_dashboard_content(workshop_name, branch_name, year_value, month_value):
    st.markdown(
        f"""
        <div class="selected-header">
            <div class="selected-title">{workshop_name}</div>
            <div class="selected-detail">
                Chi nhánh: {branch_name} &nbsp;&nbsp;|&nbsp;&nbsp; Năm: {year_value}
                &nbsp;&nbsp;|&nbsp;&nbsp; Tháng: {month_value}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    m1, m2, m3, m4 = st.columns(4)

    with m1:
        st.metric("RO", "0", "Waiting for data")

    with m2:
        st.metric("Doanh thu dịch vụ", "0 VND", "Waiting for data")

    with m3:
        st.metric("Doanh thu phụ tùng", "0 VND", "Waiting for data")

    with m4:
        st.metric("Tổng doanh thu", "0 VND", "Waiting for data")

    st.info(
        "Đây là khung dashboard Version 2. "
        "Phần tiếp theo, bạn chỉ cần thay thế section này bằng toàn bộ code dashboard Version 1 của bạn."
    )

    st.markdown("### Chỗ để gắn dashboard Version 1")
    st.markdown(
        """
        - Bảng KPI
        - Phân tích hãng xe
        - Cơ cấu nguồn thanh toán
        - Doanh thu dịch vụ + phụ tùng + phụ kiện
        - Các chart hiện tại của Version 1
        """
    )

    st.markdown("<br>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.button("Refresh dashboard", use_container_width=True)
    with c2:
        if st.button("← Quay về homepage", use_container_width=True):
            st.session_state.page_mode = "home"
            st.rerun()


# =========================================================
# MAIN APP FLOW
# =========================================================
render_global_css()
render_sidebar_filters()

# If transition is active, show animation first
if st.session_state.show_transition and st.session_state.pending_workshop:
    render_transition_screen(st.session_state.pending_workshop)
    time.sleep(3)
    st.session_state.selected_workshop = st.session_state.pending_workshop
    st.session_state.selected_branch = WORKSHOP_TO_BRANCH.get(
        st.session_state.pending_workshop,
        st.session_state.selected_branch
    )
    st.session_state.page_mode = "dashboard"
    st.session_state.show_transition = False
    st.rerun()

# Normal pages
if st.session_state.page_mode == "home":
    render_homepage()

else:
    selected_ws = st.session_state.selected_workshop

    if selected_ws == "Tất cả":
        st.warning("Vui lòng chọn một xưởng để xem dashboard.")
    else:
        branch_name = WORKSHOP_TO_BRANCH.get(selected_ws, st.session_state.selected_branch)
        render_dashboard_content(
            workshop_name=selected_ws,
            branch_name=branch_name,
            year_value=st.session_state.selected_year,
            month_value=st.session_state.selected_month,
        )

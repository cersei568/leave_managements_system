import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
from dataclasses import dataclass, asdict
from typing import List, Dict
import calendar

# Page configuration
st.set_page_config(
    page_title="Leave Management System",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional Custom CSS - Dark Blue & Ivory Theme
st.markdown("""
    <style>
    /* Main color palette */
    :root {
        --primary-dark-blue: #1a3a52;
        --secondary-blue: #2c5f7f;
        --accent-blue: #4a7fa0;
        --light-blue: #6ba3c5;
        --ivory: #fffff0;
        --soft-ivory: #f8f8f0;
        --cream: #faf9f6;
    }
    
    /* Main app background */
    .main {
        background: linear-gradient(135deg, #f8f8f0 0%, #ffffff 100%);
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a3a52 0%, #2c5f7f 100%);
    }
    
    [data-testid="stSidebar"] * {
        color: #fffff0 !important;
    }
    
    [data-testid="stSidebar"] .stRadio > label {
        color: #fffff0 !important;
        font-weight: 500;
    }
    
    [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] .stMetric label {
        color: #fffff0 !important;
        font-weight: 500;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #1a3a52;
        font-weight: 600;
    }
    
    /* Metric cards */
    div[data-testid="stMetricValue"] {
        font-size: 32px;
        font-weight: 700;
        color: #1a3a52;
    }
    
    div[data-testid="metric-container"] {
        background: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(26, 58, 82, 0.08);
        border-left: 4px solid #4a7fa0;
    }
    
    /* Professional cards */
    .leave-card {
        background: white;
        padding: 24px;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(26, 58, 82, 0.08);
        margin: 12px 0;
        border-left: 4px solid #4a7fa0;
        transition: all 0.3s ease;
    }
    
    .leave-card:hover {
        box-shadow: 0 6px 20px rgba(26, 58, 82, 0.12);
        transform: translateY(-2px);
    }
    
    /* Status badges */
    .pending-badge {
        background: linear-gradient(135deg, #ff9800 0%, #f57c00 100%);
        color: white;
        padding: 6px 16px;
        border-radius: 20px;
        font-size: 13px;
        font-weight: 600;
        display: inline-block;
        box-shadow: 0 2px 8px rgba(255, 152, 0, 0.3);
    }
    
    .approved-badge {
        background: linear-gradient(135deg, #4caf50 0%, #388e3c 100%);
        color: white;
        padding: 6px 16px;
        border-radius: 20px;
        font-size: 13px;
        font-weight: 600;
        display: inline-block;
        box-shadow: 0 2px 8px rgba(76, 175, 80, 0.3);
    }
    
    .rejected-badge {
        background: linear-gradient(135deg, #f44336 0%, #d32f2f 100%);
        color: white;
        padding: 6px 16px;
        border-radius: 20px;
        font-size: 13px;
        font-weight: 600;
        display: inline-block;
        box-shadow: 0 2px 8px rgba(244, 67, 54, 0.3);
    }
    
    /* Info boxes */
    .stAlert {
        border-radius: 12px;
        border-left: 4px solid #4a7fa0;
        background-color: #f8f8f0;
    }
    
    /* Buttons */
    .stButton > button {
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s ease;
        border: none;
        box-shadow: 0 2px 8px rgba(26, 58, 82, 0.15);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(26, 58, 82, 0.25);
    }
    
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #2c5f7f 0%, #1a3a52 100%);
        color: #fffff0;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background-color: white;
        border-radius: 8px;
        border: 1px solid #e0e0e0;
        font-weight: 600;
        color: #1a3a52;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: transparent;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: white;
        border-radius: 8px;
        padding: 12px 24px;
        font-weight: 600;
        color: #1a3a52;
        border: 2px solid transparent;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #2c5f7f 0%, #1a3a52 100%);
        color: #fffff0 !important;
        border-color: #1a3a52;
    }
    
    /* Data frames */
    .dataframe {
        border: none !important;
        box-shadow: 0 4px 12px rgba(26, 58, 82, 0.08);
        border-radius: 8px;
    }
    
    /* Select boxes and inputs */
    .stSelectbox > div > div,
    .stTextInput > div > div,
    .stTextArea > div > div {
        border-radius: 8px;
        border-color: #4a7fa0;
    }
    
    /* Professional header banner */
    .header-banner {
        background: linear-gradient(135deg, #1a3a52 0%, #2c5f7f 100%);
        padding: 30px;
        border-radius: 12px;
        color: #fffff0;
        margin-bottom: 30px;
        box-shadow: 0 6px 20px rgba(26, 58, 82, 0.2);
    }
    
    /* Dashboard stats card */
    .stat-card {
        background: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(26, 58, 82, 0.08);
        border-top: 4px solid #4a7fa0;
        text-align: center;
    }
    
    /* Section divider */
    hr {
        border: none;
        height: 2px;
        background: linear-gradient(to right, transparent, #4a7fa0, transparent);
        margin: 30px 0;
    }
    </style>
""", unsafe_allow_html=True)

# Data Classes
@dataclass
class LeavePolicy:
    name: str
    annual_days: int
    sick_days: int
    personal_days: int
    carryover_limit: int
    max_consecutive_days: int
    min_notice_days: int

@dataclass
class Employee:
    id: str
    name: str
    email: str
    department: str
    manager_id: str
    policy: str
    hire_date: datetime

@dataclass
class LeaveRequest:
    id: str
    employee_id: str
    leave_type: str
    start_date: datetime
    end_date: datetime
    days: float
    reason: str
    status: str
    submitted_date: datetime
    approver_id: str = None
    approved_date: datetime = None
    comments: str = ""

# Initialize session state
if 'leave_policies' not in st.session_state:
    st.session_state.leave_policies = {
        'Standard': LeavePolicy('Standard', 20, 10, 5, 5, 15, 7),
        'Senior': LeavePolicy('Senior', 25, 12, 7, 10, 20, 5),
        'Executive': LeavePolicy('Executive', 30, 15, 10, 15, 30, 3)
    }

if 'employees' not in st.session_state:
    st.session_state.employees = [
        Employee('E001', 'John Doe', 'john@company.com', 'Engineering', 'M001', 'Standard', datetime(2020, 1, 15)),
        Employee('E002', 'Jane Smith', 'jane@company.com', 'Marketing', 'M002', 'Senior', datetime(2018, 3, 20)),
        Employee('E003', 'Bob Johnson', 'bob@company.com', 'Engineering', 'M001', 'Standard', datetime(2021, 6, 1)),
        Employee('E004', 'Alice Williams', 'alice@company.com', 'HR', 'M003', 'Senior', datetime(2019, 9, 10)),
        Employee('E005', 'Charlie Brown', 'charlie@company.com', 'Sales', 'M002', 'Standard', datetime(2022, 2, 14)),
        Employee('M001', 'Manager One', 'manager1@company.com', 'Engineering', 'CEO', 'Executive', datetime(2015, 1, 1)),
        Employee('M002', 'Manager Two', 'manager2@company.com', 'Marketing', 'CEO', 'Executive', datetime(2016, 1, 1)),
        Employee('M003', 'Manager Three', 'manager3@company.com', 'HR', 'CEO', 'Executive', datetime(2017, 1, 1)),
    ]

if 'leave_requests' not in st.session_state:
    st.session_state.leave_requests = [
        LeaveRequest('L001', 'E001', 'Annual Leave', datetime(2024, 2, 1), datetime(2024, 2, 5), 5, 'Family vacation', 'Approved', datetime(2024, 1, 15), 'M001', datetime(2024, 1, 16)),
        LeaveRequest('L002', 'E002', 'Sick Leave', datetime(2024, 1, 10), datetime(2024, 1, 12), 3, 'Flu', 'Approved', datetime(2024, 1, 9), 'M002', datetime(2024, 1, 9)),
        LeaveRequest('L003', 'E003', 'Annual Leave', datetime(2024, 3, 15), datetime(2024, 3, 20), 4, 'Vacation', 'Pending', datetime(2024, 1, 20)),
        LeaveRequest('L004', 'E001', 'Personal Leave', datetime(2024, 2, 26), datetime(2024, 2, 27), 2, 'Personal matters', 'Pending', datetime(2024, 1, 25)),
        LeaveRequest('L005', 'E004', 'Annual Leave', datetime(2024, 4, 1), datetime(2024, 4, 10), 8, 'Spring break', 'Approved', datetime(2024, 1, 28), 'M003', datetime(2024, 1, 29)),
    ]

if 'holidays' not in st.session_state:
    st.session_state.holidays = [
        {'date': datetime(2024, 1, 1), 'name': "New Year's Day"},
        {'date': datetime(2024, 7, 4), 'name': "Independence Day"},
        {'date': datetime(2024, 12, 25), 'name': "Christmas Day"},
        {'date': datetime(2024, 11, 28), 'name': "Thanksgiving"},
    ]

if 'current_user' not in st.session_state:
    st.session_state.current_user = 'E001'

if 'leave_balances' not in st.session_state:
    st.session_state.leave_balances = {}
    for emp in st.session_state.employees:
        policy = st.session_state.leave_policies[emp.policy]
        st.session_state.leave_balances[emp.id] = {
            'Annual Leave': policy.annual_days,
            'Sick Leave': policy.sick_days,
            'Personal Leave': policy.personal_days,
            'Used Annual': 0,
            'Used Sick': 0,
            'Used Personal': 0
        }

# Helper Functions
def get_employee(emp_id):
    return next((emp for emp in st.session_state.employees if emp.id == emp_id), None)

def get_employee_name(emp_id):
    emp = get_employee(emp_id)
    return emp.name if emp else "Unknown"

def calculate_working_days(start_date, end_date):
    """Calculate working days excluding weekends and holidays"""
    days = 0
    current = start_date
    holiday_dates = [h['date'].date() for h in st.session_state.holidays]
    
    while current <= end_date:
        if current.weekday() < 5 and current.date() not in holiday_dates:
            days += 1
        current += timedelta(days=1)
    return days

def check_team_coverage(employee_id, start_date, end_date):
    """Check if leave would create coverage issues"""
    emp = get_employee(employee_id)
    team_members = [e for e in st.session_state.employees if e.department == emp.department and e.id != employee_id]
    
    overlapping_leaves = []
    for leave in st.session_state.leave_requests:
        if leave.status == 'Approved' and leave.employee_id in [tm.id for tm in team_members]:
            if not (leave.end_date < start_date or leave.start_date > end_date):
                overlapping_leaves.append(leave)
    
    coverage_percentage = 1 - (len(overlapping_leaves) / max(len(team_members), 1))
    return coverage_percentage, overlapping_leaves

def analyze_sick_leave_patterns(employee_id):
    """Analyze sick leave patterns for wellness interventions"""
    sick_leaves = [lr for lr in st.session_state.leave_requests 
                   if lr.employee_id == employee_id and lr.leave_type == 'Sick Leave']
    
    if not sick_leaves:
        return {
            'total_days': 0,
            'frequency': 0,
            'pattern': 'No pattern',
            'alert_level': 'green'
        }
    
    total_days = sum(lr.days for lr in sick_leaves)
    frequency = len(sick_leaves)
    
    monday_friday_leaves = sum(1 for lr in sick_leaves 
                               if lr.start_date.weekday() in [0, 4])
    
    alert_level = 'green'
    pattern = 'Normal'
    
    if total_days > 8:
        alert_level = 'red'
        pattern = 'High frequency - wellness check recommended'
    elif total_days > 5:
        alert_level = 'yellow'
        pattern = 'Moderate - monitor'
    elif monday_friday_leaves > frequency * 0.6:
        alert_level = 'yellow'
        pattern = 'Weekend-adjacent pattern detected'
    
    return {
        'total_days': total_days,
        'frequency': frequency,
        'pattern': pattern,
        'alert_level': alert_level
    }

def validate_leave_request(employee_id, leave_type, start_date, end_date):
    """Validate leave request against policies"""
    emp = get_employee(employee_id)
    policy = st.session_state.leave_policies[emp.policy]
    
    errors = []
    warnings = []
    
    days_until_leave = (start_date - datetime.now()).days
    if days_until_leave < policy.min_notice_days:
        warnings.append(f"Less than {policy.min_notice_days} days notice provided")
    
    leave_days = calculate_working_days(start_date, end_date)
    if leave_days > policy.max_consecutive_days:
        errors.append(f"Exceeds maximum consecutive days ({policy.max_consecutive_days})")
    
    balance = st.session_state.leave_balances.get(employee_id, {})
    available = balance.get(leave_type, 0)
    if leave_days > available:
        errors.append(f"Insufficient {leave_type} balance (Available: {available}, Requested: {leave_days})")
    
    coverage, overlapping = check_team_coverage(employee_id, start_date, end_date)
    if coverage < 0.5:
        warnings.append(f"Low team coverage ({coverage*100:.0f}%) - {len(overlapping)} team members also on leave")
    
    return errors, warnings

def update_leave_balance(employee_id, leave_type, days, operation='deduct'):
    """Update employee leave balance"""
    if employee_id not in st.session_state.leave_balances:
        return
    
    balance = st.session_state.leave_balances[employee_id]
    
    if operation == 'deduct':
        balance[leave_type] -= days
        balance[f'Used {leave_type.split()[0]}'] += days
    elif operation == 'restore':
        balance[leave_type] += days
        balance[f'Used {leave_type.split()[0]}'] -= days

# Main App
def main():
    # Professional header
    st.markdown("""
        <div class="header-banner">
            <h1 style="margin:0; color: #fffff0; font-size: 36px;">🏢 Leave Management System</h1>
            <p style="margin:5px 0 0 0; color: #fffff0; opacity: 0.9; font-size: 16px;">Professional Time-Off Management Platform</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("<br>", unsafe_allow_html=True)
        
        # User selection
        current_user = st.selectbox(
            "👤 Current User",
            options=[emp.id for emp in st.session_state.employees],
            format_func=lambda x: get_employee_name(x),
            key='user_selector'
        )
        st.session_state.current_user = current_user
        
        emp = get_employee(current_user)
        st.markdown(f"""
            <div style="background: rgba(255,255,240,0.1); padding: 15px; border-radius: 8px; margin: 15px 0;">
                <p style="margin:0; font-size: 14px;"><strong>Department:</strong> {emp.department}</p>
                <p style="margin:5px 0 0 0; font-size: 14px;"><strong>Policy:</strong> {emp.policy}</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Quick Stats
        st.subheader("📊 Leave Balance")
        balance = st.session_state.leave_balances.get(current_user, {})
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Annual", f"{balance.get('Annual Leave', 0):.0f}")
            st.metric("Sick", f"{balance.get('Sick Leave', 0):.0f}")
        with col2:
            st.metric("Personal", f"{balance.get('Personal Leave', 0):.0f}")
            
        pending = sum(1 for lr in st.session_state.leave_requests 
                     if lr.employee_id == current_user and lr.status == 'Pending')
        if pending > 0:
            st.warning(f"⏳ {pending} pending request(s)")
        
        st.markdown("---")
        
        # Navigation
        page = st.radio(
            "Navigation",
            ["🏠 Dashboard", "📝 New Request", "📋 My Requests", 
             "✅ Approvals", "📅 Team Calendar", "📊 Analytics", 
             "⚙️ Settings"],
            label_visibility="collapsed"
        )
    
    # Main Content Area
    if page == "🏠 Dashboard":
        show_dashboard()
    elif page == "📝 New Request":
        show_new_request()
    elif page == "📋 My Requests":
        show_my_requests()
    elif page == "✅ Approvals":
        show_approvals()
    elif page == "📅 Team Calendar":
        show_team_calendar()
    elif page == "📊 Analytics":
        show_analytics()
    elif page == "⚙️ Settings":
        show_settings()

def show_dashboard():
    st.header("Dashboard Overview")
    
    current_user = st.session_state.current_user
    emp = get_employee(current_user)
    balance = st.session_state.leave_balances.get(current_user, {})
    
    # Top metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_balance = balance.get('Annual Leave', 0) + balance.get('Sick Leave', 0) + balance.get('Personal Leave', 0)
        st.metric("Total Leave Balance", f"{total_balance:.0f} days")
    
    with col2:
        used_total = balance.get('Used Annual', 0) + balance.get('Used Sick', 0) + balance.get('Used Personal', 0)
        st.metric("Leave Used (YTD)", f"{used_total:.0f} days")
    
    with col3:
        pending_count = sum(1 for lr in st.session_state.leave_requests 
                           if lr.employee_id == current_user and lr.status == 'Pending')
        st.metric("Pending Requests", pending_count)
    
    with col4:
        subordinates = [e for e in st.session_state.employees if e.manager_id == current_user]
        pending_approvals = sum(1 for lr in st.session_state.leave_requests 
                               if lr.status == 'Pending' and 
                               any(e.id == lr.employee_id for e in subordinates))
        st.metric("Pending Approvals", pending_approvals)
    
    st.markdown("---")
    
    # Leave Balance Visualization
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📊 Leave Balance Breakdown")
        
        balance_data = pd.DataFrame([
            {'Type': 'Annual', 'Available': balance.get('Annual Leave', 0), 
             'Used': balance.get('Used Annual', 0)},
            {'Type': 'Sick', 'Available': balance.get('Sick Leave', 0), 
             'Used': balance.get('Used Sick', 0)},
            {'Type': 'Personal', 'Available': balance.get('Personal Leave', 0), 
             'Used': balance.get('Used Personal', 0)},
        ])
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            name='Available',
            x=balance_data['Type'],
            y=balance_data['Available'],
            marker_color='#2c5f7f',
            text=balance_data['Available'],
            textposition='outside'
        ))
        fig.add_trace(go.Bar(
            name='Used',
            x=balance_data['Type'],
            y=balance_data['Used'],
            marker_color='#6ba3c5',
            text=balance_data['Used'],
            textposition='outside'
        ))
        
        fig.update_layout(
            barmode='group',
            height=350,
            margin=dict(l=0, r=0, t=30, b=0),
            showlegend=True,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            font=dict(color='#1a3a52')
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("🎯 Policy Limits")
        policy = st.session_state.leave_policies[emp.policy]
        
        st.markdown(f"""
        <div style="background: white; padding: 20px; border-radius: 12px; box-shadow: 0 4px 12px rgba(26, 58, 82, 0.08);">
            <h4 style="color: #1a3a52; margin-top: 0;">Your Policy: {emp.policy}</h4>
            <p style="margin: 8px 0; color: #2c5f7f;"><strong>Max Consecutive:</strong> {policy.max_consecutive_days} days</p>
            <p style="margin: 8px 0; color: #2c5f7f;"><strong>Min Notice:</strong> {policy.min_notice_days} days</p>
            <p style="margin: 8px 0; color: #2c5f7f;"><strong>Carryover Limit:</strong> {policy.carryover_limit} days</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Upcoming leaves
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📅 Your Upcoming Leaves")
        upcoming = [lr for lr in st.session_state.leave_requests 
                   if lr.employee_id == current_user and 
                   lr.start_date >= datetime.now() and 
                   lr.status == 'Approved']
        upcoming.sort(key=lambda x: x.start_date)
        
        if upcoming:
            for leave in upcoming[:5]:
                st.markdown(f"""
                <div class="leave-card">
                    <h4 style="color: #1a3a52; margin: 0 0 10px 0;">{leave.leave_type}</h4>
                    <p style="margin: 5px 0; color: #2c5f7f;">📅 {leave.start_date.strftime('%b %d')} - {leave.end_date.strftime('%b %d, %Y')}</p>
                    <p style="margin: 5px 0; color: #4a7fa0;">📝 {leave.reason}</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No upcoming approved leaves")
    
    with col2:
        st.subheader("👥 Team Absences")
        team_members = [e for e in st.session_state.employees 
                       if e.department == emp.department and e.id != current_user]
        
        team_leaves = [lr for lr in st.session_state.leave_requests 
                      if lr.employee_id in [tm.id for tm in team_members] and 
                      lr.start_date >= datetime.now() and 
                      lr.status == 'Approved']
        team_leaves.sort(key=lambda x: x.start_date)
        
        if team_leaves:
            for leave in team_leaves[:5]:
                emp_name = get_employee_name(leave.employee_id)
                st.markdown(f"""
                <div class="leave-card">
                    <h4 style="color: #1a3a52; margin: 0 0 10px 0;">{emp_name}</h4>
                    <p style="margin: 5px 0; color: #2c5f7f;">📅 {leave.start_date.strftime('%b %d')} - {leave.end_date.strftime('%b %d, %Y')}</p>
                    <p style="margin: 5px 0; color: #4a7fa0;">🏷️ {leave.leave_type}</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No upcoming team absences")
    
    # Holidays
    st.markdown("---")
    st.subheader("🎉 Upcoming Holidays")
    
    upcoming_holidays = [h for h in st.session_state.holidays if h['date'] >= datetime.now()]
    upcoming_holidays.sort(key=lambda x: x['date'])
    
    num_cols = max(min(len(upcoming_holidays), 4), 1)
    cols = st.columns(num_cols)
    
    for i, holiday in enumerate(upcoming_holidays[:4]):
        with cols[i % num_cols]:
            st.markdown(f"""
            <div style="background: white; padding: 20px; border-radius: 12px; box-shadow: 0 4px 12px rgba(26, 58, 82, 0.08); text-align: center; border-top: 4px solid #4a7fa0;">
                <h4 style="color: #1a3a52; margin: 0 0 10px 0;">{holiday['name']}</h4>
                <p style="color: #2c5f7f; margin: 0;">{holiday['date'].strftime('%B %d, %Y')}</p>
            </div>
            """, unsafe_allow_html=True)

def show_new_request():
    st.header("📝 New Leave Request")
    
    current_user = st.session_state.current_user
    emp = get_employee(current_user)
    balance = st.session_state.leave_balances.get(current_user, {})
    
    with st.form("new_leave_request"):
        col1, col2 = st.columns(2)
        
        with col1:
            leave_type = st.selectbox(
                "Leave Type",
                ["Annual Leave", "Sick Leave", "Personal Leave"],
                help="Select the type of leave you want to request"
            )
            
            available = balance.get(leave_type, 0)
            st.markdown(f"""
            <div style="background: white; padding: 15px; border-radius: 8px; border-left: 4px solid #4a7fa0; margin: 10px 0;">
                <p style="margin: 0; color: #1a3a52;"><strong>Available {leave_type}:</strong> <span style="color: #2c5f7f; font-size: 20px; font-weight: bold;">{available:.1f} days</span></p>
            </div>
            """, unsafe_allow_html=True)
            
            start_date = st.date_input(
                "Start Date",
                min_value=datetime.now().date(),
                value=datetime.now().date()
            )
        
        with col2:
            end_date = st.date_input(
                "End Date",
                min_value=datetime.now().date(),
                value=datetime.now().date() + timedelta(days=1)
            )
            
            if end_date < start_date:
                st.error("End date must be after start date")
            else:
                days_requested = calculate_working_days(
                    datetime.combine(start_date, datetime.min.time()),
                    datetime.combine(end_date, datetime.min.time())
                )
                st.metric("Working Days", days_requested)
        
        reason = st.text_area(
            "Reason",
            placeholder="Please provide a reason for your leave request...",
            help="Provide details about your leave request",
            height=100
        )
        
        # Validation preview
        if start_date and end_date and end_date >= start_date:
            errors, warnings = validate_leave_request(
                current_user, leave_type,
                datetime.combine(start_date, datetime.min.time()),
                datetime.combine(end_date, datetime.min.time())
            )
            
            if errors:
                for error in errors:
                    st.error(f"❌ {error}")
            
            if warnings:
                for warning in warnings:
                    st.warning(f"⚠️ {warning}")
            
            # Coverage check
            coverage, overlapping = check_team_coverage(
                current_user,
                datetime.combine(start_date, datetime.min.time()),
                datetime.combine(end_date, datetime.min.time())
            )
            
            if coverage < 0.7:
                st.warning(f"⚠️ Team coverage will be {coverage*100:.0f}% during this period")
                if overlapping:
                    st.write("Team members on leave during this time:")
                    for ol in overlapping:
                        st.write(f"- {get_employee_name(ol.employee_id)}: {ol.start_date.strftime('%b %d')} - {ol.end_date.strftime('%b %d')}")
        
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            submit = st.form_submit_button("✅ Submit Request", type="primary", use_container_width=True)
        with col2:
            save_draft = st.form_submit_button("💾 Save Draft", use_container_width=True)
        with col3:
            cancel = st.form_submit_button("❌ Cancel", use_container_width=True)
        
        if submit:
            if not reason:
                st.error("Please provide a reason for your leave request")
            elif end_date < start_date:
                st.error("End date must be after start date")
            else:
                errors, warnings = validate_leave_request(
                    current_user, leave_type,
                    datetime.combine(start_date, datetime.min.time()),
                    datetime.combine(end_date, datetime.min.time())
                )
                
                if errors:
                    st.error("Cannot submit request due to policy violations")
                else:
                    new_id = f"L{len(st.session_state.leave_requests) + 1:03d}"
                    new_request = LeaveRequest(
                        id=new_id,
                        employee_id=current_user,
                        leave_type=leave_type,
                        start_date=datetime.combine(start_date, datetime.min.time()),
                        end_date=datetime.combine(end_date, datetime.min.time()),
                        days=days_requested,
                        reason=reason,
                        status='Pending',
                        submitted_date=datetime.now()
                    )
                    
                    st.session_state.leave_requests.append(new_request)
                    st.success(f"✅ Leave request {new_id} submitted successfully!")
                    st.balloons()
                    
                    manager = get_employee(emp.manager_id)
                    st.info(f"Your request will be reviewed by {manager.name}")

def show_my_requests():
    st.header("📋 My Leave Requests")
    
    current_user = st.session_state.current_user
    
    # Filter options
    col1, col2, col3 = st.columns(3)
    with col1:
        status_filter = st.multiselect(
            "Status",
            ["Pending", "Approved", "Rejected"],
            default=["Pending", "Approved"]
        )
    with col2:
        leave_type_filter = st.multiselect(
            "Leave Type",
            ["Annual Leave", "Sick Leave", "Personal Leave"],
            default=["Annual Leave", "Sick Leave", "Personal Leave"]
        )
    with col3:
        year_filter = st.selectbox(
            "Year",
            [2024, 2023],
            index=0
        )
    
    my_requests = [lr for lr in st.session_state.leave_requests 
                   if lr.employee_id == current_user and 
                   lr.status in status_filter and 
                   lr.leave_type in leave_type_filter and
                   lr.start_date.year == year_filter]
    
    my_requests.sort(key=lambda x: x.submitted_date, reverse=True)
    
    if not my_requests:
        st.info("No leave requests found matching the filters")
        return
    
    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Requests", len(my_requests))
    with col2:
        pending = sum(1 for lr in my_requests if lr.status == 'Pending')
        st.metric("Pending", pending)
    with col3:
        approved = sum(1 for lr in my_requests if lr.status == 'Approved')
        st.metric("Approved", approved)
    with col4:
        total_days = sum(lr.days for lr in my_requests if lr.status == 'Approved')
        st.metric("Total Days", f"{total_days:.0f}")
    
    st.markdown("---")
    
    # Display requests
    for request in my_requests:
        with st.expander(
            f"{request.leave_type} - {request.start_date.strftime('%b %d')} to {request.end_date.strftime('%b %d, %Y')} "
            f"({request.days} days) - {request.status}",
            expanded=request.status == 'Pending'
        ):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(f"""
                **Request ID:** {request.id}  
                **Leave Type:** {request.leave_type}  
                **Duration:** {request.start_date.strftime('%B %d, %Y')} - {request.end_date.strftime('%B %d, %Y')}  
                **Days:** {request.days}  
                **Reason:** {request.reason}  
                **Submitted:** {request.submitted_date.strftime('%B %d, %Y at %I:%M %p')}  
                """)
                
                if request.status != 'Pending':
                    approver_name = get_employee_name(request.approver_id) if request.approver_id else "Unknown"
                    st.markdown(f"**Reviewed by:** {approver_name}")
                    if request.approved_date:
                        st.markdown(f"**Review Date:** {request.approved_date.strftime('%B %d, %Y')}")
                    if request.comments:
                        st.markdown(f"**Comments:** {request.comments}")
            
            with col2:
                if request.status == 'Pending':
                    badge = '<div class="pending-badge">PENDING</div>'
                elif request.status == 'Approved':
                    badge = '<div class="approved-badge">APPROVED</div>'
                else:
                    badge = '<div class="rejected-badge">REJECTED</div>'
                    
                st.markdown(f"""
                <div style="text-align: center; padding: 20px;">
                    {badge}
                </div>
                """, unsafe_allow_html=True)
                
                if request.status == 'Pending':
                    if st.button("🗑️ Cancel Request", key=f"cancel_{request.id}"):
                        st.session_state.leave_requests.remove(request)
                        st.success("Request cancelled")
                        st.rerun()

def show_approvals():
    st.header("✅ Leave Approvals")
    
    current_user = st.session_state.current_user
    
    subordinates = [e for e in st.session_state.employees if e.manager_id == current_user]
    
    if not subordinates:
        st.info("You don't have any team members to approve leaves for")
        return
    
    pending_requests = [lr for lr in st.session_state.leave_requests 
                       if lr.status == 'Pending' and 
                       lr.employee_id in [s.id for s in subordinates]]
    
    pending_requests.sort(key=lambda x: x.submitted_date)
    
    st.subheader(f"📊 Pending Approvals: {len(pending_requests)}")
    
    if not pending_requests:
        st.success("✨ No pending approvals!")
        
        st.markdown("---")
        st.subheader("Recent Approvals")
        
        recent = [lr for lr in st.session_state.leave_requests 
                 if lr.approver_id == current_user and lr.status in ['Approved', 'Rejected']]
        recent.sort(key=lambda x: x.approved_date if x.approved_date else x.submitted_date, reverse=True)
        
        for request in recent[:5]:
            emp_name = get_employee_name(request.employee_id)
            status_icon = "✅" if request.status == "Approved" else "❌"
            st.markdown(f"""
            <div class="leave-card">
                <p style="margin: 0; color: #1a3a52;">{status_icon} <strong>{emp_name}</strong> - {request.leave_type} - {request.status}</p>
            </div>
            """, unsafe_allow_html=True)
        
        return
    
    # Display pending requests
    for request in pending_requests:
        emp = get_employee(request.employee_id)
        balance = st.session_state.leave_balances.get(request.employee_id, {})
        
        with st.expander(
            f"🔔 {emp.name} - {request.leave_type} ({request.days} days) - "
            f"{request.start_date.strftime('%b %d')} to {request.end_date.strftime('%b %d')}",
            expanded=True
        ):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"""
                **Employee:** {emp.name} ({emp.department})  
                **Leave Type:** {request.leave_type}  
                **Duration:** {request.start_date.strftime('%B %d, %Y')} - {request.end_date.strftime('%B %d, %Y')}  
                **Days Requested:** {request.days}  
                **Reason:** {request.reason}  
                **Submitted:** {request.submitted_date.strftime('%B %d, %Y at %I:%M %p')}  
                """)
                
                st.markdown(f"""
                <div style="background: white; padding: 15px; border-radius: 8px; border-left: 4px solid #4a7fa0; margin: 10px 0;">
                    <p style="margin: 0; color: #1a3a52;"><strong>Current Balance:</strong> <span style="color: #2c5f7f; font-weight: bold;">{balance.get(request.leave_type, 0):.1f} days</span></p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                coverage, overlapping = check_team_coverage(
                    request.employee_id,
                    request.start_date,
                    request.end_date
                )
                
                coverage_color = '#4caf50' if coverage >= 0.7 else '#ff9800' if coverage >= 0.5 else '#f44336'
                st.markdown(f"""
                <div style="background: white; padding: 15px; border-radius: 8px; text-align: center;">
                    <p style="margin: 0 0 5px 0; color: #1a3a52; font-weight: 600;">Team Coverage</p>
                    <p style="margin: 0; color: {coverage_color}; font-size: 24px; font-weight: bold;">{coverage*100:.0f}%</p>
                </div>
                """, unsafe_allow_html=True)
                
                if overlapping:
                    st.warning(f"⚠️ {len(overlapping)} team member(s) also on leave")
                
                if request.leave_type == 'Sick Leave':
                    pattern = analyze_sick_leave_patterns(request.employee_id)
                    if pattern['alert_level'] != 'green':
                        st.warning(f"⚠️ {pattern['pattern']}")
            
            errors, warnings = validate_leave_request(
                request.employee_id,
                request.leave_type,
                request.start_date,
                request.end_date
            )
            
            if errors:
                for error in errors:
                    st.error(f"❌ {error}")
            
            if warnings:
                for warning in warnings:
                    st.warning(f"⚠️ {warning}")
            
            st.markdown("---")
            col1, col2, col3 = st.columns([2, 1, 1])
            
            with col1:
                comments = st.text_input(
                    "Comments (optional)",
                    key=f"comments_{request.id}",
                    placeholder="Add any comments..."
                )
            
            with col2:
                if st.button("✅ Approve", key=f"approve_{request.id}", type="primary", use_container_width=True):
                    request.status = 'Approved'
                    request.approver_id = current_user
                    request.approved_date = datetime.now()
                    request.comments = comments
                    
                    update_leave_balance(request.employee_id, request.leave_type, request.days, 'deduct')
                    
                    st.success(f"✅ Approved leave for {emp.name}")
                    st.rerun()
            
            with col3:
                if st.button("❌ Reject", key=f"reject_{request.id}", use_container_width=True):
                    request.status = 'Rejected'
                    request.approver_id = current_user
                    request.approved_date = datetime.now()
                    request.comments = comments if comments else "Request rejected"
                    
                    st.error(f"❌ Rejected leave for {emp.name}")
                    st.rerun()

def show_team_calendar():
    st.header("📅 Team Availability Calendar")
    
    current_user = st.session_state.current_user
    emp = get_employee(current_user)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        view_type = st.selectbox("View", ["My Team", "Department", "All Employees"])
    with col2:
        selected_month = st.selectbox(
            "Month",
            range(1, 13),
            format_func=lambda x: calendar.month_name[x],
            index=datetime.now().month - 1
        )
    with col3:
        selected_year = st.selectbox("Year", [2024, 2025], index=0)
    
    if view_type == "My Team":
        employees = [e for e in st.session_state.employees if e.manager_id == current_user]
    elif view_type == "Department":
        employees = [e for e in st.session_state.employees if e.department == emp.department]
    else:
        employees = st.session_state.employees
    
    if not employees:
        st.info("No employees to display for this view")
        return
    
    start_date = datetime(selected_year, selected_month, 1)
    if selected_month == 12:
        end_date = datetime(selected_year + 1, 1, 1) - timedelta(days=1)
    else:
        end_date = datetime(selected_year, selected_month + 1, 1) - timedelta(days=1)
    
    leaves_in_period = [lr for lr in st.session_state.leave_requests 
                       if lr.status == 'Approved' and 
                       lr.employee_id in [e.id for e in employees] and
                       not (lr.end_date < start_date or lr.start_date > end_date)]
    
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Team Size", len(employees))
    with col2:
        total_leave_days = sum(lr.days for lr in leaves_in_period)
        st.metric("Total Leave Days", f"{total_leave_days:.0f}")
    with col3:
        avg_availability = 100 - (total_leave_days / (len(employees) * 20) * 100) if employees else 100
        st.metric("Avg Availability", f"{avg_availability:.0f}%")
    
    st.markdown("---")
    st.subheader("📊 Daily Team Availability")
    
    daily_data = []
    current = start_date
    while current <= end_date:
        on_leave = sum(1 for lr in leaves_in_period 
                      if lr.start_date.date() <= current.date() <= lr.end_date.date())
        available = len(employees) - on_leave
        availability_pct = (available / len(employees) * 100) if employees else 100
        
        daily_data.append({
            'Date': current,
            'Available': available,
            'On Leave': on_leave,
            'Availability %': availability_pct
        })
        current += timedelta(days=1)
    
    df_daily = pd.DataFrame(daily_data)
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=df_daily['Date'],
        y=df_daily['Available'],
        name='Available',
        marker_color='#2c5f7f'
    ))
    
    fig.add_trace(go.Bar(
        x=df_daily['Date'],
        y=df_daily['On Leave'],
        name='On Leave',
        marker_color='#6ba3c5'
    ))
    
    fig.update_layout(
        barmode='stack',
        height=350,
        xaxis_title="Date",
        yaxis_title="Number of Employees",
        hovermode='x unified',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#1a3a52'),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    st.subheader("📋 Leave Details")
    
    if leaves_in_period:
        for leave in sorted(leaves_in_period, key=lambda x: x.start_date):
            emp_name = get_employee_name(leave.employee_id)
            emp_dept = get_employee(leave.employee_id).department
            
            st.markdown(f"""
            <div class="leave-card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <h4 style="margin: 0; color: #1a3a52;">{emp_name}</h4>
                        <p style="margin: 5px 0; color: #4a7fa0;">{emp_dept}</p>
                    </div>
                    <div style="text-align: right;">
                        <p style="margin: 0; color: #2c5f7f; font-weight: 600;">{leave.start_date.strftime('%b %d')} - {leave.end_date.strftime('%b %d')}</p>
                        <p style="margin: 5px 0; color: #4a7fa0;">{leave.days} days • {leave.leave_type}</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No approved leaves for this period")
    
    st.markdown("---")
    st.subheader("🎉 Holidays")
    
    holidays_in_month = [h for h in st.session_state.holidays 
                        if h['date'].month == selected_month and h['date'].year == selected_year]
    
    if holidays_in_month:
        for holiday in holidays_in_month:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #4a7fa0 0%, #2c5f7f 100%); padding: 15px 20px; border-radius: 8px; margin: 10px 0;">
                <p style="margin: 0; color: #fffff0; font-weight: 600;">📅 {holiday['name']} - {holiday['date'].strftime('%B %d, %Y')}</p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No holidays in this month")

def show_analytics():
    st.header("📊 Leave Analytics & Insights")
    
    current_user = st.session_state.current_user
    emp = get_employee(current_user)
    
    is_manager = any(e.manager_id == current_user for e in st.session_state.employees)
    
    tab1, tab2, tab3, tab4 = st.tabs([
        "📈 Usage Trends", 
        "🏥 Wellness Insights", 
        "👥 Team Analytics",
        "📋 Reports"
    ])
    
    with tab1:
        st.subheader("Leave Usage Trends")
        
        my_leaves = [lr for lr in st.session_state.leave_requests 
                    if lr.employee_id == current_user and lr.status == 'Approved']
        
        if my_leaves:
            monthly_usage = {}
            for leave in my_leaves:
                month_key = leave.start_date.strftime('%Y-%m')
                if month_key not in monthly_usage:
                    monthly_usage[month_key] = {'Annual': 0, 'Sick': 0, 'Personal': 0}
                
                leave_category = leave.leave_type.split()[0]
                monthly_usage[month_key][leave_category] += leave.days
            
            df_monthly = pd.DataFrame([
                {'Month': k, 'Annual': v['Annual'], 'Sick': v['Sick'], 'Personal': v['Personal']}
                for k, v in sorted(monthly_usage.items())
            ])
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=df_monthly['Month'], y=df_monthly['Annual'], 
                                    mode='lines+markers', name='Annual', line=dict(color='#2c5f7f', width=3)))
            fig.add_trace(go.Scatter(x=df_monthly['Month'], y=df_monthly['Sick'], 
                                    mode='lines+markers', name='Sick', line=dict(color='#4a7fa0', width=3)))
            fig.add_trace(go.Scatter(x=df_monthly['Month'], y=df_monthly['Personal'], 
                                    mode='lines+markers', name='Personal', line=dict(color='#6ba3c5', width=3)))
            
            fig.update_layout(
                title="Your Monthly Leave Usage",
                xaxis_title="Month",
                yaxis_title="Days",
                height=400,
                hovermode='x unified',
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#1a3a52')
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                total_by_type = df_monthly[['Annual', 'Sick', 'Personal']].sum()
                fig_pie = px.pie(
                    values=total_by_type.values,
                    names=total_by_type.index,
                    title="Leave Distribution by Type",
                    color_discrete_sequence=['#2c5f7f', '#4a7fa0', '#6ba3c5']
                )
                fig_pie.update_layout(font=dict(color='#1a3a52'))
                st.plotly_chart(fig_pie, use_container_width=True)
            
            with col2:
                avg_duration = np.mean([lr.days for lr in my_leaves])
                total_leaves = len(my_leaves)
                
                st.metric("Average Leave Duration", f"{avg_duration:.1f} days")
                st.metric("Total Leave Instances", total_leaves)
                st.metric("Total Days Taken", f"{sum(lr.days for lr in my_leaves):.0f}")
        else:
            st.info("No leave history available yet")
    
    with tab2:
        st.subheader("🏥 Wellness & Pattern Insights")
        
        pattern = analyze_sick_leave_patterns(current_user)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Sick Days Taken", f"{pattern['total_days']:.0f}")
        with col2:
            st.metric("Sick Leave Instances", pattern['frequency'])
        with col3:
            alert_emoji = {'green': '✅', 'yellow': '⚠️', 'red': '🚨'}
            st.metric("Status", f"{alert_emoji[pattern['alert_level']]} {pattern['alert_level'].upper()}")
        
        if pattern['alert_level'] != 'green':
            st.warning(f"**Pattern Detected:** {pattern['pattern']}")
            
            if pattern['alert_level'] == 'red':
                st.error("""
                **Wellness Check Recommended**
                
                Your sick leave pattern suggests you might benefit from:
                - A wellness consultation with HR
                - Review of workplace ergonomics
                - Stress management resources
                - Health screening services
                """)
        else:
            st.success("No concerning sick leave patterns detected. Keep up the good health! 💪")
        
        sick_leaves = [lr for lr in st.session_state.leave_requests 
                      if lr.employee_id == current_user and 
                      lr.leave_type == 'Sick Leave' and 
                      lr.status == 'Approved']
        
        if sick_leaves:
            day_counts = {i: 0 for i in range(7)}
            for leave in sick_leaves:
                day_counts[leave.start_date.weekday()] += 1
            
            days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            fig = px.bar(
                x=days,
                y=[day_counts[i] for i in range(7)],
                title="Sick Leave by Day of Week",
                labels={'x': 'Day', 'y': 'Count'},
                color=[day_counts[i] for i in range(7)],
                color_continuous_scale=[[0, '#6ba3c5'], [1, '#1a3a52']]
            )
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#1a3a52')
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        if is_manager:
            st.subheader("👥 Team Analytics")
            
            subordinates = [e for e in st.session_state.employees if e.manager_id == current_user]
            
            team_leaves = [lr for lr in st.session_state.leave_requests 
                          if lr.employee_id in [s.id for s in subordinates] and 
                          lr.status == 'Approved']
            
            if team_leaves:
                team_usage = {}
                for sub in subordinates:
                    sub_leaves = [lr for lr in team_leaves if lr.employee_id == sub.id]
                    team_usage[sub.name] = sum(lr.days for lr in sub_leaves)
                
                fig = px.bar(
                    x=list(team_usage.keys()),
                    y=list(team_usage.values()),
                    title="Team Leave Usage Comparison",
                    labels={'x': 'Employee', 'y': 'Days'},
                    color=list(team_usage.values()),
                    color_continuous_scale=[[0, '#6ba3c5'], [1, '#1a3a52']]
                )
                fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='#1a3a52')
                )
                st.plotly_chart(fig, use_container_width=True)
                
                leave_type_summary = {'Annual': 0, 'Sick': 0, 'Personal': 0}
                for leave in team_leaves:
                    leave_category = leave.leave_type.split()[0]
                    leave_type_summary[leave_category] += leave.days
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Team Annual Leave", f"{leave_type_summary['Annual']:.0f} days")
                with col2:
                    st.metric("Team Sick Leave", f"{leave_type_summary['Sick']:.0f} days")
                with col3:
                    st.metric("Team Personal Leave", f"{leave_type_summary['Personal']:.0f} days")
                
                st.markdown("---")
                st.subheader("🔍 Team Insights")
                
                high_users = [k for k, v in team_usage.items() if v > 15]
                if high_users:
                    st.info(f"**High Leave Utilization:** {', '.join(high_users)}")
                
                for sub in subordinates:
                    pattern = analyze_sick_leave_patterns(sub.id)
                    if pattern['alert_level'] == 'red':
                        st.warning(f"**Wellness Check Recommended for {sub.name}:** {pattern['pattern']}")
            else:
                st.info("No team leave history available")
        else:
            st.info("Team analytics are available for managers only")
    
    with tab4:
        st.subheader("📋 Exportable Reports")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Personal Leave Report**")
            my_leaves = [lr for lr in st.session_state.leave_requests 
                        if lr.employee_id == current_user]
            
            if my_leaves:
                df_report = pd.DataFrame([
                    {
                        'Request ID': lr.id,
                        'Leave Type': lr.leave_type,
                        'Start Date': lr.start_date.strftime('%Y-%m-%d'),
                        'End Date': lr.end_date.strftime('%Y-%m-%d'),
                        'Days': lr.days,
                        'Status': lr.status,
                        'Submitted': lr.submitted_date.strftime('%Y-%m-%d')
                    }
                    for lr in my_leaves
                ])
                
                st.dataframe(df_report, use_container_width=True)
                
                csv = df_report.to_csv(index=False)
                st.download_button(
                    "📥 Download CSV",
                    csv,
                    "my_leave_report.csv",
                    "text/csv",
                    key='download-personal-csv'
                )
        
        with col2:
            if is_manager:
                st.write("**Team Leave Report**")
                subordinates = [e for e in st.session_state.employees if e.manager_id == current_user]
                team_leaves = [lr for lr in st.session_state.leave_requests 
                              if lr.employee_id in [s.id for s in subordinates]]
                
                if team_leaves:
                    df_team_report = pd.DataFrame([
                        {
                            'Employee': get_employee_name(lr.employee_id),
                            'Department': get_employee(lr.employee_id).department,
                            'Leave Type': lr.leave_type,
                            'Start Date': lr.start_date.strftime('%Y-%m-%d'),
                            'End Date': lr.end_date.strftime('%Y-%m-%d'),
                            'Days': lr.days,
                            'Status': lr.status
                        }
                        for lr in team_leaves
                    ])
                    
                    st.dataframe(df_team_report, use_container_width=True)
                    
                    csv_team = df_team_report.to_csv(index=False)
                    st.download_button(
                        "📥 Download Team CSV",
                        csv_team,
                        "team_leave_report.csv",
                        "text/csv",
                        key='download-team-csv'
                    )

def show_settings():
    st.header("⚙️ Settings & Configuration")
    
    current_user = st.session_state.current_user
    emp = get_employee(current_user)
    is_admin = emp.id.startswith('M')
    
    tab1, tab2, tab3, tab4 = st.tabs([
        "👤 Profile",
        "📋 Leave Policies",
        "🎉 Holidays",
        "🔔 Notifications"
    ])
    
    with tab1:
        st.subheader("Profile Information")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.text_input("Name", value=emp.name, disabled=True)
            st.text_input("Email", value=emp.email, disabled=True)
            st.text_input("Employee ID", value=emp.id, disabled=True)
        
        with col2:
            st.text_input("Department", value=emp.department, disabled=True)
            manager = get_employee(emp.manager_id)
            st.text_input("Manager", value=manager.name if manager else "N/A", disabled=True)
            st.text_input("Policy", value=emp.policy, disabled=True)
        
        st.markdown("---")
        st.info("To update your profile information, please contact HR.")
    
    with tab2:
        st.subheader("Leave Policies")
        
        policy = st.session_state.leave_policies[emp.policy]
        
        st.markdown(f"<h3 style='color: #1a3a52;'>Your Current Policy: {emp.policy}</h3>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Annual Leave", f"{policy.annual_days} days")
            st.metric("Sick Leave", f"{policy.sick_days} days")
        with col2:
            st.metric("Personal Leave", f"{policy.personal_days} days")
            st.metric("Carryover Limit", f"{policy.carryover_limit} days")
        with col3:
            st.metric("Max Consecutive", f"{policy.max_consecutive_days} days")
            st.metric("Min Notice", f"{policy.min_notice_days} days")
        
        st.markdown("---")
        
        if is_admin:
            st.subheader("Manage Policies (Admin)")
            
            with st.expander("View All Policies"):
                for policy_name, policy_obj in st.session_state.leave_policies.items():
                    st.markdown(f"""
                    <div class="leave-card">
                        <h4 style="color: #1a3a52; margin-top: 0;">{policy_name} Policy</h4>
                        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px;">
                            <div>
                                <p style="margin: 5px 0; color: #2c5f7f;"><strong>Annual:</strong> {policy_obj.annual_days}</p>
                                <p style="margin: 5px 0; color: #2c5f7f;"><strong>Sick:</strong> {policy_obj.sick_days}</p>
                            </div>
                            <div>
                                <p style="margin: 5px 0; color: #2c5f7f;"><strong>Personal:</strong> {policy_obj.personal_days}</p>
                                <p style="margin: 5px 0; color: #2c5f7f;"><strong>Carryover:</strong> {policy_obj.carryover_limit}</p>
                            </div>
                            <div>
                                <p style="margin: 5px 0; color: #2c5f7f;"><strong>Max Consecutive:</strong> {policy_obj.max_consecutive_days}</p>
                                <p style="margin: 5px 0; color: #2c5f7f;"><strong>Min Notice:</strong> {policy_obj.min_notice_days}</p>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
    
    with tab3:
        st.subheader("Company Holidays")
        
        upcoming_holidays = sorted(st.session_state.holidays, key=lambda x: x['date'])
        
        for holiday in upcoming_holidays:
            col1, col2, col3 = st.columns([3, 2, 1])
            with col1:
                st.markdown(f"<p style='color: #1a3a52; font-weight: 600; margin: 10px 0;'>🎉 {holiday['name']}</p>", unsafe_allow_html=True)
            with col2:
                st.markdown(f"<p style='color: #2c5f7f; margin: 10px 0;'>{holiday['date'].strftime('%B %d, %Y')}</p>", unsafe_allow_html=True)
            with col3:
                if is_admin:
                    if st.button("🗑️ Delete", key=f"del_holiday_{holiday['date']}"):
                        st.session_state.holidays.remove(holiday)
                        st.rerun()
        
        if is_admin:
            st.markdown("---")
            with st.expander("➕ Add New Holiday"):
                col1, col2 = st.columns(2)
                with col1:
                    new_holiday_name = st.text_input("Holiday Name")
                with col2:
                    new_holiday_date = st.date_input("Date", min_value=datetime.now().date())
                
                if st.button("Add Holiday", type="primary"):
                    if new_holiday_name:
                        st.session_state.holidays.append({
                            'date': datetime.combine(new_holiday_date, datetime.min.time()),
                            'name': new_holiday_name
                        })
                        st.success(f"Added {new_holiday_name}")
                        st.rerun()
    
    with tab4:
        st.subheader("Notification Preferences")
        
        st.markdown("""
        <div class="leave-card">
            <h4 style="color: #1a3a52; margin-top: 0;">Email Notifications</h4>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.checkbox("✉️ Leave approval notifications", value=True)
            st.checkbox("✉️ Leave rejection notifications", value=True)
            st.checkbox("✉️ Pending request reminders", value=True)
        with col2:
            st.checkbox("✉️ Team availability alerts", value=True)
            st.checkbox("✉️ Leave balance reminders", value=False)
            st.checkbox("✉️ Policy update notifications", value=True)
        
        st.markdown("---")
        
        st.markdown("""
        <div class="leave-card">
            <h4 style="color: #1a3a52; margin-top: 0;">Integration Settings</h4>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.checkbox("📅 Sync with Google Calendar", value=False)
            st.checkbox("📅 Sync with Outlook", value=False)
            st.checkbox("💬 Enable Slack notifications", value=False)
        with col2:
            st.checkbox("💰 Payroll system integration", value=True)
            st.checkbox("📊 Export to HRIS", value=False)
            st.checkbox("📱 Mobile app notifications", value=True)
        
        st.markdown("---")
        
        if st.button("💾 Save Preferences", type="primary", use_container_width=False):
            st.success("✅ Preferences saved successfully!")
            st.balloons()

if __name__ == "__main__":
    main()
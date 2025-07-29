import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json

# Sayfa konfigürasyonu
st.set_page_config(
    page_title="AI Bütçe Planlayıcısı",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS stilleri
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .success-metric {
        border-left-color: #28a745;
    }
    .warning-metric {
        border-left-color: #ffc107;
    }
    .danger-metric {
        border-left-color: #dc3545;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.title("💰 AI Bütçe Planlayıcısı")
    st.markdown("---")
    
    # Kullanıcı bilgileri
    st.subheader("👤 Kullanıcı Bilgileri")
    user_name = st.text_input("Adınız:", placeholder="Adınızı girin")
    monthly_income = st.number_input("Aylık Geliriniz (TL):", min_value=0, value=5000)
    
    # Bütçe kategorileri
    st.subheader("📊 Bütçe Kategorileri")
    housing = st.number_input("Konut (Kira/Ev):", min_value=0, value=1500)
    food = st.number_input("Yemek:", min_value=0, value=800)
    transport = st.number_input("Ulaşım:", min_value=0, value=400)
    utilities = st.number_input("Faturalar:", min_value=0, value=300)
    entertainment = st.number_input("Eğlence:", min_value=0, value=300)
    savings = st.number_input("Tasarruf:", min_value=0, value=500)
    other = st.number_input("Diğer:", min_value=0, value=200)
    
    # AI önerileri için buton
    if st.button("🤖 AI Önerileri Al", type="primary"):
        st.session_state.get_ai_suggestions = True

# Ana sayfa
st.markdown('<h1 class="main-header">💰 AI Bütçe Planlayıcısı</h1>', unsafe_allow_html=True)

# Backend bağlantı kontrolü
@st.cache_data
def check_backend():
    try:
        response = requests.get("http://localhost:5000/health")
        return response.status_code == 200
    except:
        return False

backend_status = check_backend()

if not backend_status:
    st.error("⚠️ Backend sunucusu çalışmıyor! Lütfen backend'i başlatın.")
    st.stop()

# Bütçe hesaplamaları
total_expenses = housing + food + transport + utilities + entertainment + savings + other
remaining_budget = monthly_income - total_expenses
savings_rate = (savings / monthly_income) * 100 if monthly_income > 0 else 0

# Metrikler
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="metric-card {'success-metric' if remaining_budget >= 0 else 'danger-metric'}">
        <h3>💰 Kalan Bütçe</h3>
        <h2>{remaining_budget:,.0f} TL</h2>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card {'success-metric' if savings_rate >= 20 else 'warning-metric'}">
        <h3>💎 Tasarruf Oranı</h3>
        <h2>{savings_rate:.1f}%</h2>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <h3>📊 Toplam Gider</h3>
        <h2>{total_expenses:,.0f} TL</h2>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card">
        <h3>💵 Aylık Gelir</h3>
        <h2>{monthly_income:,.0f} TL</h2>
    </div>
    """, unsafe_allow_html=True)

# Grafikler
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Gider Dağılımı")
    
    # Gider verileri
    expenses_data = {
        'Kategori': ['Konut', 'Yemek', 'Ulaşım', 'Faturalar', 'Eğlence', 'Tasarruf', 'Diğer'],
        'Tutar': [housing, food, transport, utilities, entertainment, savings, other]
    }
    
    df_expenses = pd.DataFrame(expenses_data)
    
    fig_pie = px.pie(
        df_expenses, 
        values='Tutar', 
        names='Kategori',
        title="Aylık Gider Dağılımı",
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    fig_pie.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig_pie, use_container_width=True)

with col2:
    st.subheader("📈 Bütçe Durumu")
    
    # Bütçe durumu grafiği
    budget_data = {
        'Kategori': ['Gelir', 'Gider', 'Kalan'],
        'Tutar': [monthly_income, total_expenses, remaining_budget]
    }
    
    df_budget = pd.DataFrame(budget_data)
    
    fig_bar = px.bar(
        df_budget,
        x='Kategori',
        y='Tutar',
        title="Gelir vs Gider Analizi",
        color='Kategori',
        color_discrete_map={
            'Gelir': '#28a745',
            'Gider': '#dc3545',
            'Kalan': '#17a2b8'
        }
    )
    st.plotly_chart(fig_bar, use_container_width=True)

# AI Önerileri
if st.session_state.get('get_ai_suggestions', False):
    st.markdown("---")
    st.subheader("🤖 AI Bütçe Önerileri")
    
    try:
        # Backend'e veri gönder
        budget_data = {
            "monthly_income": monthly_income,
            "expenses": {
                "housing": housing,
                "food": food,
                "transport": transport,
                "utilities": utilities,
                "entertainment": entertainment,
                "savings": savings,
                "other": other
            }
        }
        
        response = requests.post("http://localhost:5000/analyze", json=budget_data)
        
        if response.status_code == 200:
            ai_suggestions = response.json()
            
            # Önerileri göster
            for i, suggestion in enumerate(ai_suggestions['suggestions'], 1):
                with st.expander(f"💡 Öneri {i}: {suggestion['title']}"):
                    st.write(suggestion['description'])
                    if 'action' in suggestion:
                        st.info(f"**Önerilen Eylem:** {suggestion['action']}")
        else:
            st.error("AI önerileri alınırken hata oluştu.")
            
    except Exception as e:
        st.error(f"Backend bağlantısında hata: {e}")

# Gelecek planlama
st.markdown("---")
st.subheader("🎯 Gelecek Planlama")

col1, col2 = st.columns(2)

with col1:
    st.subheader("💎 Tasarruf Hedefleri")
    target_savings = st.number_input("Aylık Tasarruf Hedefi (TL):", min_value=0, value=1000)
    current_savings = savings
    
    if current_savings >= target_savings:
        st.success(f"🎉 Hedefinize ulaştınız! {current_savings} TL tasarruf ediyorsunuz.")
    else:
        needed = target_savings - current_savings
        st.warning(f"⚠️ Hedefinize ulaşmak için {needed} TL daha tasarruf etmelisiniz.")

with col2:
    st.subheader("🔮 Gelecek Ay Tahmini")
    if remaining_budget > 0:
        st.success(f"✅ Gelecek ay {remaining_budget} TL tasarruf edebilirsiniz.")
    else:
        st.error(f"⚠️ Gelecek ay {abs(remaining_budget)} TL açık verebilirsiniz.")

# Alt bilgi
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>💡 Bu uygulama, finansal farkındalığınızı artırmak ve tasarruf hedeflerinize ulaşmanız için tasarlandı.</p>
    <p>🤖 AI destekli öneriler ile daha akıllı finansal kararlar alın!</p>
</div>
""", unsafe_allow_html=True)
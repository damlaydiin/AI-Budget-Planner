from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import json
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Frontend ile iletişim için

# Basit veri saklama (gerçek uygulamada veritabanı kullanılır)
budget_data = []

@app.route('/')
def home():
    return jsonify({
        "message": "AI Budget Planner Backend API",
        "status": "running",
        "endpoints": [
            "/health",
            "/analyze",
            "/budget",
            "/suggestions"
        ]
    })

@app.route('/health')
def health_check():
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "AI Budget Planner Backend"
    })

@app.route('/analyze', methods=['POST'])
def analyze_budget():
    try:
        data = request.get_json()
        
        monthly_income = data.get('monthly_income', 0)
        expenses = data.get('expenses', {})
        
        # Toplam gider hesaplama
        total_expenses = sum(expenses.values())
        remaining_budget = monthly_income - total_expenses
        savings_rate = (expenses.get('savings', 0) / monthly_income * 100) if monthly_income > 0 else 0
        
        # AI önerileri oluştur
        suggestions = generate_ai_suggestions(monthly_income, expenses, remaining_budget, savings_rate)
        
        return jsonify({
            "status": "success",
            "analysis": {
                "total_expenses": total_expenses,
                "remaining_budget": remaining_budget,
                "savings_rate": savings_rate,
                "budget_status": "healthy" if remaining_budget >= 0 else "over_budget"
            },
            "suggestions": suggestions
        })
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 400

def generate_ai_suggestions(income, expenses, remaining, savings_rate):
    suggestions = []
    
    # Tasarruf oranı önerileri
    if savings_rate < 20:
        suggestions.append({
            "title": "Tasarruf Oranınızı Artırın",
            "description": f"Şu anda gelirinizin %{savings_rate:.1f}'ini tasarruf ediyorsunuz. Finansal güvenlik için %20-30 arası önerilir.",
            "action": "Aylık tasarruf hedefinizi gelirinizin %20'sine çıkarın."
        })
    
    # Bütçe açığı kontrolü
    if remaining < 0:
        suggestions.append({
            "title": "Bütçe Açığınızı Kapatın",
            "description": f"Gelirinizden {abs(remaining)} TL fazla harcıyorsunuz. Bu durum borç birikimine yol açabilir.",
            "action": "Gereksiz harcamaları azaltın veya gelirinizi artırın."
        })
    
    # Kategori bazlı öneriler
    housing_ratio = (expenses.get('housing', 0) / income * 100) if income > 0 else 0
    if housing_ratio > 30:
        suggestions.append({
            "title": "Konut Giderlerinizi Gözden Geçirin",
            "description": f"Konut giderleriniz gelirinizin %{housing_ratio:.1f}'ini oluşturuyor. %30'un altında olması önerilir.",
            "action": "Daha uygun konut seçenekleri değerlendirin."
        })
    
    food_ratio = (expenses.get('food', 0) / income * 100) if income > 0 else 0
    if food_ratio > 15:
        suggestions.append({
            "title": "Yemek Giderlerinizi Optimize Edin",
            "description": f"Yemek giderleriniz gelirinizin %{food_ratio:.1f}'ini oluşturuyor. Ev yemekleri ve toplu alışveriş tasarruf sağlar.",
            "action": "Ev yemeklerine ağırlık verin ve toplu alışveriş yapın."
        })
    
    # Genel öneriler
    if len(suggestions) < 3:
        suggestions.append({
            "title": "Acil Durum Fonu Oluşturun",
            "description": "En az 3-6 aylık giderinizi karşılayacak acil durum fonu oluşturun.",
            "action": "Aylık gelirinizin %10'unu acil durum fonuna ayırın."
        })
    
    if remaining > 0 and savings_rate < 30:
        suggestions.append({
            "title": "Tasarruf Potansiyelinizi Değerlendirin",
            "description": f"Kalan bütçenizden {remaining} TL daha tasarruf edebilirsiniz.",
            "action": "Kalan bütçenizi tasarruf hesaplarınıza aktarın."
        })
    
    return suggestions

@app.route('/budget', methods=['GET', 'POST'])
def budget_endpoint():
    if request.method == 'POST':
        data = request.get_json()
        budget_data.append({
            'timestamp': datetime.now().isoformat(),
            'data': data
        })
        return jsonify({"status": "saved", "message": "Bütçe verisi kaydedildi"})
    else:
        return jsonify({"budgets": budget_data})

@app.route('/suggestions')
def get_suggestions():
    return jsonify({
        "general_tips": [
            "Gelirinizin %50'sini temel ihtiyaçlara ayırın",
            "Gelirinizin %30'unu isteklerinize ayırın", 
            "Gelirinizin %20'sini tasarruf ve yatırıma ayırın"
        ],
        "savings_tips": [
            "Otomatik tasarruf transferleri kurun",
            "Gereksiz abonelikleri iptal edin",
            "Toplu alışveriş yapın",
            "Enerji tasarrufu yapın"
        ]
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
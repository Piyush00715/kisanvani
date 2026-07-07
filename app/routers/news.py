from fastapi import APIRouter

router = APIRouter()

MOCK_NEWS = [
    {
        "id": 1,
        "title": "PM-Kisan 16th Installment Released: Check Your Status",
        "category": "Government Schemes",
        "thumbnail": "https://images.unsplash.com/photo-1592982537447-7440770cbfc9?q=80&w=2069&auto=format&fit=crop",
        "date": "2 Days Ago",
        "summary": "The government has released the latest installment of the PM-Kisan Samman Nidhi Yojana. Over 9 crore farmers have directly received ₹2,000 in their bank accounts."
    },
    {
        "id": 2,
        "title": "New Subsidy Announced for Micro-Irrigation Systems",
        "category": "Subsidies",
        "thumbnail": "https://images.unsplash.com/photo-1560493676-04071c5f467b?q=80&w=1974&auto=format&fit=crop",
        "date": "5 Days Ago",
        "summary": "Under the Pradhan Mantri Krishi Sinchayee Yojana (PMKSY), the center announced a 50% subsidy for farmers adopting drip and sprinkler irrigation to combat water scarcity."
    },
    {
        "id": 3,
        "title": "Monsoon Arrives Early: Good News for Kharif Sowing",
        "category": "Weather Alert",
        "thumbnail": "https://images.unsplash.com/photo-1515694346937-94d85e41e6f0?q=80&w=2127&auto=format&fit=crop",
        "date": "1 Week Ago",
        "summary": "The IMD has reported an early onset of the Southwest Monsoon. Farmers are advised to prepare their fields for Kharif crops like paddy, maize, and soybean."
    },
    {
        "id": 4,
        "title": "Soil Health Card Scheme Surpasses 20 Crore Issuances",
        "category": "Government Schemes",
        "thumbnail": "https://images.unsplash.com/photo-1464226184884-fa280b87c399?q=80&w=2070&auto=format&fit=crop",
        "date": "2 Weeks Ago",
        "summary": "The Soil Health Card scheme helps farmers understand their soil's nutrient status. The government urges remaining farmers to apply for free soil testing."
    },
    {
        "id": 5,
        "title": "Fasal Bima Yojana: Last Date for Registration Extended",
        "category": "Alert",
        "thumbnail": "https://images.unsplash.com/photo-1605000797499-95a51c5269ae?q=80&w=2071&auto=format&fit=crop",
        "date": "Yesterday",
        "summary": "Farmers can now register for the Pradhan Mantri Fasal Bima Yojana (PMFBY) until the end of this month to insure their crops against natural calamities."
    }
]

@router.get("/latest")
def get_latest_news():
    return {"status": "success", "data": MOCK_NEWS}

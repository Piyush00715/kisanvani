import sqlite3
from fastapi import APIRouter, HTTPException

router = APIRouter()
DB_PATH = "kisanvani.db"

@router.get("/logs")
def get_rsk_logs():
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        query = """
            SELECT 
                h.id,
                h.timestamp,
                h.phone_number,
                h.details,
                u.state,
                u.latitude,
                u.longitude,
                u.preferred_language
            FROM history h
            LEFT JOIN users u ON h.phone_number = u.phone_number
            WHERE h.action_type = 'Disease Detection'
            ORDER BY h.timestamp DESC
        """
        
        rows = cursor.execute(query).fetchall()
        
        logs = []
        for row in rows:
            logs.append(dict(row))
            
        conn.close()
        return {"status": "success", "logs": logs}
    except Exception as e:
        print("Error fetching RSK logs:", e)
        raise HTTPException(status_code=500, detail=str(e))

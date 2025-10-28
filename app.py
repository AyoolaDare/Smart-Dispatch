from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import ConnectionError, NotFoundError
from datetime import datetime
from typing import Optional, List, Dict, Any
import os
from dotenv import load_dotenv
import uuid
import math

load_dotenv()

app = FastAPI(title="ATM Smart Dispatch API", version="1.0.0")

# Initialize Elasticsearch
CLOUD_ID = os.getenv("ELASTIC_CLOUD_ID")
API_KEY = os.getenv("ELASTIC_API_KEY")

es = Elasticsearch(
    cloud_id=CLOUD_ID,
    api_key=API_KEY
)

# ============= PYDANTIC MODELS =============

class Location(BaseModel):
    lat: float
    lng: float
    address: str

class ATMAsset(BaseModel):
    atm_id: str
    location: Location
    model: str
    installed_date: str
    status: str = "active"  # active, maintenance, decommissioned
    cash_capacity: int
    notes: Optional[str] = None

class EngineerAsset(BaseModel):
    engineer_id: str
    name: str
    phone: str
    email: str
    location: Location
    skill_level: str  # junior, senior, specialist
    available: bool = True
    current_workload: int = 0
    certification: Optional[str] = None

class ATMLog(BaseModel):
    atm_id: str
    status: str  # active, error, warning
    error_code: Optional[str] = None
    error_description: Optional[str] = None
    cash_status: str  # normal, low, out
    card_reader_status: str  # operational, warning, faulty
    dispenser_status: str  # operational, warning, faulty
    network_status: str  # online, offline
    uptime_percentage: float
    temperature: float
    transaction_count: int
    failed_transactions: int
    last_transaction_time: Optional[str] = None

class DispatchTicket(BaseModel):
    atm_id: str
    fault_type: str
    severity: str
    engineer_id: Optional[str] = None
    status: str = "pending"
    priority: int = 0

class EngineerResolution(BaseModel):
    ticket_id: str
    engineer_id: str
    resolution_notes: str
    photo_evidence_url: Optional[str] = None
    resolution_time_minutes: int

# ============= INDICES INITIALIZATION =============

@app.on_event("startup")
async def init_indices():
    """Initialize Elasticsearch indices with proper mappings"""
    print("\n" + "="*60)
    print("📑 INITIALIZING ELASTICSEARCH INDICES")
    print("="*60)
    
    indices = {
        "atm-assets": {
            "settings": {
                "number_of_shards": 1,
                "number_of_replicas": 1
            },
            "mappings": {
                "properties": {
                    "atm_id": {"type": "keyword"},
                    "location": {"type": "geo_point"},
                    "status": {"type": "keyword"},
                    "model": {"type": "text"},
                    "installed_date": {"type": "date"},
                    "cash_capacity": {"type": "integer"},
                    "registered_at": {"type": "date"}
                }
            }
        },
        "engineer-assets": {
            "settings": {
                "number_of_shards": 1,
                "number_of_replicas": 1
            },
            "mappings": {
                "properties": {
                    "engineer_id": {"type": "keyword"},
                    "name": {"type": "text"},
                    "phone": {"type": "keyword"},
                    "email": {"type": "keyword"},
                    "location": {"type": "geo_point"},
                    "skill_level": {"type": "keyword"},
                    "available": {"type": "boolean"},
                    "current_workload": {"type": "integer"},
                    "certification": {"type": "text"},
                    "registered_at": {"type": "date"}
                }
            }
        },
        "atm-logs": {
            "settings": {
                "number_of_shards": 2,
                "number_of_replicas": 1
            },
            "mappings": {
                "properties": {
                    "atm_id": {"type": "keyword"},
                    "timestamp": {"type": "date"},
                    "received_at": {"type": "date"},
                    "status": {"type": "keyword"},
                    "error_code": {"type": "keyword"},
                    "error_description": {"type": "text"},
                    "card_reader_status": {"type": "keyword"},
                    "dispenser_status": {"type": "keyword"},
                    "network_status": {"type": "keyword"},
                    "cash_status": {"type": "keyword"},
                    "uptime_percentage": {"type": "float"},
                    "temperature": {"type": "float"},
                    "transaction_count": {"type": "integer"},
                    "failed_transactions": {"type": "integer"},
                    "last_transaction_time": {"type": "date"}
                }
            }
        },
        "dispatch-tickets": {
            "settings": {
                "number_of_shards": 1,
                "number_of_replicas": 1
            },
            "mappings": {
                "properties": {
                    "ticket_id": {"type": "keyword"},
                    "atm_id": {"type": "keyword"},
                    "engineer_id": {"type": "keyword"},
                    "status": {"type": "keyword"},
                    "fault_type": {"type": "keyword"},
                    "severity": {"type": "keyword"},
                    "priority": {"type": "integer"},
                    "created_at": {"type": "date"},
                    "resolved_at": {"type": "date"}
                }
            }
        },
        "resolutions": {
            "settings": {
                "number_of_shards": 1,
                "number_of_replicas": 1
            },
            "mappings": {
                "properties": {
                    "resolution_id": {"type": "keyword"},
                    "ticket_id": {"type": "keyword"},
                    "engineer_id": {"type": "keyword"},
                    "resolution_notes": {"type": "text"},
                    "photo_evidence_url": {"type": "keyword"},
                    "resolution_time_minutes": {"type": "integer"},
                    "submitted_at": {"type": "date"}
                }
            }
        }
    }
    
    for idx, config in indices.items():
        try:
            if es.indices.exists(index=idx):
                print(f"⚠️  Index already exists: {idx}")
            else:
                es.indices.create(
                    index=idx,
                    settings=config["settings"],
                    mappings=config["mappings"]
                )
                print(f"✅ Index created: {idx}")
        except Exception as e:
            print(f"❌ Error creating index {idx}: {e}")
    
    print("="*60 + "\n")

# ============= ASSET MANAGEMENT - ATMs =============

@app.post("/api/v1/assets/atms", status_code=status.HTTP_201_CREATED)
async def register_atm_asset(atm: ATMAsset):
    """Register a new ATM asset"""
    try:
        result = es.index(
            index="atm-assets",
            id=atm.atm_id,
            document={
                **atm.dict(),
                "location": {"lat": atm.location.lat, "lon": atm.location.lng},
                "registered_at": datetime.now().isoformat()
            }
        )
        return {"success": True, "atm_id": result['_id']}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/v1/assets/atms")
async def list_all_atms():
    """List all ATM assets"""
    try:
        results = es.search(index="atm-assets", query={"match_all": {}}, size=1000)
        return {
            "total": results['hits']['total']['value'],
            "atms": [hit['_source'] for hit in results['hits']['hits']]
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/v1/assets/atms/{atm_id}")
async def get_atm_asset(atm_id: str):
    """Get specific ATM asset details"""
    try:
        result = es.get(index="atm-assets", id=atm_id)
        return result['_source']
    except NotFoundError:
        raise HTTPException(status_code=404, detail="ATM not found")

@app.patch("/api/v1/assets/atms/{atm_id}")
async def update_atm_asset(atm_id: str, status: Optional[str] = None, location: Optional[Location] = None):
    """Update ATM asset status or location"""
    try:
        update_data = {}
        if status:
            update_data["status"] = status
        if location:
            update_data["location"] = {"lat": location.lat, "lon": location.lng}
        
        es.update(index="atm-assets", id=atm_id, doc=update_data)
        return {"success": True, "atm_id": atm_id}
    except NotFoundError:
        raise HTTPException(status_code=404, detail="ATM not found")

# ============= ASSET MANAGEMENT - ENGINEERS =============

@app.post("/api/v1/assets/engineers", status_code=status.HTTP_201_CREATED)
async def register_engineer_asset(engineer: EngineerAsset):
    """Register a new engineer asset"""
    try:
        result = es.index(
            index="engineer-assets",
            id=engineer.engineer_id,
            document={
                **engineer.dict(),
                "location": {"lat": engineer.location.lat, "lon": engineer.location.lng},
                "registered_at": datetime.now().isoformat()
            }
        )
        return {"success": True, "engineer_id": result['_id']}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/v1/assets/engineers")
async def list_all_engineers(available_only: bool = False):
    """List all engineer assets"""
    try:
        query = {"match": {"available": True}} if available_only else {"match_all": {}}
        results = es.search(index="engineer-assets", query=query, size=1000)
        return {
            "total": results['hits']['total']['value'],
            "engineers": [hit['_source'] for hit in results['hits']['hits']]
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/v1/assets/engineers/{engineer_id}")
async def get_engineer_asset(engineer_id: str):
    """Get specific engineer asset details"""
    try:
        result = es.get(index="engineer-assets", id=engineer_id)
        return result['_source']
    except NotFoundError:
        raise HTTPException(status_code=404, detail="Engineer not found")

@app.patch("/api/v1/assets/engineers/{engineer_id}")
async def update_engineer_asset(engineer_id: str, available: Optional[bool] = None, location: Optional[Location] = None):
    """Update engineer availability and location"""
    try:
        update_data = {}
        if available is not None:
            update_data["available"] = available
        if location:
            update_data["location"] = {"lat": location.lat, "lon": location.lng}
        
        es.update(index="engineer-assets", id=engineer_id, doc=update_data)
        return {"success": True, "engineer_id": engineer_id}
    except NotFoundError:
        raise HTTPException(status_code=404, detail="Engineer not found")

# ============= LOG INGESTION =============

@app.post("/api/v1/logs/atm", status_code=status.HTTP_201_CREATED)
async def ingest_atm_log(log: ATMLog):
    """Ingest ATM telemetry logs"""
    try:
        doc_id = f"{log.atm_id}-{datetime.now().isoformat()}"
        result = es.index(
            index="atm-logs",
            id=doc_id,
            document={
                **log.dict(),
                "timestamp": datetime.now().isoformat(),
                "received_at": datetime.now().isoformat()
            }
        )
        
        # Check for faults using detection rules
        await check_fault_detection(log)
        
        return {
            "success": True,
            "message": "Log ingested",
            "doc_id": result['_id']
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# ============= FAULT DETECTION RULES =============

async def check_fault_detection(log: ATMLog):
    """Check if log triggers any fault detection rules"""
    
    fault_detected = None
    severity = "low"
    
    # RULE 1: Card Reader Failure
    if log.card_reader_status == "faulty":
        fault_detected = "CARD_READER_FAILURE"
        severity = "high"
    
    # RULE 2: Dispenser Failure
    elif log.dispenser_status == "faulty":
        fault_detected = "DISPENSER_FAILURE"
        severity = "high"
    
    # RULE 3: Network Offline
    elif log.network_status == "offline":
        fault_detected = "NETWORK_OFFLINE"
        severity = "critical"
    
    # RULE 4: Multiple Failed Transactions (>5 in single log)
    elif log.failed_transactions > 5:
        fault_detected = "HIGH_FAILURE_RATE"
        severity = "medium"
    
    # RULE 5: Cash Status Critical
    elif log.cash_status == "out":
        fault_detected = "CASH_OUT"
        severity = "high"
    
    # RULE 6: Low Uptime (<80%)
    elif log.uptime_percentage < 80:
        fault_detected = "LOW_UPTIME"
        severity = "medium"
    
    # RULE 7: High Temperature
    elif log.temperature > 45:
        fault_detected = "HIGH_TEMPERATURE"
        severity = "medium"
    
    if fault_detected:
        await trigger_dispatch_workflow(log.atm_id, fault_detected, severity)

async def trigger_dispatch_workflow(atm_id: str, fault_type: str, severity: str):
    """Trigger automatic dispatch workflow when fault is detected"""
    try:
        # Create dispatch ticket
        ticket_id = str(uuid.uuid4())
        es.index(
            index="dispatch-tickets",
            id=ticket_id,
            document={
                "ticket_id": ticket_id,
                "atm_id": atm_id,
                "fault_type": fault_type,
                "severity": severity,
                "status": "pending",
                "engineer_id": None,
                "created_at": datetime.now().isoformat()
            }
        )
        
        # Find nearest available engineer
        engineer_id = await find_nearest_engineer(atm_id, fault_type)
        
        if engineer_id:
            # Assign engineer
            es.update(
                index="dispatch-tickets",
                id=ticket_id,
                doc={
                    "engineer_id": engineer_id,
                    "status": "assigned"
                }
            )
            print(f"✅ Ticket {ticket_id} assigned to engineer {engineer_id}")
        else:
            print(f"⚠️  Ticket {ticket_id} created but no engineer available")
            
    except Exception as e:
        print(f"❌ Error in dispatch workflow: {str(e)}")

async def find_nearest_engineer(atm_id: str, fault_type: str) -> Optional[str]:
    """Find nearest available engineer using geo-proximity"""
    try:
        # Get ATM location
        atm_asset = es.get(index="atm-assets", id=atm_id)['_source']
        atm_lat = atm_asset['location']['lat']
        atm_lng = atm_asset['location']['lon']
        
        # Get available engineers
        available_engineers = es.search(
            index="engineer-assets",
            query={"match": {"available": True}},
            size=100
        )
        
        if not available_engineers['hits']['hits']:
            return None
        
        # Calculate distance and find nearest
        nearest_engineer = None
        min_distance = float('inf')
        
        for eng in available_engineers['hits']['hits']:
            eng_data = eng['_source']
            eng_lat = eng_data['location']['lat']
            eng_lng = eng_data['location']['lon']
            
            # Haversine distance calculation
            distance = calculate_distance(atm_lat, atm_lng, eng_lat, eng_lng)
            
            # Prioritize by skill level for certain fault types
            skill_priority = get_skill_priority(eng_data['skill_level'], fault_type)
            
            # Weighted distance (distance - skill bonus)
            weighted_distance = distance - skill_priority
            
            if weighted_distance < min_distance:
                min_distance = weighted_distance
                nearest_engineer = eng_data['engineer_id']
        
        return nearest_engineer
        
    except Exception as e:
        print(f"Error finding nearest engineer: {str(e)}")
        return None

def calculate_distance(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    """Calculate distance between two coordinates in km"""
    R = 6371  # Earth's radius in km
    dlat = math.radians(lat2 - lat1)
    dlng = math.radians(lng2 - lng1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlng/2)**2
    c = 2 * math.asin(math.sqrt(a))
    return R * c

def get_skill_priority(skill_level: str, fault_type: str) -> float:
    """Get priority bonus based on engineer skill and fault type"""
    priority_map = {
        "specialist": {"CARD_READER_FAILURE": 5, "DISPENSER_FAILURE": 5, "default": 3},
        "senior": {"CARD_READER_FAILURE": 3, "DISPENSER_FAILURE": 3, "default": 2},
        "junior": {"default": 0}
    }
    
    if skill_level in priority_map:
        return priority_map[skill_level].get(fault_type, priority_map[skill_level].get("default", 0))
    return 0

# ============= DISPATCH ENDPOINTS =============

@app.get("/api/v1/dispatch/tickets")
async def get_all_tickets(status: Optional[str] = None):
    """Get all dispatch tickets"""
    try:
        query = {"match_all": {}} if not status else {"match": {"status": status}}
        results = es.search(index="dispatch-tickets", query=query, sort=[{"created_at": {"order": "desc"}}], size=100)
        return {
            "total": results['hits']['total']['value'],
            "tickets": [hit['_source'] for hit in results['hits']['hits']]
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/v1/dispatch/tickets/{ticket_id}")
async def get_ticket(ticket_id: str):
    """Get ticket details"""
    try:
        result = es.get(index="dispatch-tickets", id=ticket_id)
        return result['_source']
    except NotFoundError:
        raise HTTPException(status_code=404, detail="Ticket not found")

@app.patch("/api/v1/dispatch/tickets/{ticket_id}/status")
async def update_ticket_status(ticket_id: str, status: str):
    """Update ticket status"""
    try:
        es.update(index="dispatch-tickets", id=ticket_id, doc={"status": status})
        return {"success": True}
    except NotFoundError:
        raise HTTPException(status_code=404, detail="Ticket not found")

# ============= RESOLUTION ENDPOINTS =============

@app.post("/api/v1/resolutions", status_code=status.HTTP_201_CREATED)
async def submit_resolution(resolution: EngineerResolution):
    """Submit resolution"""
    try:
        resolution_id = str(uuid.uuid4())
        es.index(
            index="resolutions",
            id=resolution_id,
            document={
                **resolution.dict(),
                "resolution_id": resolution_id,
                "submitted_at": datetime.now().isoformat()
            }
        )
        
        # Update ticket
        es.update(
            index="dispatch-tickets",
            id=resolution.ticket_id,
            doc={"status": "resolved", "resolved_at": datetime.now().isoformat()}
        )
        
        return {"success": True, "resolution_id": resolution_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# ============= DASHBOARD ENDPOINTS =============

@app.get("/api/v1/dashboard/overview")
async def dashboard_overview():
    """Get dashboard overview"""
    try:
        atm_count = es.search(index="atm-assets", query={"match_all": {}}, size=0)
        engineer_count = es.search(index="engineer-assets", query={"match_all": {}}, size=0)
        active_tickets = es.search(index="dispatch-tickets", query={"terms": {"status": ["pending", "assigned", "in_progress"]}}, size=0)
        resolved_today = es.search(index="dispatch-tickets", query={"range": {"resolved_at": {"gte": "now-1d"}}}, size=0)
        
        return {
            "total_atms": atm_count['hits']['total']['value'],
            "total_engineers": engineer_count['hits']['total']['value'],
            "active_incidents": active_tickets['hits']['total']['value'],
            "resolved_today": resolved_today['hits']['total']['value']
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/health")
async def health():
    """Health check"""
    try:
        es.info()
        return {"status": "healthy"}
    except:
        return {"status": "unhealthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
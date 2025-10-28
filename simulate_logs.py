import requests
import json
import time
import random
from datetime import datetime
from typing import List, Dict

BASE_URL = "http://localhost:8000"

class ATMAssetManager:
    """Manage ATM and Engineer assets"""
    
    def __init__(self):
        self.session = requests.Session()
    
    def create_atm_assets(self):
        """Create sample ATM assets"""
        atms = [
            {
                "atm_id": "ATM-045",
                "location": {"lat": 6.5244, "lng": 3.3792, "address": "Ikoyi, Lagos"},
                "model": "Diebold Nixdorf 5585",
                "installed_date": "2022-01-15",
                "cash_capacity": 5000000
            },
            {
                "atm_id": "ATM-046",
                "location": {"lat": 6.5300, "lng": 3.3850, "address": "Victoria Island, Lagos"},
                "model": "NCR SelfServ 5000",
                "installed_date": "2021-06-20",
                "cash_capacity": 4000000
            },
            {
                "atm_id": "ATM-047",
                "location": {"lat": 6.5200, "lng": 3.3700, "address": "Lekki, Lagos"},
                "model": "Wincor Nixdorf ProCash",
                "installed_date": "2023-03-10",
                "cash_capacity": 6000000
            }
        ]
        
        print("\n📋 CREATING ATM ASSETS")
        print("=" * 60)
        for atm in atms:
            try:
                response = self.session.post(f"{BASE_URL}/api/v1/assets/atms", json=atm)
                if response.status_code == 201:
                    print(f"✅ ATM Created: {atm['atm_id']} - {atm['location']['address']}")
                else:
                    print(f"❌ Failed to create ATM: {response.text}")
            except Exception as e:
                print(f"❌ Error: {str(e)}")
    
    def create_engineer_assets(self):
        """Create sample engineer assets"""
        engineers = [
            {
                "engineer_id": "ENG-001",
                "name": "Chidi Okafor",
                "phone": "+234-701-2345678",
                "email": "chidi@atmdispatch.com",
                "location": {"lat": 6.5244, "lng": 3.3792, "address": "Ikoyi"},
                "skill_level": "senior",
                "available": True,
                "certification": "Diebold, NCR"
            },
            {
                "engineer_id": "ENG-002",
                "name": "Amara Ngozi",
                "phone": "+234-702-2345678",
                "email": "amara@atmdispatch.com",
                "location": {"lat": 6.5300, "lng": 3.3850, "address": "VI"},
                "skill_level": "junior",
                "available": True,
                "certification": "NCR"
            },
            {
                "engineer_id": "ENG-003",
                "name": "Tunde Adeyemi",
                "phone": "+234-703-2345678",
                "email": "tunde@atmdispatch.com",
                "location": {"lat": 6.5200, "lng": 3.3700, "address": "Lekki"},
                "skill_level": "specialist",
                "available": True,
                "certification": "Diebold, NCR, Wincor"
            }
        ]
        
        print("\n👨‍🔧 CREATING ENGINEER ASSETS")
        print("=" * 60)
        for eng in engineers:
            try:
                response = self.session.post(f"{BASE_URL}/api/v1/assets/engineers", json=eng)
                if response.status_code == 201:
                    print(f"✅ Engineer Created: {eng['name']} ({eng['engineer_id']}) - {eng['skill_level']}")
                else:
                    print(f"❌ Failed to create engineer: {response.text}")
            except Exception as e:
                print(f"❌ Error: {str(e)}")

class ATMLogGenerator:
    """Generate realistic ATM logs with random faults"""
    
    def __init__(self):
        self.session = requests.Session()
        self.atm_ids = ["ATM-045", "ATM-046", "ATM-047"]
    
    def generate_healthy_log(self, atm_id: str) -> Dict:
        """Generate a healthy ATM log"""
        return {
            "atm_id": atm_id,
            "status": "active",
            "error_code": None,
            "error_description": None,
            "cash_status": "normal",
            "card_reader_status": "operational",
            "dispenser_status": "operational",
            "network_status": "online",
            "uptime_percentage": random.uniform(99, 100),
            "temperature": random.uniform(25, 35),
            "transaction_count": random.randint(50, 200),
            "failed_transactions": random.randint(0, 2),
            "last_transaction_time": datetime.now().isoformat()
        }
    
    def generate_card_reader_fault(self, atm_id: str) -> Dict:
        """Generate card reader fault log"""
        log = self.generate_healthy_log(atm_id)
        log.update({
            "status": "error",
            "error_code": "ERR_CARD_JAM",
            "error_description": "Card reader jam detected - multiple failures",
            "card_reader_status": "faulty",
            "uptime_percentage": random.uniform(45, 70),
            "failed_transactions": random.randint(8, 15)
        })
        return log
    
    def generate_dispenser_fault(self, atm_id: str) -> Dict:
        """Generate dispenser fault log"""
        log = self.generate_healthy_log(atm_id)
        log.update({
            "status": "error",
            "error_code": "ERR_DISPENSER",
            "error_description": "Cash dispenser mechanism failure",
            "dispenser_status": "faulty",
            "uptime_percentage": random.uniform(40, 65),
            "failed_transactions": random.randint(10, 20)
        })
        return log
    
    def generate_network_fault(self, atm_id: str) -> Dict:
        """Generate network fault log"""
        log = self.generate_healthy_log(atm_id)
        log.update({
            "status": "error",
            "error_code": "ERR_NET_TIMEOUT",
            "error_description": "Network connection lost",
            "network_status": "offline",
            "uptime_percentage": random.uniform(10, 40),
            "failed_transactions": random.randint(50, 100)
        })
        return log
    
    def generate_cash_low_alert(self, atm_id: str) -> Dict:
        """Generate cash low alert log"""
        log = self.generate_healthy_log(atm_id)
        log.update({
            "status": "warning",
            "error_code": "WARN_CASH_LOW",
            "error_description": "Cash level critically low",
            "cash_status": "out",
            "uptime_percentage": random.uniform(98, 100),
            "failed_transactions": random.randint(2, 5)
        })
        return log
    
    def generate_temperature_warning(self, atm_id: str) -> Dict:
        """Generate temperature warning log"""
        log = self.generate_healthy_log(atm_id)
        log.update({
            "status": "warning",
            "error_code": "WARN_TEMP_HIGH",
            "error_description": "Internal temperature exceeding threshold",
            "temperature": random.uniform(45, 55),
            "uptime_percentage": random.uniform(90, 98),
            "failed_transactions": random.randint(3, 8)
        })
        return log
    
    def generate_random_log(self, atm_id: str) -> Dict:
        """Generate a random log with fault probability"""
        fault_type = random.choices(
            ["healthy", "card_reader", "dispenser", "network", "cash_low", "temperature"],
            weights=[60, 10, 10, 10, 5, 5]
        )[0]
        
        generators = {
            "healthy": self.generate_healthy_log,
            "card_reader": self.generate_card_reader_fault,
            "dispenser": self.generate_dispenser_fault,
            "network": self.generate_network_fault,
            "cash_low": self.generate_cash_low_alert,
            "temperature": self.generate_temperature_warning
        }
        
        return generators[fault_type](atm_id)
    
    def ingest_log(self, log: Dict) -> bool:
        """Send log to backend for ingestion"""
        try:
            response = self.session.post(f"{BASE_URL}/api/v1/logs/atm", json=log)
            if response.status_code == 201:
                status_icon = "✅" if log["status"] == "active" else "⚠️"
                error_code = log.get('error_code', 'HEALTHY')
                error_desc = log.get('error_description', 'OK')
                print(f"{status_icon} [{log['atm_id']}] {error_code} - {error_desc}")
                return True
            else:
                print(f"❌ Failed to ingest log: {response.text}")
                return False
        except Exception as e:
            print(f"❌ Error ingesting log: {str(e)}")
            return False
    
    def run_continuous_simulation(self, duration_seconds: int = 60, interval_seconds: int = 5):
        """Run continuous log generation and ingestion"""
        print("\n🚀 STARTING CONTINUOUS ATM LOG SIMULATION")
        print("=" * 60)
        print(f"Duration: {duration_seconds}s | Interval: {interval_seconds}s")
        print("=" * 60)
        
        start_time = time.time()
        log_count = 0
        
        while time.time() - start_time < duration_seconds:
            print(f"\n⏱️  [{datetime.now().strftime('%H:%M:%S')}] Generating logs...")
            
            # Generate log for each ATM
            for atm_id in self.atm_ids:
                log = self.generate_random_log(atm_id)
                self.ingest_log(log)
                log_count += 1
            
            elapsed = int(time.time() - start_time)
            remaining = duration_seconds - elapsed
            print(f"📊 Total logs ingested: {log_count} | Remaining: {remaining}s")
            
            time.sleep(interval_seconds)
        
        print("\n✨ SIMULATION COMPLETED")
        print("=" * 60)
        print(f"Total logs ingested: {log_count}")

class DispatchMonitor:
    """Monitor dispatch tickets and alert creation"""
    
    def __init__(self):
        self.session = requests.Session()
    
    def monitor_tickets(self, interval: int = 10, duration: int = 60):
        """Monitor active tickets"""
        print("\n📡 STARTING DISPATCH MONITOR")
        print("=" * 60)
        
        start_time = time.time()
        
        while time.time() - start_time < duration:
            try:
                response = self.session.get(f"{BASE_URL}/api/v1/dispatch/tickets?status=pending")
                if response.status_code == 200:
                    tickets = response.json()["tickets"]
                    print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Active pending tickets: {len(tickets)}")
                    
                    for ticket in tickets[:3]:  # Show first 3
                        print(f"  🎟️  ID: {ticket['ticket_id'][:8]}... | ATM: {ticket['atm_id']} | Fault: {ticket['fault_type']} | Severity: {ticket['severity']}")
                else:
                    print(f"❌ Failed to fetch tickets: {response.text}")
            except Exception as e:
                print(f"❌ Error monitoring tickets: {str(e)}")
            
            time.sleep(interval)

class DashboardReporter:
    """Generate dashboard reports"""
    
    def __init__(self):
        self.session = requests.Session()
    
    def generate_report(self):
        """Generate full system report"""
        print("\n📊 SYSTEM DASHBOARD REPORT")
        print("=" * 60)
        
        try:
            # Get overview
            response = self.session.get(f"{BASE_URL}/api/v1/dashboard/overview")
            if response.status_code == 200:
                data = response.json()
                print(f"Total ATMs: {data['total_atms']}")
                print(f"Total Engineers: {data['total_engineers']}")
                print(f"Active Incidents: {data['active_incidents']}")
                print(f"Resolved Today: {data['resolved_today']}")
            
            # Get pending tickets
            response = self.session.get(f"{BASE_URL}/api/v1/dispatch/tickets?status=pending")
            if response.status_code == 200:
                pending = response.json()["tickets"]
                print(f"\n🎟️  PENDING TICKETS: {len(pending)}")
                for t in pending[:5]:
                    print(f"   - {t['atm_id']} | {t['fault_type']} | Assigned: {t.get('engineer_id', 'N/A')}")
            
            # Get assigned tickets
            response = self.session.get(f"{BASE_URL}/api/v1/dispatch/tickets?status=assigned")
            if response.status_code == 200:
                assigned = response.json()["tickets"]
                print(f"\n✅ ASSIGNED TICKETS: {len(assigned)}")
                for t in assigned[:5]:
                    print(f"   - {t['atm_id']} | Assigned to: {t.get('engineer_id', 'N/A')}")
            
            print("=" * 60)
        except Exception as e:
            print(f"❌ Error generating report: {str(e)}")

# ============= MAIN EXECUTION =============

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("🏦 ATM SMART DISPATCH - COMPLETE SIMULATION")
    print("=" * 60)
    
    # Step 1: Create Assets
    print("\n[STEP 1/4] Setting up assets...")
    asset_manager = ATMAssetManager()
    asset_manager.create_atm_assets()
    time.sleep(2)
    asset_manager.create_engineer_assets()
    time.sleep(2)
    
    # Step 2: Generate and ingest logs
    print("\n[STEP 2/4] Generating and ingesting logs...")
    generator = ATMLogGenerator()
    generator.run_continuous_simulation(duration_seconds=30, interval_seconds=5)
    time.sleep(2)
    
    # Step 3: Monitor tickets
    print("\n[STEP 3/4] Monitoring dispatch tickets...")
    monitor = DispatchMonitor()
    monitor.monitor_tickets(interval=5, duration=20)
    time.sleep(2)
    
    # Step 4: Generate final report
    print("\n[STEP 4/4] Generating final report...")
    reporter = DashboardReporter()
    reporter.generate_report()
    
    print("\n" + "=" * 60)
    print("✨ SIMULATION COMPLETE!")
    print("=" * 60)
    print("\nVisit http://localhost:8000/docs for API documentation")
    print("=" * 60)
# Elasticsearch index prefixes and names
TELEMETRY_INDEX_PREFIX = "atm-telemetry"
ALERTS_INDEX_NAME = "alerts"
TELEMETRY_INDEX_TEMPLATE_NAME = "atm-telemetry-template"

# Alerting rule definitions
ALERT_RULES = {
    "PRINTER_JAM": {"rule": "Printer Jam", "severity": "high"},
    "ATM_LOCKED": {"rule": "ATM Locked", "severity": "critical"},
    "OUT_OF_NETWORK": {"rule": "Out of Network", "severity": "medium"},
}

# Elasticsearch index template for ATM telemetry data
TELEMETRY_INDEX_TEMPLATE = {
    "index_patterns": [f"{TELEMETry_INDEX_PREFIX}-*"],
    "template": {
        "settings": {
            "number_of_shards": 1,
            "number_of_replicas": 1
        },
        "mappings": {
            "properties": {
                "atm_id": {"type": "keyword"},
                "timestamp": {"type": "date"},
                "error_code": {"type": "keyword"},
                "error_message": {"type": "text"},
                "status": {"type": "keyword"},
                "cash_level": {"type": "integer"},
                "uptime": {"type": "float"},
                "location": {"type": "geo_point"}
            }
        }
    }
}

from prometheus_client import start_http_server, Gauge
import time
import requests
import urllib3

# Disable SSL warnings for self-signed certs
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Define Prometheus metrics
metrics = {
    'ups_remaining_capacity_percent': Gauge('ups_remaining_capacity_percent', 'Remaining battery capacity in percent', ['ups_id']),
    'ups_battery_voltage': Gauge('ups_battery_voltage', 'Battery voltage', ['ups_id']),
    'ups_percent_load': Gauge('ups_percent_load', 'Percent load on UPS', ['ups_id']),
    'ups_run_time_to_empty_seconds': Gauge('ups_run_time_to_empty_seconds', 'Run time to empty in seconds', ['ups_id']),
    'ups_input_voltage': Gauge('ups_input_voltage', 'Input voltage', ['ups_id']),
    'ups_output_voltage': Gauge('ups_output_voltage', 'Output voltage', ['ups_id']),
    'ups_is_ac_present': Gauge('ups_is_ac_present', 'Is AC present (1=yes, 0=no)', ['ups_id']),
    'ups_is_charging': Gauge('ups_is_charging', 'Is battery charging (1=yes, 0=no)', ['ups_id']),
    'ups_is_discharging': Gauge('ups_is_discharging', 'Is battery discharging (1=yes, 0=no)', ['ups_id']),
    'ups_is_overload': Gauge('ups_is_overload', 'Is UPS overloaded (1=yes, 0=no)', ['ups_id']),
    'ups_is_ups_on': Gauge('ups_is_ups_on', 'Is UPS on (1=yes, 0=no)', ['ups_id']),
    'ups_needs_replacement': Gauge('ups_needs_replacement', 'Does battery need replacement (1=yes, 0=no)', ['ups_id']),
}

def fetch_and_update_metrics():
    try:
        response = requests.get("https://bobvs.gateway.msft:8210/api/PowerAssist", verify=False)
        ups_data = response.json()

        for ups in ups_data:
            ups_id = ups['upsUniqueIdentifier']
            status = ups['status']

            metrics['ups_remaining_capacity_percent'].labels(ups_id=ups_id).set(status['remainingCapacityInPercent'])
            metrics['ups_battery_voltage'].labels(ups_id=ups_id).set(status['batteryVoltage'])
            metrics['ups_percent_load'].labels(ups_id=ups_id).set(status['percentLoad'])
            metrics['ups_run_time_to_empty_seconds'].labels(ups_id=ups_id).set(status['runTimeToEmptyInSeconds'])
            metrics['ups_input_voltage'].labels(ups_id=ups_id).set(status['inputVoltages']['voltages'][0])
            metrics['ups_output_voltage'].labels(ups_id=ups_id).set(status['outputVoltages']['voltages'][0])
            metrics['ups_is_ac_present'].labels(ups_id=ups_id).set(int(status['isAcPresent']))
            metrics['ups_is_charging'].labels(ups_id=ups_id).set(int(status['isCharging']))
            metrics['ups_is_discharging'].labels(ups_id=ups_id).set(int(status['isDischarging']))
            metrics['ups_is_overload'].labels(ups_id=ups_id).set(int(status['isOverload']))
            metrics['ups_is_ups_on'].labels(ups_id=ups_id).set(int(status['isUpsOn']))
            metrics['ups_needs_replacement'].labels(ups_id=ups_id).set(int(status['needsReplacement']))

    except Exception as e:
        print(f"Error fetching UPS metrics: {e}")

if __name__ == "__main__":
    start_http_server(8000)  # Start Prometheus metrics server
    while True:
        fetch_and_update_metrics()
        time.sleep(30)  # Poll every 30 seconds

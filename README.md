On the Windows server install the Vertiv Power Assist:

https://www.vertiv.com/en-us/support/software-download/software/vertiv-power-assist-software-download/


Once installed verify the metrics are displayed:

https://[server]:8210/api/PowerAssist


Either create a new certificate for Power Assist or trust it on the Grafana/Prometheus server or by pass SSL.

Pull the ups_exporter.py

Make executable:

chmod +x ups_exporter.py


Edit and change the line to match your server running Power Assist:

  response = requests.get("https://<server_name>:8210/api/PowerAssist", verify=False)



Create a VENV for python3

  python3 -m venv vertiv
  source vertiv/bin/activate
  python3 pip3 install requests prometheus_client
  python3 ./ups_exporter.py

Make sure the script ran

http://[prometheus_server]:8000


Make the script a service:

1. Create a systemd Service File
  Git the service file and copy to /etc/systemd/system/ups_exporter.service
2. Reload systemd and Enable the Service
  sudo systemctl daemon-reexec
  sudo systemctl daemon-reload
  sudo systemctl enable ups_exporter.service
3. Start the Service
  sudo systemctl start ups_exporter.service
4. Check Status and Logs
  sudo systemctl status ups_exporter.service
  journalctl -u ups_exporter.service -f


Create the Prometheus scrape:

  - job_name: 'ups_metrics'
    scrape_interval: 1m  # Scrape every minute
    metrics_path: '/metrics'  # Specify the metrics endpoint path
    static_configs:
      - targets:
          - '[prometheus_server]:8000'  # Corrected: removed /metrics from target


Verify that Prometheus is scraping correctly:

  http://[prometheus_server]:9090/targets


  <img width="1892" height="182" alt="image" src="https://github.com/user-attachments/assets/44e9f67e-a357-46c5-b3a2-979a49419d19" />

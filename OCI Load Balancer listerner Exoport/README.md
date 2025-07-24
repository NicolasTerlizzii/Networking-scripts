# OCI Load Balancer Listener Exporter

This Python script retrieves SSL listener and certificate information from Oracle Cloud Infrastructure (OCI) Load Balancers and exports the results to a CSV file.

## Features

- Reads OCI configuration from the default `~/.oci/config` or a custom path.
- Finds Load Balancer OCIDs by their display names within a given compartment.
- Retrieves details for each listener, including:
  - Protocol
  - Port
  - Certificate name
  - One or more certificate OCIDs
- Exports the data into a `;`-delimited CSV file for easy analysis.

## Prerequisites

- **Python 3.6+**
- **OCI Python SDK**: Install via pip:
  ```bash
  pip install oci
  ```
- OCI configuration file (`~/.oci/config`) with at least one profile configured.

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/<your-username>/oci-lb-listener-exporter.git
   cd oci-lb-listener-exporter
   ```
2. (Optional) Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate   # Windows
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

By default the script uses the OCI config file at `~/.oci/config` and the profile `DEFAULT`. To use a different profile or location, set the `OCI_CONFIG_FILE` and `OCI_PROFILE` environment variables, for example:

```bash
export OCI_CONFIG_FILE=/path/to/your/config
export OCI_PROFILE=DEV
```

Alternatively, you can modify the script call to pass a `config_path` argument to `get_config()`.

## Usage

1. Open `export_lb_certificates.py` and set the following placeholders:
   - `compartment_id`: OCID of your OCI compartment.
   - `lb_names`: List of Load Balancer display names to export.
2. Run the script:
   ```bash
   python export_lb_certificates.py
   ```
3. The output CSV file `load_balancer_listeners.csv` will be created in the current directory.

### Example

```bash
export COMPARTMENT_OCID=ocid1.compartment.oc1..example
python export_lb_certificates.py
```

Sample output (CSV):

| lb_name              | lb_ocid                                        | listener_name        | protocol | port | certificate_name | certificate_ids                                    |
|----------------------|------------------------------------------------|----------------------|----------|------|------------------|----------------------------------------------------|
| my-load-balancer-1   | ocid1.loadbalancer.oc1...                      | listener-https       | HTTPS    | 443  | prod-cert        | ocid1.certificate.oc1...                           |
| my-load-balancer-1   | ocid1.loadbalancer.oc1...                      | listener-http        | HTTP     | 80   |                  |                                                    |

## Contributing

Contributions welcome! Please open issues or submit pull requests with enhancements or bug fixes.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.


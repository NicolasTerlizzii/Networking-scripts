# OCI Subnet Bulk Creator

A Python script to perform **bulk creation of subnets** in Oracle Cloud Infrastructure (OCI) using definitions from a CSV file. Ideal for automating large-scale network deployments across multiple tenancies, regions, compartments, and VCNs.

---

## 🚀 Features

- **Massive subnet creation** from CSV definitions
- Supports **per-row overrides** for tenancy, region, compartment, and VCN
- **Automatic delimiter detection** (comma `,` or semicolon `;`)
- **Formatted console output** for easy verification
- **Configurable** via constants or CLI arguments

---

## 📦 Repository Structure

```
├── oci_subnet_creator.py   # Main Python script
├── subnet.csv              # Example CSV template for subnet definitions
└── README.md               # This documentation
```

---

## 📝 Prerequisites

- Python 3.7+
- `oci` Python SDK
- OCI CLI config file with valid credentials and profile

Install SDK:

```bash
pip install oci
```

---

## ⚙️ Configuration

At the top of `oci_subnet_creator.py`, adjust these constants if needed:

```python
# Default path to your CSV (if no --csv passed)
DEFAULT_CSV_PATH = r"/path/to/your/subnet.csv"

# OCI config file and profile
OCI_CONFIG_PATH = r"~/.oci/config"
OCI_PROFILE     = "DEFAULT"
```

Alternatively, you can override via CLI arguments.

---

## 📋 CSV Format

Your CSV must include a header row with **at least** the following columns:

| Column               | Description                                                 | Required | Example                    |
| -------------------- | ----------------------------------------------------------- | -------- | -------------------------- |
| subnet\_name         | Display name of the subnet                                  | Yes      | `web-subnet-1`             |
| cidr\_block          | CIDR block (e.g., `10.0.1.0/24`)                            | Yes      | `10.0.1.0/24`              |
| compartment\_id      | OCID of the compartment where subnet will be created        | Yes      | `ocid1.compartment.oc1...` |
| vcn\_id              | OCID of the VCN where subnet belongs                        | Yes      | `ocid1.vcn.oc1...`         |
| tenancy\_id          | OCID of the tenancy                                         | Yes      | `ocid1.tenancy.oc1...`     |
| region               | OCI region identifier (e.g., `eu-milan-1`)                  | Yes      | `eu-milan-1`               |
| availability\_domain | (Optional) Availability Domain, e.g., `AD-1`                | No       | `AD-1`                     |
| dns\_label           | (Optional) DNS label (lowercase alphanumeric, max 15 chars) | No       | `websubnet1`               |

Example (semicolon-delimited):

```csv
subnet_name;cidr_block;compartment_id;vcn_id;tenancy_id;region;availability_domain;dns_label
web-subnet-1;10.0.1.0/24;ocid1.comp.oc1..aaa;ocid1.vcn.oc1..bbb;ocid1.tenancy.oc1..ccc;eu-milan-1;AD-1;websubnet1
```

---

## 🚀 Usage

### Run with defaults:

```bash
python oci_subnet_creator.py
```

### Override CSV path or OCI config/profile:

```bash
python oci_subnet_creator.py \
  --csv "/my/path/subnet.csv" \
  --config "/home/user/.oci/config" \
  --profile "MYPROFILE" \
  --tenancy-id "ocid1.tenancy.oc1..." \
  --region "eu-frankfurt-1" \
  --compartment-id "ocid1.compartment.oc1..." \
  --vcn-id "ocid1.vcn.oc1..."
```

---

## 🎯 Output

For each subnet created, the script prints:

```
subnet name: <display_name>
" +
"cidr: <cidr_block>
" +
"dns label: <dns_label>
" +
"tenancy: <tenancy_ocid>
----------------------------------------
```

---

## 🤝 Contributing

1. Fork the repo
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m "Add awesome feature"`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License. See the `LICENSE` file for details.


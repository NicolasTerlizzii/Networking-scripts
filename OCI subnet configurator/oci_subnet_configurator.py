#!/usr/bin/env python3
"""
oci_subnet_creator.py: Bulk create subnets in Oracle Cloud Infrastructure (OCI) across multiple tenancies, regions, compartments and VCNs.

This script reads subnet definitions from a CSV file (comma or semicolon delimited) and creates them according to per-row or default CLI arguments.
It supports overriding the OCI config file path, profile, global tenancy OCID, region, compartment OCID, and VCN OCID via command-line or per-row CSV values.

CSV format (header row required, comma `,` or semicolon `;` delimiter):
  subnet_name,cidr_block,availability_domain,dns_label,compartment_id[,tenancy_id][,region][,vcn_id]
  OR
  subnet_name;cidr_block;availability_domain;dns_label;compartment_id[;tenancy_id][;region][;vcn_id]

Usage:
  python oci_subnet_creator.py [--csv] [--config] [--profile] [--tenancy-id] [--region] [--compartment-id] [--vcn-id]

If --csv is omitted, the DEFAULT_CSV_PATH constant below will be used.
"""
import os
import oci
import csv
import argparse
import sys

# Default path to CSV if not provided via --csv
DEFAULT_CSV_PATH = r"C:\Users\terlizzi\Documents\Doc Nicolas Generale\Script\Python\file\subnet.csv"

def get_config(config_file: str, profile: str) -> dict:
    # Expand ~ and env vars
    config_file = os.path.expanduser(config_file)
    config_file = os.path.expandvars(config_file)
    try:
        return oci.config.from_file(config_file, profile)
    except Exception as e:
        print(f"Error loading OCI config: {e}", file=sys.stderr)
        sys.exit(1)

def get_network_client(config: dict) -> oci.core.VirtualNetworkClient:
    return oci.core.VirtualNetworkClient(config)

def create_subnet(
    network_client: oci.core.VirtualNetworkClient,
    compartment_id: str,
    vcn_id: str,
    display_name: str,
    cidr_block: str,
    availability_domain: str = None,
    dns_label: str = None
) -> oci.core.models.Subnet:
    details = oci.core.models.CreateSubnetDetails(
        compartment_id=compartment_id,
        vcn_id=vcn_id,
        display_name=display_name,
        cidr_block=cidr_block,
        availability_domain=availability_domain,
        dns_label=dns_label
    )
    return network_client.create_subnet(create_subnet_details=details).data

def main():
    parser = argparse.ArgumentParser(description="Bulk create subnets in OCI from CSV file.")
    parser.add_argument(
        "--csv",
        default=DEFAULT_CSV_PATH,
        help="Path to CSV file containing subnet definitions (comma or semicolon separated)"
    )
    parser.add_argument(
        "--config",
        default=r"C:\Users\terlizzi\Documents\Doc Nicolas Generale\Script\Python\Oracle\config",
        help="Path to OCI CLI config file"
    )
    parser.add_argument("--profile", default="DEFAULT", help="Profile name in OCI config to use")
    parser.add_argument("--tenancy-id", help="Default OCID of the tenancy; can be overridden per CSV row")
    parser.add_argument("--region", help="Default OCI region code; can be overridden per CSV row")
    parser.add_argument("--compartment-id", help="Default OCID of the compartment; can be overridden per CSV row")
    parser.add_argument("--vcn-id", help="Default OCID of the VCN; can be overridden per CSV row")
    args = parser.parse_args()

    base_config = get_config(args.config, args.profile)
    if args.tenancy_id:
        base_config["tenancy"] = args.tenancy_id
    if args.region:
        base_config["region"] = args.region

    csv_path = args.csv
    if not os.path.isfile(csv_path):
        print(f"CSV file not found: {csv_path}", file=sys.stderr)
        sys.exit(1)

    # Detect delimiter (comma or semicolon)
    with open(csv_path, newline="", encoding="utf-8-sig") as f:
        sample = f.read(2048)
        f.seek(0)
        try:
            dialect = csv.Sniffer().sniff(sample, delimiters=",;")
        except csv.Error:
            dialect = csv.get_dialect("excel")
        reader = csv.DictReader(f, dialect=dialect)

        for row in reader:
            # strip whitespace/keys
            row = {k.strip(): v.strip() for k, v in row.items() if k}

            tenancy     = row.get("tenancy_id")     or base_config.get("tenancy")
            region      = row.get("region")         or base_config.get("region")
            compartment = row.get("compartment_id") or args.compartment_id
            vcn         = row.get("vcn_id")         or args.vcn_id

            if not all([tenancy, region, compartment, vcn]):
                print(f"Skipping row: missing tenancy/region/compartment/vcn. Row={row}", file=sys.stderr)
                continue

            config = base_config.copy()
            config["tenancy"] = tenancy
            config["region"]  = region
            network_client = get_network_client(config)

            name = row.get("subnet_name")
            cidr = row.get("cidr_block")
            dns  = row.get("dns_label") or ""

            try:
                subnet = create_subnet(
                    network_client,
                    compartment,
                    vcn,
                    name,
                    cidr,
                    availability_domain=row.get("availability_domain") or None,
                    dns_label=dns
                )
                # Formatted output
                print(f"subnet name: {subnet.display_name}")
                print(f"cidr: {cidr}")
                print(f"dns label: {dns}")
                print(f"tenancy: {tenancy}")
                print("----------------------------------------")
            except Exception as e:
                print(f"Error creating subnet {name}: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()

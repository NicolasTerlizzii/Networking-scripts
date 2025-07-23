import oci
import sys
import csv

def get_config(config_path, profile="DEFAULT"):
    try:
        return oci.config.from_file(config_path, profile)
    except Exception as e:
        print(f"Errore caricamento config: {e}", file=sys.stderr)
        sys.exit(1)

def get_load_balancer_ocid(lb_client, compartment_id, lb_name):
    lbs = lb_client.list_load_balancers(compartment_id=compartment_id).data
    matches = [lb for lb in lbs if lb.display_name == lb_name]
    if not matches:
        return None
    if len(matches) > 1:
        raise ValueError(f"Trovati più LB con nome '{lb_name}': {[lb.id for lb in matches]}")
    return matches[0].id

def gather_listeners(lb_client, lb_id):
    """
    Restituisce una lista di tuple:
      (listener_name, protocol, port, certificate_name, [certificate_ids])
    """
    lb = lb_client.get_load_balancer(load_balancer_id=lb_id).data

    out = []
    for name, listener in lb.listeners.items():
        prot, port = listener.protocol, listener.port
        ssl = listener.ssl_configuration
        if not ssl:
            out.append((name, prot, port, "", []))
            continue

        cert_name = ssl.certificate_name or ""
        # legacy single-id oppure multi-id
        single = getattr(ssl, "certificate_id", None)
        multi  = getattr(ssl, "certificate_ids", None)
        ids = []
        if single:
            ids = [single]
        elif multi:
            ids = multi

        out.append((name, prot, port, cert_name, ids))
    return out

if __name__ == "__main__":
    # 1) Configurazione
    config_path    = r"C:\Users\terlizzi\Documents\Doc Nicolas Generale\Script\Python\Oracle\config"
    profile        = "DEFAULT"
    compartment_id = "ocid1.tenancy.oc1..aaaaaaaaoxggsuebkmqgqdlwkvdorabzxeolnb3ivtkemcjjvmkjeql5rxfa"

    # 2) Lista di load balancer da processare, ad es.
    lb_names = [
        "lb_2025-0723-1535",
        # , "altro-lb", ...
    ]

    # 3) Inizializza client
    config    = get_config(config_path, profile)
    lb_client = oci.load_balancer.LoadBalancerClient(config)

    # 4) Prepara CSV
    output_file = "load_balancer_ocid.csv"
    with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile, delimiter=";")
        # Header
        writer.writerow([
            "lb_name",
            "lb_ocid",
            "listener_name",
            "protocol",
            "port",
            "certificate_name",
            "certificate_ids"
        ])

        # 5) Per ciascun LB
        for lb_name in lb_names:
            ocid = get_load_balancer_ocid(lb_client, compartment_id, lb_name)
            if not ocid:
                print(f"[WARN] Nessun LB trovato con nome '{lb_name}'", file=sys.stderr)
                continue

            # 6) Estrai info listener/certificati
            rows = gather_listeners(lb_client, ocid)
            if not rows:
                # LB senza listener
                writer.writerow([lb_name, ocid, "", "", "", "", ""])
                continue

            for listener_name, prot, port, cert_name, cert_ids in rows:
                writer.writerow([
                    lb_name,
                    ocid,
                    listener_name,
                    prot,
                    port,
                    cert_name,
                    ",".join(cert_ids)  # unisco gli OCID con virgola
                ])

    print(f"✅ Output scritto in {output_file}")

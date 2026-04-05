from datetime import datetime

import dlt
import requests


def fetch_all_customers_from_flask():
    base_url = "http://mock-server:5000/api/customers"
    all_data = []
    page = 1
    limit = 10

    while True:
        try:
            response = requests.get(f"{base_url}?page={page}&limit={limit}")
            response.raise_for_status()
            res_json = response.json()

            data = res_json.get("data", [])
            if not data:
                break

            for item in data:
                if item.get("date_of_birth"):
                    item["date_of_birth"] = datetime.strptime(item["date_of_birth"], "%Y-%m-%d").date()
                if item.get("created_at"):
                    item["created_at"] = datetime.fromisoformat(item["created_at"].replace("Z", "+00:00"))
            all_data.extend(data)

            if len(all_data) >= res_json.get("total", 0):
                break

            page += 1
        except Exception as e:
            print(f"Error fetching data from Flask: {e}")
            break

    return all_data


def run_ingestion():

    customers_data = fetch_all_customers_from_flask()

    if not customers_data:
        return 0

    pipeline = dlt.pipeline(
        pipeline_name="flask_to_postgres",
        destination="postgres",
        dataset_name="public"
    )

    load_info = pipeline.run(
        customers_data,
        table_name="customers",
        write_disposition="merge",
        primary_key="customer_id"
    )

    print(load_info)
    return len(customers_data)
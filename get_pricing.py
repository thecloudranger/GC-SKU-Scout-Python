# Copyright 2023 Nils Knieling. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse
import json
import os
import time
from datetime import datetime

from google.cloud import billing_v1
from google.api_core import client_options


def main():
    parser = argparse.ArgumentParser(description="Fetch Google Cloud SKU pricing.")
    parser.add_argument(
        "--region",
        type=str,
        default="me-central2",
        help="Google Cloud region",
    )
    args = parser.parse_args()

    api_key = os.environ.get("API_KEY")
    if not api_key:
        raise ValueError("API_KEY environment variable not set.")

    print(f"Fetching pricing for region: {args.region}")

    opts = client_options.ClientOptions(api_key=api_key)
    client = billing_v1.CloudCatalogClient(client_options=opts)

    service_ids = [
        "6F81-5844-456A",  # Compute Engine
        "E505-1604-58F8",  # Networking
        "95FF-2EF5-5EA1",  # Cloud Storage
        "58CD-E7C3-72CA",  # Cloud Monitoring
        "9662-B51E-5089",  # Cloud SQL
		"CCD8-9BF1-090E",  # Kubernetes Engine
		"5490-F7B7-8DF6",  # Cloud Logging        
    ]

    all_skus = []

    for service_id in service_ids:
        print(f"Fetching SKUs for service: {service_id}")
        request = billing_v1.ListSkusRequest(parent=f"services/{service_id}")
        for sku in client.list_skus(request=request):
            is_region_found = False
            for r in sku.service_regions:
                if r == args.region or r == "global" or r == "multi-region":
                    is_region_found = True
                    break

            if is_region_found:
                nanos = 0
                units = 0
                currency_code = ""
                calculated_price = 0.0
                price_per_unit = ""
                usage_unit_description = ""

                if sku.pricing_info and sku.pricing_info[0].pricing_expression.tiered_rates:
                    tiered_rate = sku.pricing_info[0].pricing_expression.tiered_rates[0]
                    nanos = tiered_rate.unit_price.nanos
                    units = tiered_rate.unit_price.units
                    currency_code = tiered_rate.unit_price.currency_code
                    calculated_price = float(units) + float(nanos) / 1e9
                    usage_unit_description = sku.pricing_info[0].pricing_expression.usage_unit_description
                    price_per_unit = f"{calculated_price:.10f} {currency_code} per {usage_unit_description}"

                all_skus.append(
                    {
                        "Name": sku.name,
                        "SkuId": sku.sku_id,
                        "Description": sku.description,
                        "ServiceDisplayName": sku.category.service_display_name,
                        "ResourceFamily": sku.category.resource_family,
                        "ResourceGroup": sku.category.resource_group,
                        "UsageType": sku.category.usage_type,
                        "ServiceRegions": list(sku.service_regions),
                        "ServiceProviderName": sku.service_provider_name,
                        "Nanos": nanos,
                        "Units": units,
                        "CurrencyCode": currency_code,
                        "CalculatedPrice": calculated_price,
                        "PricePerUnit": price_per_unit,
                        "UsageUnitDescription": usage_unit_description,
                    }
                )
        time.sleep(1)  # To avoid hitting API rate limits

    # Create filename with date and time
    filename = f"pricing-{args.region}-{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.json"

    # Write to file
    with open(filename, "w") as f:
        json.dump(all_skus, f, indent=2)

    print(f"\nPricing information saved to {filename}")
    print(f"\nFound {len(all_skus)} SKUs for region {args.region}")


if __name__ == "__main__":
    main()

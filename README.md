# SKU-Scout (Python Version)

This program fetches SKU pricing information from the Google Cloud Billing API for a specific region and saves it to a JSON file.

## Prerequisites

*   [Python 3](https://www.python.org/downloads/) installed on your system.
*   A Google Cloud Platform project with the [Cloud Billing API](https://console.cloud.google.com/flows/enableapi?apiid=cloudbilling.googleapis.com) enabled.
*   An API key with access to the Cloud Billing API.

## Setup

1.  **Clone the repository:**
    ```bash
    git clone <your-repo-url>
    cd <your-repo-name>/build
    ```

2.  **Install dependencies:**
    This script requires the `google-api-python-client` and `pyyaml` libraries. You can install them using pip:
    ```bash
    pip install google-api-python-client pyyaml
    ```

3.  **Set your API Key:**
    Export your API key as an environment variable.
    ```bash
    export API_KEY="YOUR-CLOUD-BILLING-API-KEY"
    ```

## Running the Program

You can run the program from the command line. Use the `--region` flag to specify the Google Cloud region you want to fetch pricing for.

```bash
python3 get_pricing.py --region=me-central2
```

The script will create a JSON file in the `build` directory named `pricing-<region>-<timestamp>.json` with the SKU information.

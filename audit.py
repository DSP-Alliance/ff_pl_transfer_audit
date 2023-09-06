import requests
import csv

def fetch_table_data(filecoin_address, page, page_size):
    url = f"https://filfox.info/api/v1/address/{filecoin_address}/transfers"
    params = {"pageSize": page_size, "page": page}

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json(), response.url
    except requests.exceptions.RequestException as e:
        print("An error occurred:", e)
        return None, None

def extract_data_from_api_response(api_response):
    if not api_response or "transfers" not in api_response:
        print("No data found.")
        return [], []

    transfers = api_response["transfers"]
    rows = []

    for transfer in transfers:
        row = [
            transfer.get("message", "N/A"),
            transfer.get("height", "N/A"),
            transfer.get("timestamp", "N/A"),
            transfer.get("from", "N/A"),
            transfer.get("to", "N/A"),
            format_value(transfer.get("value", 0)),
            transfer.get("type", "N/A")
        ]
        rows.append(row)

    return rows

def format_value(value):
    return "{:.18f}".format(float(value) / 1e18)

def save_to_csv(all_data):
    if not all_data:
        print("No data to save.")
        return

    file_name = "filecoin_data.csv"

    with open(file_name, mode="w", newline="") as file:
        writer = csv.writer(file)
        headers = ["Address", "Message ID", "Height", "Time", "From", "To", "Value", "Type"]
        writer.writerow(headers)
        writer.writerows(all_data)

    print(f"Data successfully saved to {file_name}")

def fetch_all_transfers(filecoin_addresses):
    page_size = 100
    all_data = []

    for filecoin_address in filecoin_addresses:
        total_count_response, _ = fetch_table_data(filecoin_address, 0, 1)
        if not total_count_response:
            print(f"Failed to get the total count for address {filecoin_address}.")
            continue

        total_count = total_count_response.get("totalCount", 0)
        if total_count == 0:
            print(f"No data found for address {filecoin_address}.")
            continue

        total_pages = (total_count + page_size - 1) // page_size
        print(f"Total transfers to fetch for {filecoin_address}: {total_count}")

        for page in range(total_pages):
            print(f"Fetching data on page {page}/{total_pages - 1} for address {filecoin_address}")
            api_response, url = fetch_table_data(filecoin_address, page, page_size)
            if api_response:
                rows = extract_data_from_api_response(api_response)
                for row in rows:
                    all_data.append([filecoin_address] + row)
            else:
                print(f"Failed to fetch data on page {page} or 'transfers' not found. URL: {url}")

    save_to_csv(all_data)

if __name__ == "__main__":
    filecoin_addresses = [
        "f0121", "f0117", "f0118", "f0119", "f0120", "f022572", "f022573", "f022574", "f022575", "f022576", 
        "f022577", "f022578", "f022579", "f022580", "f022581", "f022582", "f022583", "f022584", "f022585", 
        "f022586", "f022587", "f022588", "f022589", "f022590", "f022591", "f022592", "f022593", "f022594", 
        "f022595", "f022596", "f022597", "f022598", "f022599", "f022600", "f022601", "f022602", "f022603", 
        "f022604", "f022605", "f022606", "f022607", "f022608", "f022609", "f022610", "f022611", "f022612", 
        "f022613", "f022614", "f022615", "f022616", "f022617", "f022618", "f022619", "f022620", "f022621", 
        "f022622", "f022623", "f022624", "f022625", "f022626", "f022627", "f022628", "f022629", "f022630", 
        "f022631", "f022632", "f022633", "f022634", "f022635", "f022636", "f022637", "f022638", "f022639", 
        "f022640", "f022641", "f022642", "f022643", "f022644", "f022645", "f022646", "f022647", "f022648", 
        "f022649", "f022650", "f022651", "f022652", "f022653", "f022654", "f022655", "f022656", "f022657", 
        "f022658", "f022659", "f022660", "f022661", "f022662", "f022663", "f022664", "f022665", "f022666", 
        "f022667"
    ]
    fetch_all_transfers(filecoin_addresses)


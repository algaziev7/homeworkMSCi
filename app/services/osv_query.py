import httpx


async def query_osv_api(package_name: str):
    versions = set()
    versions.update(await query_ubuntu_osv_api(package_name))
    versions.update(await query_debian_osv_api(package_name))
    return sorted(versions)


async def query_ubuntu_osv_api(package_name: str):
    url = "https://api.osv.dev/v1/query"
    ecosystem = "Ubuntu"
    versions = set()

    async with httpx.AsyncClient() as client:
        payload = {
            "package": {
                "name": package_name,
                "ecosystem": ecosystem
            }
        }
        response = await client.post(url, json=payload)
        if response.status_code == 200:
            data = response.json()

            for item in data.get('vulns', []):
                for affected in item.get('affected', []):
                    versions.update(affected.get('versions', []))
                    if 'ecosystem_specific' in affected:
                        binaries = affected['ecosystem_specific'].get('binaries', [])
                        for binary in binaries:
                            versions.update(binary.values())
        else:
            print(f"Error {response.status_code} for {ecosystem}: {response.text}")

    return sorted(versions)


async def query_debian_osv_api(package_name: str):
    url = "https://api.osv.dev/v1/query"
    ecosystem = "Debian"

    async with httpx.AsyncClient() as client:
        payload = {
            "package": {
                "name": package_name,
                "ecosystem": ecosystem
            }
        }
        response = await client.post(url, json=payload)
        if response.status_code == 200:
            return get_versions(response.json())
        else:
            print(f"Error {response.status_code} for {ecosystem}: {response.text}")
            return []


def get_versions(vulnerability_data):
    extracted_versions = set()
    for vulnerability in vulnerability_data.get('vulns', []):
        for affected_package in vulnerability.get('affected', []):
            if 'ranges' in affected_package:
                for range_entry in affected_package['ranges']:
                    if 'events' in range_entry:
                        for event in range_entry['events']:
                            if 'fixed' in event:
                                extracted_versions.add(event['fixed'])
    return extracted_versions

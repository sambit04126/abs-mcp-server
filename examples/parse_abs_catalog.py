"""
Parse ABS dataflows.xml to extract all dataset mappings.
This creates a comprehensive reference for topic_mapping.py

Data source:
- Local: dta.xml (saved snapshot)
- Live API: https://data.api.abs.gov.au/rest/dataflow/all?detail=allstubs
"""
import xml.etree.ElementTree as ET
import json
import sys
import urllib.request

# Configuration
USE_LIVE_API = len(sys.argv) > 1 and sys.argv[1] == '--live'
CATALOG_URL = 'https://data.api.abs.gov.au/rest/dataflow/all?detail=allstubs'
LOCAL_FILE = 'dta.xml'

# Fetch or load catalog
if USE_LIVE_API:
    print(f"📡 Fetching live catalog from ABS API...")
    with urllib.request.urlopen(CATALOG_URL) as response:
        xml_data = response.read()
    root = ET.fromstring(xml_data)
    print(f"✅ Downloaded {len(xml_data)} bytes")
else:
    print(f"📂 Loading local catalog: {LOCAL_FILE}")
    tree = ET.parse(LOCAL_FILE)
    root = tree.getroot()

# Namespace mappings
ns = {
    'message': 'http://www.sdmx.org/resources/sdmxml/schemas/v2_1/message',
    'structure': 'http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure',
    'common': 'http://www.sdmx.org/resources/sdmxml/schemas/v2_1/common',
    'xml': 'http://www.w3.org/XML/1998/namespace'
}

# Extract all dataflows
dataflows = []
for dataflow in root.findall('.//structure:Dataflow', ns):
    dataset_id = dataflow.get('id')
    version = dataflow.get('version')
    
    # Get name - search without namespace attribute filter first
    name_elem = dataflow.find('.//common:Name', ns)
    name = name_elem.text if name_elem is not None else ""
    
    dataflows.append({
        'id': dataset_id,
        'version': version,
        'name': name
    })

# Group by topic keywords
topics = {
    'inflation': [],
    'cpi': [],
    'employment': [],
    'unemployment': [],
    'labour': [],
    'population': [],
    'gdp': [],
    'wages': [],
    'earnings': [],
    'retail': [],
    'housing': [],
    'building': [],
}

for df in dataflows:
    name_lower = df['name'].lower()
    
    for topic in topics:
        if topic in name_lower:
            topics[topic].append(df)

# Print summary for key topics
print("=" * 80)
print("ABS DATASET CATALOG ANALYSIS")
print("=" * 80)
print(f"\nTotal Production Datasets: {len(dataflows)}\n")

for topic, datasets in topics.items():
    if datasets:
        print(f"\n{topic.upper()} ({len(datasets)} datasets):")
        for ds in datasets[:5]:  # Show top 5
            print(f"  - {ds['id']}: {ds['name'][:70]}")
        if len(datasets) > 5:
            print(f"  ... and {len(datasets) - 5} more")

# Save full catalog
with open('abs_dataset_catalog.json', 'w') as f:
    json.dump(dataflows, f, indent=2)

print(f"\n✅ Full catalog saved to abs_dataset_catalog.json ({len(dataflows)} datasets)")

print("\n" + "=" * 80)
print("USAGE:")
print("  Local file:  python parse_abs_catalog.py")
print("  Live API:    python parse_abs_catalog.py --live")
print("=" * 80)

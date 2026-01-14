"""
Enhanced topic to dataset mappings based on ABS catalog analysis.
Generated from complete ABS dataset catalog (dta.xml - 1,219 datasets).

To refresh the catalog from ABS API:
  https://data.api.abs.gov.au/rest/dataflow/all?detail=allstubs
  Run: python examples/parse_abs_catalog.py --live

Key datasets discovered:
- CPI: 3 variants (quarterly, monthly, weights)
- Labour Force: 102 datasets
- GDP: 3 variants (expenditure, income, production)
- Population: 16 datasets
- Employment: 57 datasets  
- Retail: 1 dataset (RT)
- Wages: 1 dataset (AWE)
- Housing: 1 dataset (LEND_HOUSING)
- Building: 14 datasets
"""

TOPIC_TO_DATASET = {
    # INFLATION & CPI
    "inflation": {
        "dataset_id": "CPI_M",  # Monthly CPI - most current
        "aliases": ["CPI"],  # Quarterly version
        "description": "Monthly Consumer Price Index - latest inflation rates",
        "common_dimensions": {
            "MEASURE": "3",      # Percentage change
            "INDEX": "10001",    # All groups CPI
            "TSEST": "10",       # Original (not seasonally adjusted)
            "REGION": "50",      # Weighted average of eight capital cities
            "FREQ": "M"          # Monthly
        }
    },
    "cpi": {
        "dataset_id": "CPI_M",
        "description": "Monthly Consumer Price Index",
        "common_dimensions": {
            "MEASURE": "3",
            "INDEX": "10001",
            "TSEST": "10",
            "REGION": "50",
            "FREQ": "M"
        }
    },
    "price": {
        "dataset_id": "CPI_M",
        "description": "Consumer Price Index for price changes",
        "common_dimensions": {
            "MEASURE": "3",
            "INDEX": "10001",
            "TSEST": "10",
            "REGION": "50",
            "FREQ": "M"
        }
    },
    
    # EMPLOYMENT & LABOUR FORCE
    "employment": {
        "dataset_id": "LF",
        "description": "Labour Force - employment statistics",
        "common_dimensions": {
            "FREQ": "M",         # Monthly
            "TSEST": "20",       # Seasonally adjusted
            "SEX": "3",          # Persons
            "AGE": "1599",       # 15 years and over
            "REGION": "AUS"      # Australia
        }
    },
    "unemployment": {
        "dataset_id": "LF",
        "description": "Labour Force - unemployment rate",
        "common_dimensions": {
            "MEASURE": "M13",    # Unemployment rate
            "FREQ": "M",
            "TSEST": "20",
            "SEX": "3",
            "AGE": "1599",
            "REGION": "AUS"
        }
    },
    "jobs": {
        "dataset_id": "LF",
        "description": "Labour Force - employment statistics",
        "common_dimensions": {
            "FREQ": "M",
            "TSEST": "20",
            "SEX": "3",
            "AGE": "1599",
            "REGION": "AUS"
        }
    },
    "labour": {
        "dataset_id": "LF",
        "description": "Labour Force Survey",
        "common_dimensions": {
            "FREQ": "M",
            "TSEST": "20",
            "SEX": "3",
            "AGE": "1599",
            "REGION": "AUS"
        }
    },
    
    # POPULATION
    "population": {
        "dataset_id": "ABS_ANNUAL_ERP_ASGS2021",
        "description": "Estimated Resident Population by region (ASGS Edition 3)",
        "common_dimensions": {
            "MEASURE": "ERP",           # Estimated Resident Population
            "REGION_TYPE": "GCCSA",     # Greater Capital City Statistical Area
            "FREQ": "A"                 # Annual
        },
        "regional_codes": {
            "perth": "5GPER",
            "sydney": "1GSYD",
            "melbourne": "2GMEL",
            "brisbane": "3GBRI",
            "adelaide": "4GADE",
            "hobart": "6GHOB",
            "darwin": "7GDAR",
            "canberra": "8ACTE"
        }
    },
    
    # GDP & NATIONAL ACCOUNTS
    "gdp": {
        "dataset_id": "ANA_EXP",  # GDP by Expenditure approach
        "aliases": ["ANA_INC", "ANA_IND_GVA"],  # Income and Production approaches
        "description": "Gross Domestic Product (Expenditure approach)",
        "common_dimensions": {
            "FREQ": "Q"  # Quarterly
        }
    },
    "economy": {
        "dataset_id": "ANA_EXP",
        "description": "National Accounts - GDP",
        "common_dimensions": {
            "FREQ": "Q"
        }
    },
    
    # WAGES & EARNINGS
    "wages": {
        "dataset_id": "AWE",
        "description": "Average Weekly Earnings",
        "common_dimensions": {
            "FREQ": "Q"  # Quarterly
        }
    },
    "earnings": {
        "dataset_id": "AWE",
        "description": "Average Weekly Earnings",
        "common_dimensions": {
            "FREQ": "Q"
        }
    },
    "salary": {
        "dataset_id": "AWE",
        "description": "Average Weekly Earnings (salary proxy)",
        "common_dimensions": {
            "FREQ": "Q"
        }
    },
    
    # RETAIL TRADE
    "retail": {
        "dataset_id": "RT",
        "description": "Retail Trade turnover",
        "common_dimensions": {
            "FREQ": "M"  # Monthly
        }
    },
    
    # HOUSING & BUILDING
    "housing": {
        "dataset_id": "LEND_HOUSING",
        "description": "Lending Indicators for Housing Finance",
        "common_dimensions": {
            "FREQ": "M"
        }
    },
    "building": {
        "dataset_id": "BA_GCCSA",  # Building Approvals by Greater Capital City
        "description": "Building Approvals by Greater Capital City Statistical Area",
        "common_dimensions": {
            "FREQ": "M"
        }
    },
    "construction": {
        "dataset_id": "BA_GCCSA",
        "description": "Building Approvals (construction proxy)",
        "common_dimensions": {
            "FREQ": "M"
        }
    },
    
    # TRADE & EXPORTS
    "exports": {
        "dataset_id": "MERCH_EXP",  # Merchandise Exports by Commodity
        "description": "Merchandise Exports by Commodity (SITC), Country and State",
        "common_dimensions": {
            "FREQ": "M"
        }
    },
    "imports": {
        "dataset_id": "MERCH_IMP",  # Merchandise Imports
        "description": "Merchandise Imports by Commodity (SITC), Country and State",
        "common_dimensions": {
            "FREQ": "M"
        }
    },
    "trade": {
        "dataset_id": "ITGS",  # International Trade in Goods
        "description": "International Trade in Goods and Services",
        "common_dimensions": {
            "FREQ": "M"
        }
    },
    "commodity": {
        "dataset_id": "MERCH_EXP",
        "description": "Commodity exports (merchandise by SITC classification)",
        "common_dimensions": {
            "FREQ": "M"
        }
    },
    
    # MIGRATION
    "migration": {
        "dataset_id": "OMAD_VISA",  # Overseas Arrivals and Departures
        "description": "Overseas migrant arrivals and departures by visa group",
        "common_dimensions": {
            "FREQ": "Q"  # Quarterly
        }
    },
    "migrants": {
        "dataset_id": "OMAD_VISA",
        "description": "Overseas migration statistics by visa group",
        "common_dimensions": {
            "FREQ": "Q"
        }
    },
    
    # VITAL STATISTICS (Births/Deaths)
    "births": {
        "dataset_id": "BIRTHS_SUMMARY",
        "description": "Registered births summary by state",
        "common_dimensions": {
            "MEASURE": "1",      # Births
            "ASGS_2011": "0",    # Australia (Default) - use 1 for NSW, 2 for VIC etc.
            "FREQ": "A"          # Annual
        },
        "regional_codes": {
            "nsw": "1",
            "vic": "2",
            "qld": "3",
            "sa": "4",
            "wa": "5",
            "tas": "6",
            "nt": "7",
            "act": "8",
            "australia": "0"
        }
    },
    "deaths": {
        "dataset_id": "DEATHS_SUMMARY",
        "description": "Registered deaths summary by state",
        "common_dimensions": {
            "MEASURE": "1"  # Deaths
        }
    },
    "mortality": {
        "dataset_id": "PROV_MORTALITY",
        "description": "Provisional mortality statistics",
        "common_dimensions": {
            "MEASURE": "1"  # Deaths
        }
    }
}

def get_dataset_for_topic(query_text: str):
    """
    Find matching dataset based on query text.
    Returns (dataset_id, common_dimensions, regional_codes) or None.
    """
    query_lower = query_text.lower()
    
    for topic, info in TOPIC_TO_DATASET.items():
        if topic in query_lower:
            return (
                info["dataset_id"],
                info.get("common_dimensions", {}),
                info.get("regional_codes", {})
            )
    
    return None

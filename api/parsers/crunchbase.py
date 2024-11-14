import json

import requests

from api.parsers.base import BaseParser


class CrunchbaseParser(BaseParser):
    supported_domains = ["crunchbase.com"]

    def _fix_employee_count(self, count):
        pos1 = count.find("c_")
        pos2 = pos1 + 2
        while pos2 < len(count) and count[pos2] == "0":
            pos2 += 1
        count = count[:pos1] + count[pos2:]
        pos1 = count.find("_")
        pos2 = pos1 + 1
        while pos2 < len(count) and count[pos2] == "0":
            pos2 += 1
        count = count[:pos1] + "-" + count[pos2:]
        return count

    def _parse_organization_data(self, data):
        properties = data["properties"]
        cards = data["cards"]
        faqs = []
        for key in cards:
            if key.startswith("frequently_asked_questions"):
                faqs.append(cards[key])
        crunchbase_type = properties.get("layout_id", "company")
        more_about = cards[f"{crunchbase_type}_about_fields2"]
        num_employees = self._fix_employee_count(more_about["num_employees_enum"])
        location_identifiers = more_about["location_identifiers"]
        location_data = {}
        for location in location_identifiers:
            location_data[location["location_type"]] = location["value"]
        similar_orgs = cards["org_similarity_list"]
        competitors = []
        for org in similar_orgs:
            competitor = {
                "name": org["source"]["value"],
                "logo": "https://images.crunchbase.com/image/upload/c_pad,h_45,w_45,f_auto,b_white,q_auto:eco,dpr_4/"
                + org["source"]["image_id"],
                "description": org.get("source_short_description", ""),
                "locations": [loc["value"] for loc in org["source_locations"]],
                "categories": [cat["value"] for cat in org.get("source_categories", [])],
                "num_employees": (
                    self._fix_employee_count(org["source_num_employees_enum"])
                    if org.get("source_num_employees_enum")
                    else None
                ),
            }
            if org["source"]["value"] == properties["title"]:
                continue
            competitors.append(competitor)
        parsed = {
            "name": properties["title"],
            "website": more_about["website"]["value"],
            "company_type": more_about["ipo_status"] if "ipo_status" in more_about else more_about["investor_type"][0],
            "num_employees": num_employees,
            "location": location_data,
            "crunchbase_rank": (
                more_about["rank_org_company"] if "rank_org_company" in more_about else more_about["rank_principal_investor"]
            ),
            "funding_round": more_about.get("last_funding_type", None),
            "id": properties["identifier"]["permalink"],
            "logo": "https://images.crunchbase.com/image/upload/c_pad,h_45,w_45,f_auto,b_white,q_auto:eco,dpr_4/"
            + properties["identifier"]["image_id"],
            "description": properties["short_description"],
            "competitors": competitors,
            "faqs": faqs,
            "semrush_global_rank": cards["semrush_summary"].get("semrush_global_rank", None),
            "semrush_visits_latest_month": cards["semrush_summary"].get("semrush_visits_latest_month", None),
            "founded_on": cards["overview_fields_extended"]["founded_on"],
        }
        return parsed

    def parse(self, name):
        app_state_data = json.loads(requests.post("http://localhost:3000/scrape", json={"name": name}).json())
        cache_keys = list(app_state_data["HttpState"])
        try:
            data_cache_key = next(key for key in cache_keys if "entities/organizations/" in key)
        except Exception:
            return {}
        organization = app_state_data["HttpState"][data_cache_key]["data"]
        return self._parse_organization_data(organization)

from fastapi import APIRouter

from api import crud, schemes
from api.llm import llm_summary
from api.parsers import parse

router = APIRouter()


@router.post("")
def lookup_company(params: schemes.LookupParams):
    duckduckgo_result = parse("duckduckgo.com", params.name)
    wikipedia_result = parse("wikipedia.org", params.name)
    crunchbase_org = duckduckgo_result["crunchbase_org"] or params.name
    crunchbase_result = parse("crunchbase.com", crunchbase_org)
    website = crunchbase_result.get("website")
    site_parsed = None
    if website:
        site_parsed = parse(website, website)
    results = [
        {"source": "crunchbase", "data": crunchbase_result},
        {"source": "wikipedia", "data": wikipedia_result},
        {"source": "duckduckgo", "data": duckduckgo_result["company"]},
    ]
    if site_parsed:
        results.append({"source": "website", "data": site_parsed})
    llm_summary_result = llm_summary(params.name, results)
    data = {
        **crunchbase_result,
        **llm_summary_result,
        "wikipedia": wikipedia_result,
        "duckduckgo": duckduckgo_result["company"],
    }
    if "name" not in data:
        data["name"] = params.name
    request_id = crud.request.create(schemes.CreateRequest(data=data)).id
    return {"request_id": request_id, **data}

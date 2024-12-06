import json

import pytest

import api

request_json = json.load(open("./tests/data/requests.json"))
ai_result = {
    "ai_short_summary": "Lorem ipsum",
    "ai_long_summary": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
    "ai_competitor_summary": "test2",
}


@pytest.fixture
def mock_wiki_invoke(mocker):
    return mocker.patch("langchain_community.tools.WikipediaQueryRun.invoke", return_value=request_json["create"])


def duck_invoke(obj, input):
    if "site:crunchbase.com" in input:
        return json.dumps([{"link": "crunchbase.com/organization/test"}])
    return json.dumps(request_json["create"])


@pytest.fixture
def mock_duck_invoke(mocker):
    return mocker.patch("langchain_community.tools.DuckDuckGoSearchResults.invoke", new=duck_invoke)


@pytest.fixture
def mock_crunch_parser(mocker):
    return mocker.patch("api.parsers.crunchbase.CrunchbaseParser.parse", return_value=request_json["create"])


@pytest.fixture
def mock_generic_parser(mocker):
    return mocker.patch("langchain_community.document_loaders.WebBaseLoader.load", return_value=[request_json["create"]])


@pytest.fixture
def mock_llm_summary(mocker):
    return mocker.patch("api.views.lookup.llm_summary", return_value=ai_result)


def test_lookup_company(
    client,
    mock_wiki_invoke,
    mock_duck_invoke,
    mock_crunch_parser,
    mock_generic_parser,
    mock_llm_summary,
):
    response = client.post("/lookup", json={"name": "test"})
    assert response.status_code == 200
    assert (
        response.json().items()
        >= {
            **request_json["create"],
            **ai_result,
            "wikipedia": request_json["create"],
            "duckduckgo": request_json["create"],
        }.items()
    )

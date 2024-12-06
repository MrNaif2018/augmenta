import json

import pytest
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings

request_json = json.load(open("./tests/data/requests.json"))
ai_result = {
    "ai_short_summary": "Lorem ipsum",
    "ai_long_summary": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
    "ai_competitor_summary": "test2",
}


@pytest.fixture
def mock_wiki_invoke(mocker):
    return mocker.patch("langchain_community.tools.WikipediaQueryRun.invoke", return_value=request_json["create"])


@pytest.fixture
def mock_duck_invoke(mocker):
    return mocker.patch("langchain_community.tools.DuckDuckGoSearchResults.invoke", return_value=request_json["create"])


@pytest.fixture
def mock_crunch_search_invoke(mocker):
    return mocker.patch(
        "langchain_community.tools.DuckDuckGoSearchResults.invoke",
        return_value=json.dumps([{"link": "crunchbase.com/organization/test"}]),
    )


@pytest.fixture
def mock_crunch_parser(mocker):
    return mocker.patch("api.parsers.crunchbase.CrunchbaseParser.parse", return_value=request_json["create"])


@pytest.fixture
def mock_generic_parser(mocker):
    return mocker.patch("langchain_community.document_loaders.WebBaseLoader.load", return_value=[request_json["create"]])


@pytest.fixture
def mock_llm_summary(mocker):
    return mocker.patch("api.llm.llm_summary", return_value=ai_result)


def test_lookup_company(
    client,
    mock_wiki_invoke,
    mock_duck_invoke,
    mock_crunch_search_invoke,
    mock_crunch_parser,
    mock_generic_parser,
    mock_llm_summary,
):
    response = client.post("/lookup", json={"name": "test"})
    assert response.status_code == 200
    assert response.json() >= {
        **request_json["create"],
        **ai_result,
        "wikipedia": request_json["create"],
        "duckduckgo": request_json["create"],
    }

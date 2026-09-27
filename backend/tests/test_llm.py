from app.llm.client import get_llm_client


def test_llm_provider_created():
    client = get_llm_client()

    assert client is not None
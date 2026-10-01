from app.rag.retriever import normalize_retrieval_query


def test_inverter_query_is_expanded_with_guideline_context():
    query = normalize_retrieval_query(
        "What requirements apply to rooftop solar inverters?"
    )

    assert "installation guideline" in query
    assert "protection" in query


def test_bess_query_is_expanded_with_interconnection_context():
    query = normalize_retrieval_query(
        "What does RTSPV with BESS mean?"
    )

    assert "interconnection" in query
    assert "prosumer" in query

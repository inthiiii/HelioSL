def test_empty_knowledge_result_structure():
    result = {
        "query": "Net Metering",
        "result_count": 0,
        "context": "",
    }

    assert result["result_count"] == 0
    assert result["context"] == ""

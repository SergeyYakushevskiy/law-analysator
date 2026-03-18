def test_add_and_get_document(document_repo):
    doc = document_repo.add_document("Test Doc")
    assert doc.id is not None
    assert doc.name == "Test Doc"

    fetched = document_repo.get(doc.id)
    assert fetched.id == doc.id
    assert fetched.name == "Test Doc"

def test_get_all_documents(document_repo):
    document_repo.add_document("Doc1")
    document_repo.add_document("Doc2")
    all_docs = document_repo.get_all()
    assert len(all_docs) == 2

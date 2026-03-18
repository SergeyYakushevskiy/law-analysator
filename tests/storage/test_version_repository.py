def test_versions_order_real_data(version_repo, version_service, document_repo, grouped_versions):
    doc = document_repo.add_document("Doc")

    for key in sorted(grouped_versions.keys()):
        file = sorted(grouped_versions[key])[0]
        version_service.add_new_version(doc.id, file)

    versions = version_repo.get_versions(doc.id)

    positions = [v.position for v in versions]
    assert positions == sorted(positions)

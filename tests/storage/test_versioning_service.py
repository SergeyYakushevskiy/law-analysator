def test_add_versions_grouped(version_service, document_repo, grouped_versions):
    doc = document_repo.add_document("Doc")

    ordered_keys = sorted(grouped_versions.keys())  # test_1, test_2, test_3

    created_versions = []

    for key in ordered_keys:
        # берём любой файл как представитель версии (например txt)
        file = sorted(grouped_versions[key])[0]
        v = version_service.add_new_version(doc.id, file)
        created_versions.append(v)

    # Проверка порядка
    positions = [v.position for v in created_versions]
    assert positions == sorted(positions)

    # Проверка количества логических версий
    assert len(created_versions) == 3
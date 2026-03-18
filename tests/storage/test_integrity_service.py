from src.storage.services.integrity_service import IntegrityService

def test_integrity_grouped(version_repo, version_service, document_repo, grouped_versions):
    doc = document_repo.add_document("Doc")

    for key in sorted(grouped_versions.keys()):
        file = sorted(grouped_versions[key])[0]
        version_service.add_new_version(doc.id, file)

    integrity_service = IntegrityService(version_repo, version_service)
    problems = integrity_service.verify_versions()

    assert problems == []

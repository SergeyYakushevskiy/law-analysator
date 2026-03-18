from src.storage.services.folder_sync_service import FolderSyncService

def test_detect_untracked_formats(version_repo, version_service, document_repo, versioned_folder, grouped_versions):
    doc = document_repo.add_document("Doc")

    # Добавляем только .txt версии
    for key in sorted(grouped_versions.keys()):
        txt_file = next(f for f in grouped_versions[key] if f.suffix == ".txt")
        version_service.add_new_version(doc.id, txt_file)

    folder_service = FolderSyncService(versioned_folder, version_repo, version_service)

    changes = folder_service.detect_changes(doc.id)

    # Остальные форматы должны считаться новыми
    assert len(changes["new_files"]) > 0

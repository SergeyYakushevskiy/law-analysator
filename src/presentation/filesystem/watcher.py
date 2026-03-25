import logging
import os
from typing import Callable, Set
from PyQt6.QtCore import QFileSystemWatcher, QTimer

logger = logging.getLogger(__name__)
class ProjectWatcher:
    def __init__(self, root_path, on_change: Callable[[], None]):
        logger.debug('запуск project watcher')
        self._root_path = str(root_path)
        self._on_change = on_change

        self._watcher = QFileSystemWatcher()
        self._watched_dirs: Set[str] = set()

        self._debounce_timer = QTimer()
        self._debounce_timer.setSingleShot(True)
        self._debounce_timer.setInterval(500)  # 500 мс
        self._debounce_timer.timeout.connect(self._trigger_change)

        self._init_watch()

        self._watcher.directoryChanged.connect(self._on_directory_changed)
        self._watcher.fileChanged.connect(self._on_file_changed)
        logger.info('project watcher запущен')


    def _init_watch(self):
        self._add_directories_recursively(self._root_path)

    def _add_directories_recursively(self, path: str):
        for root, dirs, _ in os.walk(path):
            self._add_directory(root)

    def _add_directory(self, path: str):
        if path not in self._watched_dirs:
            self._watcher.addPath(path)
            self._watched_dirs.add(path)

    def _on_directory_changed(self, path: str):
        if os.path.exists(path):
            self._add_directories_recursively(path)

        self._schedule_update()

    def _on_file_changed(self, path: str):
        self._schedule_update()

    def _schedule_update(self):
        self._debounce_timer.start()

    def _trigger_change(self):
        self._on_change()

    def stop(self):
        self._watcher.directoryChanged.disconnect()
        self._watcher.fileChanged.disconnect()

        self._watcher.removePaths(list(self._watched_dirs))
        self._watched_dirs.clear()

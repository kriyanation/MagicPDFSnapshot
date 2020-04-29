import json, snapshot_view

class MagicSnapshotController():
    def __init__(self,json_lesson):
                    self.snapshotapp = snapshot_view.SnapshotView(json_lesson)
    def getSnapshotView(self):
                    return self.snapshotapp


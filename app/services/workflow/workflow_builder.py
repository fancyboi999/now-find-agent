from loguru import logger

class workflow_builder(db=None):
    def __init__(self, db=None):
        self.db = db

    async def build_graph_async(self):
        pass
class JsonConvert:
    @classmethod
    def data_to_json(cls,data):
        if hasattr(data, "model_dump"):
            return data.model_dump()
        return data
import base64


class AssetsHandler:

    def __init__(self, filename):
        self.filename = filename

    def encode_file_to_base64(self):
        return base64.b64encode(
            open(self.filename, "rb").read()
        )
    
    def decode_base64(self):
        return "data:image/png;base64,{}".format(self.encode_file_to_base64().decode())

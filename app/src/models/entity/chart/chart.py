class Chart:
    
    def __init__(self, data_frame, addit_data_frame=None, template="plotly_dark"):
        self.data_frame = data_frame
        self.addit_data_frame = addit_data_frame
        self.template = template

    def create(self):
        pass

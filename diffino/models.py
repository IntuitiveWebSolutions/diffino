

class Diffino:
    def __init__(self, **kwargs):
        left = kwargs.get('left')
        right = kwargs.get('left')
        output = kwargs.get('output')
        convert_numeric = kwargs.get('convert_numeric', True)
        mode = kwargs.get('mode', 'pandas')
        cols = kwargs.get('cols')

        self.diff_results = {}

    def _build_inputs(self):
        pass

    def build_diff(self):
        return self.diff_results

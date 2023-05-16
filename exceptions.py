class ElementNotFoundError(Exception):
    def __init__(self, element):
        self.element = element

    def __str__(self):
        return f'Element not found: {self.element}'

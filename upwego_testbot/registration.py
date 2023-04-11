class User:

    def __init__(self, name, surname, upwego_code):
        self.name = name
        self.surname = surname
        self.upwego_code = upwego_code

    def set_variables(self, name, surname, upwego_code):
        result = f"'name': {{{name}}}, 'surname': {{{surname}}}, 'upwego_code': {{{upwego_code}}}"
        print(result)

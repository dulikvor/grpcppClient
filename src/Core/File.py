class File:
    def __init__(self, filePath, permissions = 'r'):
        self.__filePath = filePath
        self.__permissions = permissions

    def __enter__(self):
        self.__file = open(self.__filePath, self.__permissions)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__file.close()

    def __iter__(self):
        if hasattr(self, '_File__file') == False:
            raise AttributeError('The file is not opened yet, use with statement.')
        def LineReader():
            for line in self.__file:
                yield line

        return LineReader()
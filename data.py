class ToBytesBandwidthConverter:
    @classmethod
    def from_kilobytes(cls, kilobytes):
        return kilobytes * 1024

    @classmethod
    def from_megabytes(cls, megabytes):
        return cls.from_kilobytes(megabytes * 1024)

    @classmethod
    def from_gigabytes(cls, gigabytes):
        return cls.from_megabytes(gigabytes * 1024)

    @classmethod
    def from_terabytes(cls, terabytes):
        return cls.from_gigabytes(terabytes * 1024)


class FromBytesBandwidthConverter:
    @classmethod
    def to_kilobytes(cls, bytes_):
        return bytes_ / 1024

    @classmethod
    def to_megabytes(cls, bytes_):
        return bytes_ / (1024**2)

    @classmethod
    def to_gigabytes(cls, bytes_):
        return bytes_ / (1024**3)

    @classmethod
    def to_terabytes(cls, bytes_):
        return bytes_ / (1024**4)

    @classmethod
    def beautify(cls, bytes_):
        if bytes_ < 1024:
            return f'{bytes_} bytes'
        elif bytes_ < 1024 ** 2:
            return f'{cls.to_kilobytes(bytes_)} KB'
        elif bytes_ < 1024 ** 3:
            return f'{cls.to_megabytes(bytes_)} MB'
        elif bytes_ < 1024 ** 4:
            return f'{cls.to_gigabytes(bytes_)} GB'
        else:
            return f'{cls.to_terabytes(bytes_)} TB'
"""     Misc mock utilities.
"""
import datetime


def mock_true(*args, **kwargs):
    """ Always return True
    """
    return True


def mock_false(*args, **kwargs):
    """ Always return False
    """
    return False


def mock_pass(*args, **kwargs):
    """ Always pass
    """
    pass


def mock_datetime(year, month, day, hour=0, minute=0, second=0):
    """ This is for mocking datetime.datetime.today() - can't patch this directly
        as it's a builtin so we subclass the whole datetime type

        :returns:       datetime class object

        Eg::

            @patch('datetime.datetime', mock_datetime(year=1989)
            test_foo():
                assert datetime.datetime.today().year == 1989
    """
    class d(datetime.datetime):
        @classmethod
        def today(cls):
            return cls(year=year, month=month, day=day)

        @classmethod
        def now(cls):
            return cls(year=year, month=month, day=day, hour=hour, minute=minute, second=second)

        # Can be extended to other datetime methods
    return d

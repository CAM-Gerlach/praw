"""Provide the RedditBase class."""
from ...const import API_PATH
from ..base import PRAWBase


class RedditBase(PRAWBase):
    """Base class that represents actual Reddit objects."""

    @property
    def fullname(self):
        """Return the object's fullname.

        A fullname is an object's kind mapping like `t3` followed by an
        underscore and the object's base36 ID, e.g., `t1_c5s96e0`.

        """
        return '{}_{}'.format(self._reddit._objector.kind(self),
                              self.id)  # pylint: disable=invalid-name

    def __eq__(self, other):
        """Return whether the other instance equals the current."""
        if isinstance(other, str):
            return other.lower() == str(self).lower()
        return (isinstance(other, self.__class__) and
                str(self).lower() == str(other).lower())

    def __getattr__(self, attribute):
        """Return the value of `attrribute`."""
        if not attribute.startswith('__') and not self._fetched:
            self._fetch()
            return getattr(self, attribute)
        raise AttributeError('{!r} object has no attribute {!r}'
                             .format(self.__class__.__name__, attribute))

    def __hash__(self):
        """Return the hash of the current instance."""
        return hash(self.__class__.__name__) ^ hash(str(self).lower())

    def __init__(self, reddit, _data):
        """Initialize a RedditBase instance.

        :param reddit: An instance of :class:`~.Reddit`.

        """
        super(RedditBase, self).__init__(reddit, _data)
        self._fetched = False

    def __repr__(self):
        """Return an object initialization representation of the instance."""
        return '{}({}={!r})'.format(self.__class__.__name__, self.STR_FIELD,
                                    str(self))

    def __str__(self):
        """Return a string representation of the instance."""
        return getattr(self, self.STR_FIELD)

    def __ne__(self, other):
        """Return whether the other instance differs from the current."""
        return not self == other

    def _fetch(self):
        if '_info_path' in dir(self):
            other = self._reddit.get(self._info_path())
        else:
            other = self._reddit.get(API_PATH['info'],
                                     params={'id': self.fullname}).children[0]
        self.__dict__.update(other.__dict__)
        self._fetched = True

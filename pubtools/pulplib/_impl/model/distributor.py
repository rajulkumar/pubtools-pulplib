import datetime

from .common import PulpObject
from .attr import pulp_attrib
from ..schema import load_schema
from .. import compat_attr as attr


@attr.s(kw_only=True, frozen=True)
class Distributor(PulpObject):
    """Represents a Pulp distributor."""

    _SCHEMA = load_schema("repository", "distributor")

    id = pulp_attrib(type=str, pulp_field="id")
    """ID of this distributor (str).

    This is an arbitrary string, though often matches exactly the `type_id`.
    """

    type_id = pulp_attrib(type=str, pulp_field="distributor_type_id")
    """Type ID of this distributor (str).

    The type ID of a distributor determines which content may be handled and
    which steps may be performed by the distributor. For example, distributors
    of type `yum_distributor` may be used to create yum repositories.
    """

    repo_id = pulp_attrib(type=str, default=None, pulp_field="repo_id")
    """The :class:`pubtools.pulplib.Repository` ID this distributor is attached to."""

    last_publish = pulp_attrib(
        default=None, type=datetime.datetime, pulp_field="last_publish"
    )
    """The :class:`~datetime.datetime` at which this distributor was last published,
    if known."""

    is_rsync = attr.ib(
        default=attr.Factory(
            lambda self: self.type_id
            in (
                "rpm_rsync_distributor",
                "iso_rsync_distributor",
                "docker_rsync_distributor",
            ),
            takes_self=True,
        )
    )
    """True for distributors in the 'rsync distributor' family
    (e.g. ``rpm_rsync_distributor``).
    """

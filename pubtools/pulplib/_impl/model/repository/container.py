from .base import Repository, repo_type
from ..attr import pulp_attrib
from ... import compat_attr as attr


@repo_type("docker-repo")
@attr.s(kw_only=True, frozen=True)
class ContainerImageRepository(Repository):
    """A :class:`~pubtools.pulplib.Repository` for container images."""

    type = pulp_attrib(default="docker-repo", type=str, pulp_field="notes._repo-type")

    registry_id = attr.ib(
        default=attr.Factory(lambda self: self.id, takes_self=True), type=str
    )
    """The ID of this repository in a container image registry.

    For example:

    - pulp repo id: redhat-rhel7-openscap
    - registry id:  rhel7/openscap

    The registry id is used by clients of the published repo, i.e.

    ``docker pull registry.example.com/<registry_id>:latest``
    """

    @classmethod
    def _data_to_init_args(cls, data):
        out = super(ContainerImageRepository, cls)._data_to_init_args(data)

        for dist in data.get("distributors") or []:
            if dist["distributor_type_id"] == "docker_distributor_web":
                out["registry_id"] = dist["config"].get("repo-registry-id")
                break

        return out

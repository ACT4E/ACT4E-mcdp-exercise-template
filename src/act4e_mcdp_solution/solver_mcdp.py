from typing import Any, Mapping

from act4e_mcdp import Interval, LowerSet, MCDPSolverInterface, NamedDP, UpperSet

__all__ = [
    "MCDPSolver",
]


class MCDPSolver(MCDPSolverInterface):
    def solve_mcdp_FixFunMinRes(
        self,
        graph: NamedDP,
        functionality_needed: Mapping[str, Any],
        /,
        resolution_optimistic: int = 0,
        resolution_pessimistic: int = 0,
    ) -> Interval[UpperSet[Mapping[str, Any]]]:
        value_as_tuple = tuple(functionality_needed[key] for key in graph.functionalities)

        optimistic = pessimistic = UpperSet([])
        return Interval(pessimistic=pessimistic, optimistic=optimistic)

    def solve_mcdp_FixResMaxFun(
        self,
        graph: NamedDP,
        resources_budget: Mapping[str, Any],
        /,
        resolution_optimistic: int = 0,
        resolution_pessimistic: int = 0,
    ) -> Interval[LowerSet[Mapping[str, Any]]]:
        value_as_tuple = tuple(resources_budget[key] for key in graph.resources)
        optimistic = pessimistic = LowerSet([])
        return Interval(pessimistic=pessimistic, optimistic=optimistic)

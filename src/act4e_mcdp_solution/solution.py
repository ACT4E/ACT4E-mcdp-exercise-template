from typing import Any, Mapping

from act4e_mcdp import NamedDP, SolverInterface, UpperSet, LowerSet

__all__ = ["MySolution"]


class MySolution(SolverInterface):
    def solve_FixFunMinRes(self, model: NamedDP, query: Mapping[str, Any]) -> UpperSet[Mapping[str, Any]]:
        # returns the empty upper set - marking it as infeasible
        return UpperSet([])

    def solve_FixResMaxFun(self, model: NamedDP, query: Mapping[str, Any]) -> LowerSet[Mapping[str, Any]]:
        # returns the empty upper set - marking it as infeasible
        return LowerSet([])

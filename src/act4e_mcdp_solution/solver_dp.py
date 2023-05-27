from act4e_mcdp import DPSolverInterface, Interval, LowerSet, PrimitiveDP, UpperSet

__all__ = [
    "DPSolver",
]


class DPSolver(DPSolverInterface):
    def solve_dp_FixFunMinRes(
        self,
        dp: PrimitiveDP,
        functionality_needed: object,
        /,
        resolution_optimistic: int = 0,
        resolution_pessimistic: int = 0,
    ) -> Interval[UpperSet[object]]:
        optimistic = pessimistic = UpperSet([])
        return Interval(pessimistic=pessimistic, optimistic=optimistic)

    def solve_dp_FixResMaxFun(
        self,
        dp: PrimitiveDP,
        resource_budget: object,
        /,
        resolution_optimistic: int = 0,
        resolution_pessimistic: int = 0,
    ) -> Interval[LowerSet[object]]:
        optimistic = pessimistic = LowerSet([])
        return Interval(pessimistic=pessimistic, optimistic=optimistic)

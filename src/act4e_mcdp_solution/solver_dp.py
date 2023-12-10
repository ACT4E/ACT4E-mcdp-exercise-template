from typing import Optional, TypeVar
from act4e_mcdp import *  # type: ignore
from decimal import Decimal

__all__ = [
    "DPSolver",
]


X = TypeVar("X")
FT = TypeVar("FT")
RT = TypeVar("RT")
R1 = TypeVar("R1")
R2 = TypeVar("R2")
F1 = TypeVar("F1")
F2 = TypeVar("F2")


class DPSolver(DPSolverInterface):
    # walkthrough: identity

    def solve_dp_FixFunMinRes_IdentityDP(
        self, _: IdentityDP[X], query: FixFunMinResQuery[X]
    ) -> Interval[UpperSet[X]]:
        # Easy: the minimal resources are the functionality itself
        f = query.functionality
        min_r = f
        min_resources = UpperSet.principal(min_r)

        # We need to return an interval of upper sets. It is a degenerate interval
        return Interval.degenerate(min_resources)

    def solve_dp_FixResMaxFun_IdentityDP(
        self, _: IdentityDP[X], query: FixResMaxFunQuery[X]
    ) -> Interval[LowerSet[X]]:
        # same as above, but we return lower sets

        r = query.resources
        max_f = r
        max_functionalities = LowerSet.principal(max_f)
        return Interval.degenerate(max_functionalities)

    # walkthrough: constant resources

    def solve_dp_FixFunMinRes_Constant(
        self, dp: Constant[X], query: FixFunMinResQuery[tuple[()]]
    ) -> Interval[UpperSet[X]]:
        # The DP is a relation of the type
        #
        #    42 ≤ r

        # The functionalities are the empty tuple

        assert query.functionality == (), query.functionality

        # The minimal resources do not depend on functionality
        # They are the constant value of the DP

        min_r = dp.c.value
        min_resources = UpperSet.principal(min_r)
        return Interval.degenerate(min_resources)

    def solve_dp_FixResMaxFun_Constant(
        self, dp: Constant[X], query: FixResMaxFunQuery[X]
    ) -> Interval[LowerSet[tuple[()]]]:
        # The DP is a relation of the type
        #
        #    42 ≤ r

        # Here we need to check whether the resources are at least 42

        R = dp.R
        if R.leq(dp.c.value, query.resources):
            # the functionalities are the empty tuple
            max_f = ()
            return Interval.degenerate(LowerSet.principal(max_f))
        else:
            # the given budget is not enough
            empty: LowerSet[tuple[()]] = LowerSet.empty()
            return Interval.degenerate(empty)

    # exercise: limit

    def solve_dp_FixResMaxFun_Limit(self, dp: Limit[X], query: FixResMaxFunQuery[X]) -> Interval[LowerSet[X]]:
        # The DP is a relation of the type
        #
        #    f ≤ 42

        # This is the dual of Constant above. Swap functionalities and resources.

        raise NotImplementedError

    def solve_dp_FixFunMinRes_Limit(
        self, dp: Limit[X], query: FixFunMinResQuery[X]
    ) -> Interval[UpperSet[tuple[()]]]:
        # The DP is a relation of the type
        #
        #    f ≤ 42

        # This is the dual of Constant above. Swap functionalities and resources.

        raise NotImplementedError

    # walkthrough: ceil(f) <= r  DP

    def solve_dp_FixFunMinRes_M_Ceil_DP(
        self, dp: M_Ceil_DP, query: FixFunMinResQuery[Decimal]
    ) -> Interval[UpperSet[Decimal]]:
        # In the documentation of the class M_Ceil_DP we have
        # that the relation is defined as:
        #
        #   ceil(f) ≤ r

        # Therefore, the minimal resources are the ceiling of the functionality
        #   r >= ceil(f)
        f = query.functionality
        assert isinstance(f, Decimal)

        # For M_Ceil_DP, the F and R posets are Numbers
        R: Numbers = dp.R
        F: Numbers = dp.F

        # Note: the f = +inf is a special case for which __ceil__() does not work
        if f.is_infinite():
            min_r = f
        else:
            # otherwise, we just use the ceil function
            min_r = Decimal(f.__ceil__())

        # now, one last detail: in general, the F poset can have
        # different upper/lower bound or discretization than the R poset.
        # We need to make sure that we provide a valid resource.

        # There is a function largest_upperset_above() that will do this for us.
        # See documentation there.

        min_resources = R.largest_upperset_above(min_r)
        return Interval.degenerate(min_resources)

    def solve_dp_FixResMaxFun_M_Ceil_DP(
        self, dp: M_Ceil_DP, query: FixResMaxFunQuery[Decimal]
    ) -> Interval[LowerSet[Decimal]]:
        # Now r is fixed
        r = query.resources
        assert isinstance(r, Decimal), r

        R: Numbers = dp.R
        F: Numbers = dp.F

        # For M_Ceil_DP, the F/R posets are Numbers

        # first special case: r = +inf
        if r.is_infinite():
            max_f = r

        else:
            # what is the maximum f such that
            #   ceil(f) <= r
            # ?

            # for example, if r = 13.2, then the maximum f is 13
            # in fact, we obtain the floor of r

            max_f = Decimal(r.__floor__())

        # one last detail: we need to make sure that the functionality is valid
        # for the F poset. We use the largest_lowerset_below() function in Numbers.
        # See documentation there.

        max_functionalities = F.largest_lowerset_below(max_f)

        return Interval.degenerate(max_functionalities)

    # exercise: floor relation

    def solve_dp_FixFunMinRes_M_FloorFun_DP(
        self, dp: M_FloorFun_DP, query: FixFunMinResQuery[Decimal]
    ) -> Interval[UpperSet[Decimal]]:
        # f <= floor(r)

        # This is dual to M_Ceil_DP

        raise NotImplementedError

    def solve_dp_FixResMaxFun_M_FloorFun_DP(
        self, dp: M_FloorFun_DP, query: FixResMaxFunQuery[Decimal]
    ) -> Interval[LowerSet[Decimal]]:
        # f <= floor(r)

        # This is dual to M_Ceil_DP

        raise NotImplementedError

    # exercise: catalogue

    def solve_dp_FixFunMinRes_CatalogueDP(
        self, dp: CatalogueDP[FT, RT], query: FixFunMinResQuery[FT]
    ) -> Interval[UpperSet[RT]]:
        f = query.functionality
        F = dp.F

        # Hint: iterate over the entries of the catalogue
        name: str
        entry_info: EntryInfo[FT, RT]
        for name, entry_info in dp.entries.items():
            # Then check if this entry is valid for the functionality
            # In that case,  the resources of the entry are a valid solution
            ...

        raise NotImplementedError

    def solve_dp_FixResMaxFun_CatalogueDP(
        self, dp: CatalogueDP[FT, RT], query: FixResMaxFunQuery[RT]
    ) -> Interval[LowerSet[FT]]:
        # Same pattern as above, but functionalities and resources are swapped.

        raise NotImplementedError

    # exercise: series interconnections

    def solve_dp_FixFunMinRes_DPSeries(
        self, dp: DPSeries, query: FixFunMinResQuery[object]
    ) -> Interval[UpperSet[object]]:
        # This is the interconnection of a sequence of DPs.
        # (You can assume that the sequence is at least 2 DPs).

        # Hint: you should solve each DP in the sequence, and then
        # pass it to the next.
        # You can use the function self.solve_dp_FixFunMinRes() for this.

        # Note 1: the solve_dp_FixFunMinRes_DPSeries() takes a single functionality.
        # But in general the previous DP returns an upperset. You need to call it multiple times.
        # Note 2: the solve_dp_FixFunMinRes_DPSeries() returns an *interval* of upper sets.
        # Just treat the optimistic and pessimistic cases separately and then combine them in an interval.

        raise NotImplementedError

    def solve_dp_FixResMaxFun_DPSeries(
        self, dp: DPSeries, query: FixResMaxFunQuery[object]
    ) -> Interval[LowerSet[object]]:
        # Hint: same as above, but go the other way...
        raise NotImplementedError

    # walkthrough: add a constant to functionalities ( f + constant <= r)

    def solve_dp_FixFunMinRes_M_Res_AddConstant_DP(
        self, dp: M_Res_AddConstant_DP, query: FixFunMinResQuery[Decimal]
    ) -> Interval[UpperSet[Decimal]]:
        f: Decimal = query.functionality
        assert isinstance(f, Decimal)

        R: Numbers = dp.R
        F: Numbers = dp.F

        # the relation is of the type
        #
        #    f + constant <= r

        # therefore, the minimum resource is simply f + constant
        min_r = f + dp.vu.value

        # one last detail: we need to make sure that the resource is valid
        # for the R poset. We use the largest_upperset_above() function in Numbers.
        # See documentation there.
        us = R.largest_upperset_above(min_r)

        return Interval.degenerate(us)

    def solve_dp_FixResMaxFun_M_Res_AddConstant_DP(
        self, dp: M_Res_AddConstant_DP, query: FixResMaxFunQuery[Decimal]
    ) -> Interval[LowerSet[Decimal]]:
        r = query.resources
        assert isinstance(r, Decimal)

        R: Numbers = dp.R
        F: Numbers = dp.F

        # the relation is of the type
        #
        #    f + constant <= r

        # therefore, the maximal functionality is r - constant

        max_f = r - dp.vu.value

        # one last detail: we need to make sure that the functionality is valid
        # for the F poset. We use the largest_lowerset_below() function in Numbers.
        # See documentation there.
        ls = F.largest_lowerset_below(max_f)

        return Interval.degenerate(ls)

    # exercise: add a constant to resource ( f <= r + constant)

    def solve_dp_FixFunMinRes_M_Fun_AddConstant_DP(
        self, dp: M_Fun_AddConstant_DP, query: FixFunMinResQuery[Decimal]
    ) -> Interval[UpperSet[Decimal]]:
        # f <= r + constant
        # This is dual to the M_Res_AddConstant_DP case above.
        raise NotImplementedError

    def solve_dp_FixResMaxFun_M_Fun_AddConstant_DP(
        self, dp: M_Fun_AddConstant_DP, query: FixResMaxFunQuery[Decimal]
    ) -> Interval[LowerSet[Decimal]]:
        # f <= r + constant
        # This is dual to the M_Res_AddConstant_DP case above.

        raise NotImplementedError

    # walkthrough: multiplying constants (f * constant <= r)
    def solve_dp_FixFunMinRes_M_Res_MultiplyConstant_DP(
        self, dp: M_Res_MultiplyConstant_DP, query: FixFunMinResQuery[Decimal]
    ) -> Interval[UpperSet[Decimal]]:
        #  (f * constant <= r)

        # This is similar to the M_Res_AddConstant_DP case above with
        # multiplication instead of addition.

        f = query.functionality
        assert isinstance(f, Decimal)
        min_r = f * dp.vu.value

        # one last detail: we need to make sure that the resource is valid
        # for the R poset. We use the largest_upperset_above() function in Numbers.
        # See documentation there.
        us = dp.R.largest_upperset_above(min_r)

        return Interval.degenerate(us)

    def solve_dp_FixResMaxFun_M_Res_MultiplyConstant_DP(
        self, dp: M_Res_MultiplyConstant_DP, query: FixResMaxFunQuery[Decimal]
    ) -> Interval[LowerSet[Decimal]]:
        #  (f * constant <= r)

        raise NotImplementedError

    # exercise: multiply by constant (f  <= r * constant)

    def solve_dp_FixFunMinRes_M_Fun_MultiplyConstant_DP(
        self, dp: M_Fun_MultiplyConstant_DP, query: FixFunMinResQuery[Decimal]
    ) -> Interval[UpperSet[Decimal]]:
        raise NotImplementedError

    def solve_dp_FixResMaxFun_M_Fun_MultiplyConstant_DP(
        self, dp: M_Fun_MultiplyConstant_DP, query: FixResMaxFunQuery[Decimal]
    ) -> Interval[LowerSet[Decimal]]:
        raise NotImplementedError

    # walktrough: multiply functionalities

    def solve_dp_FixResMaxFun_M_Fun_MultiplyMany_DP(
        self, dp: M_Fun_MultiplyMany_DP, query: FixResMaxFunQuery[tuple[Decimal, ...]]
    ) -> Interval[LowerSet[Decimal]]:
        # f <= r1 * r2 * r3 * ...

        # This direction is easy, we just multiply the resources

        res = Decimal(1)
        for ri in query.resources:
            res *= ri
        ls = dp.F.largest_lowerset_below(res)
        return Interval.degenerate(ls)

    # exercise: multiply resources

    def solve_dp_FixFunMinRes_M_Res_MultiplyMany_DP(
        self, dp: M_Res_MultiplyMany_DP, query: FixFunMinResQuery[tuple[Decimal, ...]]
    ) -> Interval[UpperSet[Decimal]]:
        # f1 * f2 * f3 * ... <= r
        # similar to the above

        # this is the easy direction

        raise NotImplementedError

    # walkthough: add many

    def solve_dp_FixFunMinRes_M_Res_AddMany_DP(
        self, dp: M_Res_AddMany_DP, query: FixFunMinResQuery[tuple[Decimal, ...]]
    ) -> Interval[UpperSet[Decimal]]:
        # f1 + f2 + f3 + ... <= r

        f = query.functionality
        F: PosetProduct[Decimal] = dp.F
        assert isinstance(f, tuple), f
        assert len(f) == len(F.subs), (f, F)

        # This direction is easy, we just add the functionalities
        res = f[0]
        for fi in f[1:]:
            res += fi

        min_r = res
        us = dp.R.largest_upperset_above(min_r)
        return Interval.degenerate(us)

    # exercise: add many functionalities

    def solve_dp_FixResMaxFun_M_Fun_AddMany_DP(
        self, dp: M_Fun_AddMany_DP, query: FixResMaxFunQuery[tuple[Decimal, ...]]
    ) -> Interval[LowerSet[Decimal]]:
        # this is a relation of the type
        #  (f1 ≤  r) and (f2 ≤ r) and (f3 ≤ r) and ...

        # This direction is easy, we just add the resources

        raise NotImplementedError

    # exercise: meet

    def solve_dp_FixFunMinRes_MeetNDualDP(
        self, dp: MeetNDualDP[X], query: FixFunMinResQuery[X]
    ) -> Interval[UpperSet[tuple[X, ...]]]:
        # this is a relation of the type
        #  (f ≤  r₁) and (f ≤  r2)  and (f ≤  r3) and ...

        # this direction is very easy, as we can just let each resource
        # be equal to the functionality

        f = query.functionality
        min_res = (f,) * len(dp.R.subs)

        us = dp.R.largest_upperset_above(min_res)
        return Interval.degenerate(us)

    def solve_dp_FixResMaxFun_MeetNDualDP(
        self, dp: MeetNDualDP[X], query: FixResMaxFunQuery[X]
    ) -> Interval[LowerSet[tuple[X, ...]]]:
        raise NotImplementedError

    # exercise: join

    def solve_dp_FixFunMinRes_JoinNDP(
        self, dp: JoinNDP[X], query: FixFunMinResQuery[tuple[X, ...]]
    ) -> Interval[UpperSet[X]]:
        # this is a relation of the type
        #  (f1 ≤  r) and (f2 ≤ r) and (f3 ≤ r) and ...

        # similar to above

        f = query.functionality
        min_r: Optional[X] = dp.opspace.join(f)
        if min_r is None:
            raise NotImplementedError("TODO: join")
        us: UpperSet[X] = dp.R.largest_upperset_above(min_r)
        return Interval.degenerate(us)

    def solve_dp_FixResMaxFun_JoinNDP(
        self, dp: JoinNDP[X], query: FixResMaxFunQuery[X]
    ) -> Interval[LowerSet[tuple[X, ...]]]:
        raise NotImplementedError

    # The above are sufficient for lib1
    #
    #
    #
    #

    # The following are only for lib2.
    #
    #

    def solve_dp_FixResMaxFun_M_Res_DivideConstant_DP(
        self, dp: M_Res_DivideConstant_DP, query: FixResMaxFunQuery[Decimal]
    ) -> Interval[LowerSet[Decimal]]:
        # f/c <= r

        # Similar to a case above
        raise NotImplementedError

    def solve_dp_FixFunMinRes_M_Res_DivideConstant_DP(
        self, dp: M_Res_DivideConstant_DP, query: FixFunMinResQuery[Decimal]
    ) -> Interval[UpperSet[Decimal]]:
        # f/c <= r

        # Similar to a case above
        raise NotImplementedError

    # Exercise: parallel interconnection

    def solve_dp_FixFunMinRes_ParallelDP(
        self, dp: ParallelDP[FT, RT], query: FixFunMinResQuery[tuple[FT, ...]]
    ) -> Interval[UpperSet[tuple[RT, ...]]]:
        # This is the parallel composition of a sequence of DPs.

        f = query.functionality

        # F and R are PosetProducts
        F: PosetProduct[FT] = dp.F
        R: PosetProduct[RT] = dp.R

        # and f is a tuple of functionalities
        assert isinstance(f, tuple), f
        # ... of the same length as the number of DPs
        assert len(f) == len(dp.subs), (f, F)

        # You should decompose f into its components, and then solve each DP.
        # Then you need to take the *product* of the solutions.
        # The product of upper sets is the upper set of the cartesian product
        # and it is implemented as UpperSet.product().

        raise NotImplementedError

    def solve_dp_FixResMaxFun_ParallelDP(
        self, dp: ParallelDP[FT, RT], query: FixResMaxFunQuery[tuple[RT, ...]]
    ) -> Interval[LowerSet[FT]]:
        # Hint: same as above, swapping functionalities and resources

        # You will need to use LowerSet.product()
        raise NotImplementedError

    # exercise (advanced): loops!

    def solve_dp_FixFunMinRes_DPLoop2(
        self, dp: DPLoop2[F1, R1, object], query: FixFunMinResQuery[F1]
    ) -> Interval[UpperSet[R1]]:
        # Note: this is an advanced exercise.

        # As in the book, the intermediate goal is to define a function f such that
        # the solution is the least fixed point of f.

        raise NotImplementedError

    def solve_dp_FixResMaxFun_DPLoop2(
        self, dp: DPLoop2[F1, R1, object], query: FixResMaxFunQuery[R1]
    ) -> Interval[LowerSet[F1]]:
        # Note: this is an advanced exercise.

        # Hint: same as above, but go the other way...
        raise NotImplementedError

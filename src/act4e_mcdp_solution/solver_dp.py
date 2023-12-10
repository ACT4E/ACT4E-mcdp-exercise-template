from decimal import Decimal
from typing import TypeVar

from act4e_mcdp import *

__all__ = [
    "DPSolver",
]

from act4e_mcdp.solution_interface import FixFunMinResQuery
from act4e_mcdp.utils import rich_format

X = TypeVar("X")
FT = TypeVar("FT")
RT = TypeVar("RT")
F1 = TypeVar("F1")
R1 = TypeVar("R1")
M = TypeVar("M")

lib2 = True


class DPSolver(DPSolverInterface):
    def solve_dp_FixFunMinRes_CatalogueDP(
        self, dp: CatalogueDP[FT, RT], query: FixFunMinResQuery[FT]
    ) -> Interval[UpperSet[RT]]:
        f = query.functionality
        F = dp.F

        res: list[RT] = []
        for name, entry_info in dp.entries.items():
            if F.leq(f, entry_info.f_max):
                res.append(entry_info.r_min)

        return Interval.degenerate(UpperSet.from_points(dp.R, res))

    def solve_dp_FixResMaxFun_CatalogueDP(
        self, dp: CatalogueDP[FT, RT], query: FixResMaxFunQuery[RT]
    ) -> Interval[LowerSet[object]]:
        r = query.resources
        R = dp.R

        res = []
        for name, entry_info in dp.entries.items():
            if R.leq(entry_info.r_min, r):
                res.append(entry_info.f_max)

        return Interval.degenerate(LowerSet.from_points(dp.F, res))

    def solve_dp_FixResMaxFun_Limit(self, dp: Limit, query: FixResMaxFunQuery) -> Interval[LowerSet[object]]:
        # f <= 42
        assert query.resources == (), query
        v = dp.c.value
        return Interval.degenerate(LowerSet.principal(v))

    def solve_dp_FixFunMinRes_Limit(self, dp: Limit, query: FixFunMinResQuery) -> Interval[UpperSet[object]]:
        F = dp.F
        # f <= 42

        if F.leq(query.functionality, dp.c.value):
            # the functionalities are the empty tuple
            min_r = ()
            return Interval.degenerate(UpperSet.principal(min_r))
        else:
            # the given budget is not enough

            return Interval.degenerate(UpperSet.empty())

    def solve_dp_FixFunMinRes_M_FloorFun_DP(
        self, dp: M_FloorFun_DP, query: FixFunMinResQuery
    ) -> Interval[UpperSet[object]]:
        # This is dual to M_Ceil_DP
        # f <= floor(r)
        # Now r is fixed
        f = query.functionality
        assert isinstance(f, Decimal), f

        R: Numbers = dp.R
        F: Numbers = dp.F

        if f.is_infinite():
            min_r = f
        else:
            # example: f = 2.4

            # f <= floor(r)

            min_r = Decimal(f.__ceil__())  # FIXME

        us = R.largest_upperset_above(min_r)
        return Interval.degenerate(us)

    def solve_dp_FixResMaxFun_M_FloorFun_DP(
        self, dp: M_FloorFun_DP, query: FixResMaxFunQuery
    ) -> Interval[LowerSet[object]]:
        # This is dual to M_Ceil_DP
        # f <= floor(r)
        # Now r is fixed
        r = query.resources
        assert isinstance(r, Decimal), r

        F: Numbers = dp.F

        if r.is_infinite():
            max_f = r
        else:
            max_f = Decimal(r.__floor__())

        ls = F.largest_lowerset_below(max_f)
        return Interval.degenerate(ls)

    def solve_dp_FixFunMinRes_M_Fun_AddConstant_DP(
        self, dp: M_Fun_AddConstant_DP, query: FixFunMinResQuery
    ) -> Interval[UpperSet[object]]:
        # f <= r + constant
        f = query.functionality
        assert isinstance(f, Decimal), f
        min_r = f - dp.vu.value
        us = dp.R.largest_upperset_above(min_r)
        return Interval.degenerate(us)

    def solve_dp_FixResMaxFun_M_Fun_AddConstant_DP(
        self, dp: M_Fun_AddConstant_DP, query: FixResMaxFunQuery
    ) -> Interval[LowerSet[object]]:
        r = query.resources
        assert isinstance(r, Decimal), r
        max_f = r + dp.vu.value
        ls = dp.F.largest_lowerset_below(max_f)
        return Interval.degenerate(ls)

    def solve_dp_FixResMaxFun_M_Res_MultiplyConstant_DP(
        self, dp: M_Res_MultiplyConstant_DP, query: FixResMaxFunQuery
    ) -> Interval[LowerSet[object]]:
        r = query.resources
        assert isinstance(r, Decimal)
        max_f = r / dp.vu.value

        ls = dp.F.largest_lowerset_below(max_f)
        return Interval.degenerate(ls)

    #
    def solve_dp_FixFunMinRes_M_Fun_MultiplyConstant_DP(
        self, dp: M_Fun_MultiplyConstant_DP, query: FixFunMinResQuery
    ) -> Interval[UpperSet[object]]:
        #  (f * constant <= r)

        # This is similar to the M_Res_AddConstant_DP case above with
        # multiplication instead of addition.

        f = query.functionality
        assert isinstance(f, Decimal)
        min_r = f / dp.vu.value

        # one last detail: we need to make sure that the resource is valid
        # for the R poset. We use the largest_upperset_above() function in Numbers.
        # See documentation there.
        us = dp.R.largest_upperset_above(min_r)

        return Interval.degenerate(us)

    def solve_dp_FixResMaxFun_M_Fun_MultiplyConstant_DP(
        self, dp: M_Fun_MultiplyConstant_DP, query: FixResMaxFunQuery
    ) -> Interval[LowerSet[object]]:
        r = query.resources
        assert isinstance(r, Decimal)
        max_f = r * dp.vu.value

        ls = dp.F.largest_lowerset_below(max_f)
        return Interval.degenerate(ls)

    # series
    def solve_dp_FixFunMinRes_DPSeries(
        self, dp: DPSeries, query: FixFunMinResQuery[object]
    ) -> Interval[UpperSet[object]]:
        optimistic = UpperSet.principal(query.functionality)
        pessimistic = UpperSet.principal(query.functionality)

        for dp in dp.subs:
            query_us_opt = FixFunMinResQuery(
                functionality=optimistic,
                resolution_optimistic=query.resolution_optimistic,
                resolution_pessimistic=query.resolution_pessimistic,
            )
            res_opt = self._solve_dp_FixFunMinRes_upperset(dp, query_us_opt)
            optimistic = res_opt.optimistic

            query_us_pess = FixFunMinResQuery(
                functionality=pessimistic,
                resolution_optimistic=query.resolution_optimistic,
                resolution_pessimistic=query.resolution_pessimistic,
            )
            res_pes = self._solve_dp_FixFunMinRes_upperset(dp, query_us_pess)
            pessimistic = res_pes.pessimistic

        return Interval(optimistic=optimistic, pessimistic=pessimistic)

    def solve_dp_FixResMaxFun_DPSeries(
        self, dp: DPSeries, query: FixResMaxFunQuery[object]
    ) -> Interval[LowerSet[object]]:
        optimistic = LowerSet.principal(query.resources)
        pessimistic = LowerSet.principal(query.resources)

        for dp in reversed(dp.subs):
            query_us_opt = FixResMaxFunQuery(
                resources=optimistic,
                resolution_optimistic=query.resolution_optimistic,
                resolution_pessimistic=query.resolution_pessimistic,
            )
            res_opt = self._solve_dp_FixResMaxFun_lowerset(dp, query_us_opt)
            optimistic = res_opt.optimistic

            query_us_pess = FixResMaxFunQuery(
                resources=pessimistic,
                resolution_optimistic=query.resolution_optimistic,
                resolution_pessimistic=query.resolution_pessimistic,
            )
            res_pes = self._solve_dp_FixResMaxFun_lowerset(dp, query_us_pess)
            pessimistic = res_pes.pessimistic

        return Interval(optimistic=optimistic, pessimistic=pessimistic)

    def _solve_dp_FixFunMinRes_upperset(
        self, dp: PrimitiveDP[FT, RT], query: FixFunMinResQuery[UpperSet[FT]]
    ) -> Interval[UpperSet[RT]]:
        fs = query.functionality
        assert isinstance(fs, UpperSet), fs

        uppersets_optimistic = []
        uppersets_pessimistic = []

        for f in fs.minimals:
            if not dp.F.belongs(f):
                raise Exception(f"Functionality {f} not in {dp.F}")

            query_f = FixFunMinResQuery(
                functionality=f,
                resolution_optimistic=query.resolution_optimistic,
                resolution_pessimistic=query.resolution_pessimistic,
            )
            res = self.solve_dp_FixFunMinRes(dp, query_f)

            uppersets_optimistic.append(res.optimistic)
            uppersets_pessimistic.append(res.pessimistic)

        optimistic = UpperSet.union(uppersets_optimistic, dp.R)
        pessimistic = UpperSet.union(uppersets_pessimistic, dp.R)
        return Interval(optimistic=optimistic, pessimistic=pessimistic)

    def _solve_dp_FixResMaxFun_lowerset(
        self, dp: PrimitiveDP[FT, RT], query: FixResMaxFunQuery[LowerSet[RT]]
    ) -> Interval[LowerSet[FT]]:
        fs = query.resources
        assert isinstance(fs, LowerSet), fs

        uppersets_optimistic = []
        uppersets_pessimistic = []

        for r in fs.maximals:
            if not dp.R.belongs(r):
                raise Exception(f"Resource {r} not in {dp.R}")

            query_f = FixResMaxFunQuery(
                resources=r,
                resolution_optimistic=query.resolution_optimistic,
                resolution_pessimistic=query.resolution_pessimistic,
            )
            res = self.solve_dp_FixResMaxFun(dp, query_f)

            uppersets_optimistic.append(res.optimistic)
            uppersets_pessimistic.append(res.pessimistic)

        optimistic = LowerSet.union(uppersets_optimistic, dp.R)
        pessimistic = LowerSet.union(uppersets_pessimistic, dp.R)
        return Interval(optimistic=optimistic, pessimistic=pessimistic)

    def solve_dp_FixFunMinRes_JoinNDP(
        self, dp: JoinNDP[X], query: FixFunMinResQuery[tuple[X, ...]]
    ) -> Interval[UpperSet[X]]:
        # this is a relation of the type
        #  (f1 ≤  r) and (f2 ≤ r) and (f3 ≤ r) and ...

        f = query.functionality
        min_r = dp.opspace.join(f)
        us = dp.R.largest_upperset_above(min_r)
        return Interval.degenerate(us)

    def solve_dp_FixResMaxFun_MeetNDualDP(
        self, dp: MeetNDualDP[X], query: FixResMaxFunQuery[X]
    ) -> Interval[LowerSet[tuple[X, ...]]]:
        r = query.resources
        max_f = dp.opspace.meet(r)
        ls = dp.F.largest_lowerset_below(max_f)
        return Interval.degenerate(ls)

    def solve_dp_FixFunMinRes_M_Res_MultiplyMany_DP(
        self, dp: M_Res_MultiplyMany_DP, query: FixFunMinResQuery[tuple[Decimal, ...]]
    ) -> Interval[UpperSet[Decimal]]:
        res = Decimal(1)
        for fi in query.functionality:
            res *= fi

        us = dp.R.largest_upperset_above(res)
        return Interval.degenerate(us)

    def solve_dp_FixResMaxFun_M_Fun_AddMany_DP(
        self, dp: M_Fun_AddMany_DP, query: FixResMaxFunQuery[tuple[Decimal, ...]]
    ) -> Interval[LowerSet[Decimal]]:
        r = query.resources

        res = r[0]
        for fi in r[1:]:
            res += fi

        fs = dp.F.largest_lowerset_below(res)
        return Interval.degenerate(fs)

    def solve_dp_FixResMaxFun_JoinNDP(
        self, dp: JoinNDP[X], query: FixResMaxFunQuery[X]
    ) -> Interval[LowerSet[tuple[X, ...]]]:
        r = query.resources
        max_f = (r,) * len(dp.F.subs)

        us = dp.F.largest_lowerset_below(max_f)
        return Interval.degenerate(us)

    # End of lib1

    if lib2:

        def solve_dp_FixFunMinRes_ParallelDP(
            self, dp: ParallelDP, query: FixFunMinResQuery
        ) -> Interval[UpperSet[object]]:
            # This is the parallel composition of a sequence of DPs.

            f = query.functionality

            # F and R are PosetProducts
            F: PosetProduct = dp.F
            R: PosetProduct = dp.R

            # and f is a tuple of functionalities
            assert isinstance(f, tuple), f
            # ... of the same length as the number of DPs
            assert len(f) == len(dp.subs), (f, F)

            optimistic: list[UpperSet] = []
            pessimistic: list[UpperSet] = []

            for i, (f_i, F_i) in enumerate(zip(f, dp.subs)):
                q_i = FixFunMinResQuery(
                    functionality=f_i,
                    resolution_optimistic=query.resolution_optimistic,
                    resolution_pessimistic=query.resolution_pessimistic,
                )
                res = self.solve_dp_FixFunMinRes(F_i, q_i)
                optimistic.append(res.optimistic)
                pessimistic.append(res.pessimistic)

            optimistic = UpperSet.product(optimistic)
            pessimistic = UpperSet.product(pessimistic)
            return Interval(optimistic=optimistic, pessimistic=pessimistic)

        def solve_dp_FixResMaxFun_ParallelDP(
            self, dp: ParallelDP, query: FixResMaxFunQuery
        ) -> Interval[LowerSet[object]]:
            r = query.resources
            assert isinstance(r, tuple), r
            # F and R are PosetProducts
            F: PosetProduct = dp.F
            R: PosetProduct = dp.R

            optimistic: list[LowerSet] = []
            pessimistic: list[LowerSet] = []
            for i, (r_i, R_i) in enumerate(zip(r, dp.subs)):
                q_i = FixResMaxFunQuery(
                    resources=r_i,
                    resolution_optimistic=query.resolution_optimistic,
                    resolution_pessimistic=query.resolution_pessimistic,
                )
                res = self.solve_dp_FixResMaxFun(R_i, q_i)
                optimistic.append(res.optimistic)
                pessimistic.append(res.pessimistic)

            optimistic = LowerSet.product(optimistic)
            pessimistic = LowerSet.product(pessimistic)
            return Interval(optimistic=optimistic, pessimistic=pessimistic)

        def solve_dp_FixFunMinRes_DPLoop2(
            self, dp: DPLoop2[F1, R1, M], query: FixFunMinResQuery[F1]
        ) -> Interval[UpperSet[R1]]:
            f1: F1 = query.functionality

            logger.info("f1: %s", f1)

            def m_opt(r: UpperSet[M]) -> UpperSet[tuple[R1, M]]:
                fu: UpperSet[F1] = UpperSet.principal(f1)
                V: UpperSet[tuple[F1, M]] = UpperSet.product([fu, r])  # tpye: ignore
                #
                # logger.info(rich_format(dp.dp))
                # logger.info(rich_format(V))
                res: Interval[UpperSet[tuple[R1, M]]]
                res = self._solve_dp_FixFunMinRes_upperset(
                    dp.dp,
                    FixFunMinResQuery(
                        functionality=V,
                        resolution_optimistic=query.resolution_optimistic,
                        resolution_pessimistic=query.resolution_pessimistic,
                    ),
                )
                return res.optimistic

            PM: Poset[M] = dp.dp.F.subs[1]  # type: ignore
            m0 = PM.global_minima()

            logger.info("m0: %s", m0)
            it = 0
            rs = None
            while True:
                logger.info("it: %s   m0 = %s", it, rich_format(m0))
                x = m_opt(m0)
                minima2 = [_[1] for _ in x.minimals]
                m0_new = UpperSet(minima2)
                if m0_new == m0:
                    rs = UpperSet([_[0] for _ in x.minimals])
                    break

                it += 1
                m0 = m0_new

            assert rs is not None

            return Interval.degenerate(rs)

            raise NotImplementedError

        def solve_dp_FixResMaxFun_DPLoop2(
            self, dp: DPLoop2[F1, R1, object], query: FixResMaxFunQuery[R1]
        ) -> Interval[LowerSet[F1]]:
            # Note: this is an advanced exercise.

            # Hint: same as above, but go the other way...

            r1: R1 = query.resources

            logger.info("r1: %s", r1)

            def m_opt(r: LowerSet[M]) -> LowerSet[tuple[F1, M]]:
                fu: LowerSet[R1] = LowerSet.principal(r1)
                V: LowerSet[tuple[R1, M]] = LowerSet.product([fu, r])  # tpye: ignore
                #
                # logger.info(rich_format(dp.dp))
                # logger.info(rich_format(V))
                res: Interval[LowerSet[tuple[F1, M]]]
                res = self._solve_dp_FixResMaxFun_lowerset(
                    dp.dp,
                    FixResMaxFunQuery(
                        resources=V,
                        resolution_optimistic=query.resolution_optimistic,
                        resolution_pessimistic=query.resolution_pessimistic,
                    ),
                )
                return res.optimistic

            PM: Poset[M] = dp.dp.F.subs[1]  # type: ignore
            m0 = PM.global_maxima()

            logger.info("m0: %s", m0)
            it = 0
            rs = None
            while True:
                logger.info("it: %s   m0 = %s", it, rich_format(m0))
                x = m_opt(m0)
                minima2 = [_[1] for _ in x.maximals]
                m0_new = LowerSet(minima2)
                if m0_new == m0:
                    rs = LowerSet([_[0] for _ in x.maximals])
                    break

                it += 1
                m0 = m0_new

            assert rs is not None

            return Interval.degenerate(rs)

        def solve_dp_FixFunMinRes_M_Res_DivideConstant_DP(
            self, dp: M_Res_DivideConstant_DP, query: FixFunMinResQuery[Decimal]
        ) -> Interval[UpperSet[Decimal]]:
            f = query.functionality
            c = dp.vu.value
            min_r = f / c
            us = dp.R.largest_upperset_above(min_r)
            return Interval.degenerate(us)

        def solve_dp_FixResMaxFun_M_Res_DivideConstant_DP(
            self, dp: M_Res_DivideConstant_DP, query: FixResMaxFunQuery[Decimal]
        ) -> Interval[LowerSet[Decimal]]:
            r = query.resources
            c = dp.vu.value
            max_f = r * c
            ls = dp.F.largest_lowerset_below(max_f)
            return Interval.degenerate(ls)

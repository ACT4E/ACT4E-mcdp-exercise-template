# ACT4EI, Fall 2023, DP exercise



## Repositories

There are 2 repositories to consider:

- **This repository** contains these instructions and **the solution template** to extend.
- The repository [ACT4E/ACT4E-mcdp](https://github.com/ACT4E/ACT4E-mcdp) contains: 

  1. the API (**data structures**, interfaces);
  2. the **test runner** that checks that your implementation is correct;
  3. the **test cases**.

Note that there are extensive docs available online at [act4e-mcdp.readthedocs.io](https://act4e-mcdp.readthedocs.io/en/latest/).
  
What you'll do is **clone this repository**, and just *install* the code from `ACT4E-mcdp` using `pip` (no need to clone that). 


## Overview of the exercise

The goal of this exercise is for you to build a DP queries solver.

There are various phases of difficulty progression (listed at the end of this document).

You will be given a DP represented using the data structures defined in `ACT4E-mcdp` along with a query.

You have to extend the code in this repository by implementing the `DPSolver` class.

These are the main entrypoints of the `DPSolver` class:

```python
from act4e_mcdp import DPSolverInterface, Interval, LowerSet, PrimitiveDP, UpperSet

class DPSolver(DPSolverInterface):
     def solve_dp_FixFunMinRes(
        self,
        dp: PrimitiveDP[FT, RT],
        query: FixFunMinResQuery[FT],
        /,
    ) -> Interval[UpperSet[RT]]:
         ...

   def solve_dp_FixResMaxFun(
        self,
        dp: PrimitiveDP[FT, RT],
        query: FixResMaxFunQuery[RT],
    ) -> Interval[LowerSet[FT]]:
        ...
```

The two methods `solve_dp_FixFunMinRes` and `solve_dp_FixResMaxFun` correspond to the two queries studied in class
(also documented [here](https://act4e-mcdp.readthedocs.io/en/latest/API/API_solution/#act4e_mcdp.solution_interface.DPSolverInterface)).

The input `dp` represents the DP in consideration. There is a hierarchy of DPs available ([documented here][here]).
These includes the one that appeared in class or in the book (identity, addition, multiplication, splitters, etc.).

[here]: https://act4e-mcdp.readthedocs.io/en/latest/API/primitivedps/00_index/

The `query` parameter gives the parameters for the computation:

- `FixFunMinResQuery` has the field `functionality` of type `FT` (the functionality to be provided).
- `FixResMaxFunQuery` has the field `resources` of type `RT` (the resource budget).

In addition, there are two more fields: `resolution_optimistic` and `resolution_pessimistic`. These are used in the case the DP is not finitely computable and needs an approximated solution. In that case, your code would be called with increasing values of the resolutions and the expectation is that the interval becomes tighther and tighther.  (You can ignore these fields for now.)

For these exercises we have [3 types of posets](https://act4e-mcdp.readthedocs.io/en/latest/API/posets/):

1. `FinitePoset`: finite posets, with strings as elements
2. `Numbers`: with Python `Decimal` as elements.
3. `PosetProduct`, whose elements are *tuples* (`(a, b, c)`) of elements of its subposets. 

The posets are already implemented in `ACT4E-mcdp` and you can use them directly. They have useful methods such as `leq()` and `meet()`, `minimals()`, `join()`, `maximals()`.

The return value is an `Interval` of upper / lower sets. The two extreama of the interval represent optimistic and pessimistic solutions. 

### What you have to implement 

What you have to implement are the methods called `solve_dp_FixFunMinRes_DPTYPE` and `solve_dp_FixResMaxFun_DPTYPE`.
You have to implement these methods for each type of DP available.

There are already some completed methods in the template solution, as well as hints for many of the methods.

For example, this is the skeleton for implementing `IdentityDP`:

```python
    def solve_dp_FixFunMinRes_IdentityDP(
        self, _: IdentityDP[X], query: FixFunMinResQuery[X]
    ) -> Interval[UpperSet[X]]:
        f = query.functionality
        min_r = f # Easy: the minimal resources are the functionality itself
        min_resources = UpperSet.principal(min_r)

        # We need to return an interval of upper sets. It is a degenerate interval
        return Interval.degenerate(min_resources)

    def solve_dp_FixResMaxFun_IdentityDP(
        self, _: IdentityDP[X], query: FixResMaxFunQuery[X]
    ) -> Interval[LowerSet[X]]:
        # same as above, but we return lower sets
        r = query.resources
        max_f = r # the maximum functionality is the resource budget
        max_functionalities = LowerSet.principal(max_f)
        return Interval.degenerate(max_functionalities)
```



### Workflow

This is the suggested workflow:

1. Setup everything as described in the next section.
2. Run the test runner and observe the errors.
3. Select one error and work on that. This usually means adding support for a new type of DP.
4. repeat from 2

## Turning in the exercise

You can either email us a `.zip` file, or (better), create a **private** repository and gives us access.

We ask you that **you do not make your code public**.


-----

# Setup the development environment

This walkthrough makes you setup the development environment on VS Code in a docker container. 
It works everywhere including Windows and it does not assume much about your system.

If you know what you are doing, you could also (at your responsibility and without our support) use a native editor and Python environment.

## Install Docker

Install Docker:

* (Mac, Linux) Follow the [installation instructions](https://docs.docker.com/get-docker/)
* (Windows): Follow the manual installation steps for Windows Subsystem for Linux [here](https://docs.microsoft.com/en-us/windows/wsl/install). On
  step 1, follow the recommendation of updating to WSL 2. You do not necessarily need to install Windows Terminal. Now
  go [here](https://docs.docker.com/desktop/windows/install/) and follow the "Install Docker Desktop on Windows" instructions. You can then start
  Docker Desktop and follow the quick start quide.

## Install VS Code

Install VS Code [using the instructions online](https://code.visualstudio.com/download).

## Open the folder in VS Code using "Dev Container."

Select File -> Open and select *the entire folder*.

VS Code will propose to install "Dev Container." Click "install".

VS Code will give you a message similar to:

> Folder contains a Dev Container configuration file. Reopen folder to develop in a container.

Select "Reopen in container".

Now you should have the folder open while VS Code is in "container development mode".

You can create a new terminal using Terminal -> New Terminal.

## Install dependencies

In a terminal (inside the container), install this package and dependencies using:

    pip install -e .

The main dependency installed is `ACT4E-mcdp` which is available [on this repo](https://github.com/ACT4E/ACT4E-mcdp).
That library takes care of parsing the models and queries.
Please refer to the [online documentation](https://act4e-mcdp.readthedocs.io/en/latest/) for more information.

If we tell you to update the library, use this:

    pip install -U ACT4E-mcdp

## Make sure everything runs fine with the template solution

### Download and run the test cases

Use this command to download the test cases:

    act4e-mcdp-download-tests --out downloaded

Then you have available a few test cases in the directory `downloaded/`.

These are divided in "libraries" of varying complexity:

* `lib1-parts`: very simple test cases, with only one primitive DP per file;
* `lib2-simple`: simple test cases, with a few primitive DPs per file.
* `lib3-advanced`: more complex test cases (**not included for Fall 2023**).


`act4e-mcdp-solve-dp-queries` is the command you use to run the DP solver.

For example, you can run the solver on the test cases in `lib1-parts` using:

    act4e-mcdp-solve-dp-queries --solver act4e_mcdp_solution.DPSolver downloaded/lib1-parts


The parameters are:
* `--solver act4e_mcdp_solution.DPSolver`: this selects the class for your solver.
* `downloaded/lib1-parts`: this selects the directory with the test cases to use;
 

In the file `output_summary.yaml` you will find details of the results.

For example, one of the results could be:

```yaml
downloaded/lib1-simple.dp-queries.FixResMaxFun.all_together-0011.mcdpr1.yaml:
  query: FixResMaxFun
  value: Decimal('Infinity')
  result_expected: Interval(pessimistic=LowerSet(maximals=[Decimal('Infinity')]),
    optimistic=LowerSet(maximals=[Decimal('Infinity')]))
  result_obtained: Interval(pessimistic=LowerSet(maximals=[]), optimistic=LowerSet(maximals=[]))
  status: failed

```

This indicated the type of query (`FixResMaxFun`), the value of the query (`Decimal('Infinity')`), the expected result (`result_expected`) and the
obtained result (`result_obtained`).
This particular test case failed because the obtained result is empty ("infeasible"), while the expected result is not empty.

# ACT4E exercises progression

There are 3 phases of increasing difficulty.

Phase 1 and 2 are approachable, and were designed to be the graded part.

Phases 3 is challenging, and require some extra effort, and were always thought as optional.

## Phase 1: solve simple DP queries for each component

In this first phase, you will implement the queries for each type of DP in isolation
and the series composition.

The following command must run successfully:

    act4e-mcdp-solve-dp-queries  --solver act4e_mcdp_solution.DPSolver downloaded/lib1-parts

## Phase 2: solve DP queries with multiple DPs (series, parallel, loop) 

In this phase, you will implement the queries for *composition of DPs* joined by parallel, loop constructions.

The following command must run successfully:

    act4e-mcdp-solve-dp-queries  --solver act4e_mcdp_solution.DPSolver downloaded/lib2-simple




## Phase 3: solve advanced queries (excluded for Fall 2023)

These are advanced queries that require a nontrivial implementation to solve efficiently.

    act4e-mcdp-solve-dp-queries   -d downloaded/lib3-advanced --solver act4e_mcdp_solution.DPSolver
    
# Extra information 

Please see the file [extra_info.md](extra_info.md) for more optional information about the data structures and the queries.

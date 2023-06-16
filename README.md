# ACT4EI, Spring 2023, DP exercise

Note: for Spring 2023 this exercise is **optional** -- it is very interesting to do, but we do not feel we have play-tested it enough for it to be a graded exercise. 



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

The goal of this exercise is for you to build a DP and MCDP queries solver.

There are various phases of difficulty progression (listed at the end of this document).

You will be given a DP represented using the data structures defined in `ACT4E-mcdp` along with a query.

You have to extend the code in this repository by implementing the `DPSolver` and `MCDPSolver` classes.

For example, this is the interface of the `DPSolver` class:

```python
from act4e_mcdp import DPSolverInterface, Interval, LowerSet, PrimitiveDP, UpperSet

class DPSolver(DPSolverInterface):
    def solve_dp_FixFunMinRes(
        self,
        dp: PrimitiveDP,
        functionality_needed: object,
        /,
        resolution_optimistic: int = 0,
        resolution_pessimistic: int = 0,
    ) -> Interval[UpperSet[object]]:
         # just a template -- return infeasibility!
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
    
        # just a template -- return infeasibility!
        optimistic = pessimistic = LowerSet([])
        return Interval(pessimistic=pessimistic, optimistic=optimistic)
```

The two methods `solve_dp_FixFunMinRes` and `solve_dp_FixResMaxFun` correspond to the two queries studied in class
(also documented [here](https://act4e-mcdp.readthedocs.io/en/latest/API/API_solution/#act4e_mcdp.solution_interface.DPSolverInterface)).

The input `dp` represents the DP in consideration. There is a hierarchy of DPs available ([documented here][here]).
These includes the one that appeared in class or in the book (identity, addition, multiplication, splitters, etc.).

[here]: https://act4e-mcdp.readthedocs.io/en/latest/API/primitivedps/00_index/

The inputs (`functionality_needed` and `resource_budget`) are elements of the poset `F` or  `R` for the DPs. 
For these exercises we have [3 types of posets](https://act4e-mcdp.readthedocs.io/en/latest/API/posets/):

1. `FinitePoset`: finite posets, with strings as elements
2. `Numbers`: with Python `Decimal` as elements.
3. `PosetProduct`, whose elements are *tuples* (`(a, b, c)`) of elements of its subposets. 

The return value is an `Interval` of upper / lower sets. The two extram of the interval represent optimistic and pessimistic solutions. 

The template code above returns empty upper / lower sets, which means that the solution is not feasible.

The parameters `resolution_optimistic` and `resolution_pessimistic` are needed in the case the DP is not finitely computable and needs an approximated solution. In that case, your code would be called with increasing values of the resolutions and the expectation is that the interval becomes tighther and tighther.

### Workflow

This is the suggested workflow:

1. Setup everything as described in the next section.
2. Run the test runner and observe the errors.
3. Select one error and work on that. This usually means adding support for a new type of DP or poset.
4. repeat from 2

**Note**: the `ACT4E-mcdp` package only contains the data structures to describe the problems. It does not contain the actual "code"! For example, the `PosetProduct` class available has a member `subs` that contains the subposets. However, there is no `leq()` or `meet()` method implemented.




## Turning in the exercise

You can either email us a `.zip` file, or (better), create a **private** repository and gives us access.

We ask you that **you do not make your code public**.


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

### Download test cases

Use this command to download the test cases:

    act4e-mcdp-download-tests --out downloaded

Then you have available a few test cases in the directory `downloaded/`.

These are divided in "libraries" of varying complexity:

* `lib1-parts`: very simple test cases, with only one primitive DP per file;
* `lib2-simple`: simple test cases, with a few primitive DPs per file.
* `lib3-advanced`: more complex test cases, with many primitive DPs per file.

### Running the DP solver for a specific model and query

`act4e-mcdp-solve-dp` is the command you use to run the DP solver 
for a particular model and query:

    act4e-mcdp-solve-dp \
        --solver act4e_mcdp_solution.DPSolver \
        --query FixFunMinRes \
        --model downloaded/lib1-parts/lib1-parts.primitivedps.e03_splitter1.mcdpr1.yaml \
        --data '10'

In brief:

* `--solver act4e_mcdp_solution.DPSolver`: this selects the class for your solver;
* `--query FixFunMinRes`: this selects `FixFunMinRes` (other choice: `FixResMaxFun`);
* `--model downloaded/lib1-parts/lib1-parts.primitivedps.e03_splitter1.mcdpr1.yaml`: this selects the model to use for optimization;
* `--data '10'`: this selects the query to give.

You will see the result in the logs:

```
INFO query: 10
INFO solution: Interval(pessimistic=UpperSet(minima=[]), optimistic=UpperSet(minima=[]))
```

The template `act4e_mcdp_solution.MySolution` always returns an empty `UpperSet` (= infeasible).

### Running the DP solver on a set of test cases

`act4e-mcdp-solve-dp-queries` is the command you use to run the DP solver on a set of test cases:

    act4e-mcdp-solve-dp-queries \
        -d downloaded/lib1-parts/ \
        --solver act4e_mcdp_solution.DPSolver

In brief:

* `-d downloaded`: this selects the directory with the test cases to use;
* `--solver act4e_mcdp_solution.DPSolver`: this selects the class for your solver.

At the end of the processing, you will see an output similar to this:

```
Summary:

comparison_not_implemented:
- downloaded/lib1-parts/lib1-parts.dp-queries.FixFunMinRes.e10_conversions2-0006.mcdpr1.yaml
- downloaded/lib1-parts/lib1-parts.dp-queries.FixResMaxFun.e05_sumf-0002.mcdpr1.yaml
...
failed:
- downloaded/lib1-parts/lib1-parts.dp-queries.FixResMaxFun.e03_splitter1-0006.mcdpr1.yaml
- downloaded/lib1-parts/lib1-parts.dp-queries.FixFunMinRes.e12_catalogue_true-0010.mcdpr1.yaml
... 
succeeded:
- downloaded/lib1-parts/lib1-parts.dp-queries.FixResMaxFun.e12_catalogue_empty-0001.mcdpr1.yaml
- downloaded/lib1-parts/lib1-parts.dp-queries.FixFunMinRes.e12_catalogue-0001.mcdpr1.yaml
...
INFO Find the summary at 'output_summary.yaml'
```

For each query, the result is either `succeeded` or `failed`. (The status `comparison_not_implemented` means that we didn't implement yet
the comparison between the result and the expected result.)

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

### Running the MCDP solver

This is the command you use to run the MCDP solver:

    act4e-mcdp-solve-mcdp \
        --solver act4e_mcdp_solution.MCDPSolver \
        --query FixFunMinRes \
        --model downloaded/lib1-parts.models.e03_splitter1.mcdpr1.yaml \
        --data '{f: 42}'

Note that for the MCDP solver we give a file of type `models.mcdpr1.yaml` instead of `primitivedps.mcdpr1.yaml`.

For the data, we use a key-value pair with the functionality name and the value.

You should see the output:

    query: {'f': Decimal('42')}
    solution: Interval(pessimistic=UpperSet(minima=[]), optimistic=UpperSet(minima=[]))

## Running the MCDP solver on a set of test cases

TODO: finish this part

---

# ACT4E exercises progression

There are 4 phases of increasing difficulty.

Phase 1 and 2 are approachable, and were designed to be the graded part.

Phases 3 and 4 are more challenging, and require some extra effort, and were always thought as optional.

## Phase 1: solve simple DP queries for each component

In this first phase, you will implement the queries for each type of DP in isolation.

The following query must run successfully:

    act4e-mcdp-solve-dp-queries -d downloaded/lib1-parts  --solver act4e_mcdp_solution.DPSolver

## Phase 2: solve DP queries with multiple DPs (series, parallel, loop) 

In this phase, you will implement the queries for *composition of DPs* joined by series, parallel, loop constructions.

The following query must run successfully:

    act4e-mcdp-solve-dp-queries -d downloaded/lib2-simple --solver act4e_mcdp_solution.DPSolver

## Phase 3: solve MCDP queries (*)

In this phase, you are given only the graph. You then need to convert the graph into a DP. 

To do this, you might need some experience or strong intuition about manipulating graphs.

The following should work successfully:

    act4e-mcdp-solve-mcdp-queries -d downloaded/lib1-parts  --solver act4e_mcdp_solution.MCDPSolver
    act4e-mcdp-solve-mcdp-queries -d downloaded/lib2-simple --solver act4e_mcdp_solution.MCDPSolver

## Phase 4: solve advanced queries (*)

These are advanced queries that require a nontrivial implementation to solve efficiently.

    act4e-mcdp-solve-dp-queries   -d downloaded/lib3-advanced   --solver act4e_mcdp_solution.DPSolver
    act4e-mcdp-solve-mcdp-queries -d downloaded/lib3-advanced --solver act4e_mcdp_solution.MCDPSolver




# Creating more test cases

The models are created using [this online environment][IDE] - very experimental!

[IDE]: https://editor.zuper.ai/editor/gh/co-design-models/ACT4E-exercises-spring2023/main/view/

If you make an account you can play around. You can obtain the YAML file read by `ACT4E-mcdp` by selecting the "DP compiled YAML representation" option from the drop down menu. Some of the other visualizations might also be helpful.

[Example: drone model](https://editor.zuper.ai/editor/gh/co-design-models/ACT4E-exercises-spring2023/main/view/libraries/lib2-simple/specs/models/things/drone1/)

 <img width="1113" alt="mcdpdrone" src="https://github.com/ACT4E/ACT4E-mcdp-exercise-template/assets/81052/b2e3c9ec-c55c-49c8-9e0c-071c02fb03c0">



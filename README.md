# ACT4EI, Spring 2023, DP exercise

Note: this code exercise is **optional** -- it is very interesting to do, but we do not feel we have play-tested it enough for it to be a graded exercise. 

## Overview

There are 2 repositories to consider:

- This repository contains these instructions and the solution template.
- The repository [ACT4E/ACT4E-mcdp-exercise](https://github.com/ACT4E/ACT4E-mcdp-exercise) contains the test runner and the data structures to use.
  Note that there are extensive docs available online. 


# Setup

## Install required software

Install Docker:

* (Mac, Linux) Follow the [installation instructions](https://docs.docker.com/get-docker/)
* (Windows): Follow the manual installation steps for Windows Subsystem for Linux [here](https://docs.microsoft.com/en-us/windows/wsl/install). On
  step 1, follow the recommendation of updating to WSL 2. You do not necessarily need to install Windows Terminal. Now
  go [here](https://docs.docker.com/desktop/windows/install/) and follow the "Install Docker Desktop on Windows" instructions. You can then start
  Docker Desktop and follow the quick start quide.

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

Install this package and dependencies using:

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

## Phase 1: solve simple DP queries for each component

In this first phase, you will implement the queries for each type of DP in isolation.

The following query must run successfully:

    act4e-mcdp-solve-dp-queries -d downloaded/lib1-parts  --solver act4e_mcdp_solution.DPSolver

## Phase 2: solve DP queries with multiple DPs (series, parallel, loop) 

In this phase, you will implement the queries for *composition of DPs* joined by series, parallel, loop constructions.

The following query must run successfully:

    act4e-mcdp-solve-dp-queries -d downloaded/lib2-simple --solver act4e_mcdp_solution.DPSolver

## Phase 3: solve MCDP queries

In this phase, you are given only the graph. You then need to convert the graph into a DP. 

To do this, you might need some experience or strong intuition about manipulating graphs.

The following should work successfully:

    act4e-mcdp-solve-mcdp-queries -d downloaded/lib1-parts  --solver act4e_mcdp_solution.MCDPSolver
    act4e-mcdp-solve-mcdp-queries -d downloaded/lib2-simple --solver act4e_mcdp_solution.MCDPSolver

## Phase 4: solve advanced queries

These are advanced queries that require a nontrivial implementation to solve efficiently.

    act4e-mcdp-solve-dp-queries   -d downloaded/lib3-advanced   --solver act4e_mcdp_solution.DPSolver
    act4e-mcdp-solve-mcdp-queries -d downloaded/lib3-advanced --solver act4e_mcdp_solution.MCDPSolver

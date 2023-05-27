# Setup

## Install required software

Install Docker:

* (Mac, Linux) Follow the [installation instructions](https://docs.docker.com/get-docker/)
* (Windows): Follow the manual installation steps for Windows Subsystem for Linux [here](https://docs.microsoft.com/en-us/windows/wsl/install). On step 1, follow the recommendation of updating to WSL 2. You do not necessarily need to install Windows Terminal. Now go [here](https://docs.docker.com/desktop/windows/install/) and follow the "Install Docker Desktop on Windows" instructions. You can then start Docker Desktop and follow the quick start quide.

Install VS Code [using the instructions online](https://code.visualstudio.com/download).

## Open the folder in VS Code using "Dev Container"

Select File -> Open and select *the entire folder*.

VS Code will propose to install "Dev Container". Click "install".

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

## Make sure everything is OK

### Downloading test cases

Use this command to download the test cases:

    act4e-mcdp-download-tests --out downloaded

Then you have available a few test cases in the directory `downloaded/`.

### Running the DP solver

This is the command you use to run the DP solver:

    act4e-mcdp-solve-dp \
        --solver act4e_mcdp_solution.DPSolver \
        --query FixFunMinRes \
        --model downloaded/lib1-parts.e03_splitter1.primitivedps.mcdpr1.yaml \
        --data '42'

In brief:

* `--solver act4e_mcdp_solution.DPSolver`: this selects the class for your solver;
* `--query FixFunMinRes`: this selects `FixFunMinRes` (other choice: `FixResMaxFun`);
* `--model downloaded/lib1-parts.e03_splitter1.primitivedps.mcdpr1.yaml`: this selects the model to use for optimization;
* `--data '10'`: this selects the query to give. 

It is a YAML dictionary with a key for each functionality name.

You will see the result in the logs:

```
INFO query: 10
INFO solution: Interval(pessimistic=UpperSet(minima=[]), optimistic=UpperSet(minima=[]))
```

The template `act4e_mcdp_solution.MySolution` always returns an empty `UpperSet` (= infeasible).


### Running the MCDP solver


This is the command you use to run the MCDP solver:

    act4e-mcdp-solve-mcdp \
        --solver act4e_mcdp_solution.MCDPSolver \
        --query FixFunMinRes \
        --model downloaded/lib1-parts.e03_splitter1.models.mcdpr1.yaml \
        --data '{f: 42}'

Note that for the MCDP solver we give a file of type `models.mcdpr1.yaml` instead of `primitivedps.mcdpr1.yaml`.

For the data, we use a key-value pair with the functionality name and the value.

You should see the output:

    query: {'f': Decimal('42')}
    solution: Interval(pessimistic=UpperSet(minima=[]), optimistic=UpperSet(minima=[]))

## Next steps

TODO: exhaustive test case

# Setup

## Install Docker

<ul>
    <li> (Mac, Linux) Follow the [installation instructions](https://docs.docker.com/get-docker/) </li>
    <li>(Windows):
        <ul>
         <li>Follow the manual installation steps for Windows Subsystem for Linux [here](https://docs.microsoft.com/en-us/windows/wsl/install). On step 1, follow the recommendation of updating to WSL 2. You do not necessarily need to install Windows Terminal. </li>
            <li>Now go [here](https://docs.docker.com/desktop/windows/install/) and follow the "Install Docker Desktop on Windows" instructions. You can then start Docker Desktop and follow the quick start quide.</li>
        </ul>
    </li>
</ul>

## Install VS Code.

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

## Running the tests

Use this command to download the test cases:

    act4e-mcdp-download-tests --out downloaded

Then you have available a few test cases in the directory `downloaded/`.

This is the command you use to run the solver:

    act4e-mcdp-solve \
        --solver act4e_mcdp_solution.MySolution \
        --query FixFunMinRes \
        --model downloaded/lib1-parts.e03_splitter1.models.mcdpr1.yaml \
        --data '{f: 10}'

In turn:

* `--solver act4e_mcdp_solution.MySolution`: this selects your solver;
* `--query FixFunMinRes`: this selects `FixFunMinRes` (other choice: `FixResMaxFun`);
* `--model downloaded/lib1-parts.e03_splitter1.models.mcdpr1.yaml`: this selects the model to use for optimization;
* `--data '{f: 10}'`: this selects the query to give. It is a YAML dictionary with a key for each functionality name.

You will see the result in the logs:

```
INFO query: {'f': Decimal('10')}
INFO solution: UpperSet(minima=[])
```

The template `act4e_mcdp_solution.MySolution` always returns an empty `UpperSet` (= infeasible).
At this point, you can start implementing your solver.

For testing, run `act4e-mcdp-solve` on different files.


TODO: provide a exhaustive test case.

# Extra information

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



# Creating more test cases

The models are created using [this online environment][IDE] - very experimental!

[IDE]: https://editor.zuper.ai/editor/gh/co-design-models/ACT4E-exercises-spring2023/main/view/

If you make an account you can play around. You can obtain the YAML file read by `ACT4E-mcdp` by selecting the "DP compiled YAML representation" option from the drop down menu. Some of the other visualizations might also be helpful.

[Example: drone model](https://editor.zuper.ai/editor/gh/co-design-models/ACT4E-exercises-spring2023/main/view/libraries/lib2-simple/specs/models/things/drone1/)

 <img width="1113" alt="mcdpdrone" src="https://github.com/ACT4E/ACT4E-mcdp-exercise-template/assets/81052/b2e3c9ec-c55c-49c8-9e0c-071c02fb03c0">



<!--

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

--->

# lifeActuary 1.3.2
Package *lifeActuary* is a Python library to perform actuarial mathematics on life contingencies and classical financial mathematics computations. Versatile, simple and easy to use. The main functions are implemented using the usual actuarial approach, making it a natural choice for the life actuary.

This document is produced as a descriptive tool on how to use the package and as a user guide for the developed actuarial functions. For each actuarial function, an illustrative example is provided. 
        
The package uses Python version >= 3.6.

This package and functions herein are provided as is, without any guarantee regarding the accuracy of calculations. It's distributed using the [MIT License](https://en.wikipedia.org/wiki/MIT_License) and the authors disclaim any liability arising by any losses due to direct or indirect use of this package.
    
This package is still under development and further useful and interesting functions will be available any time soon.

## On Distribution 1.3.2
- We changed the class "annuities" and now all the life annuity functions do not rely on the computation of the actuarial table. The old functions are still available in "commutationtable"
- We developed a new class "mortality_insurance.py" where functions for evaluating life insurance contracts are available without the need to compute the commutation table. The old functions are still available in the class "commutationtable".
- We developed a new class for evaluating annuities and life insurance for groups of two individuals, for joint-life and last-survivor methods.
- We made a small correction to the function "present_value" and a large correction to the functions t_nIArx and t_nIArx_ in commutation_table.py.
- We made a small correction to the function "get_integral_px_method" in "mortality_table" class.
- We made a small correction to the function "annuity_x" in "annuities" class.
- We made a small correction to the npx and nqx functions in the module "mortality_table", when producing the fractional commutation tables using the Balducci and the Constante Mortality Force.

In this version you've a lot of [tests](https://github.com/parcr/LifeActuary_1.3.2/tree/main/tests), examples; [essay](https://github.com/parcr/LifeActuary_1.3.2/tree/main/essay),  [essay_for_Manual](https://github.com/parcr/LifeActuary_1.3.2/tree/main/essay_for_Manual) on how to use the library, as well as, our already famous [Manual](https://github.com/parcr/lifeActuary_1.3.2/blob/main/info/lifeActuary_v1_3_2.pdf).

Please, don't forget to download the soa_tables folder from github; [soa_tables](https://github.com/parcr/lifeActuary_1.3.2)

All files at [lifeactuary_1.3.2 at github](https://github.com/parcr/lifeactuary_1.3.2).

## Information On older Versions
You should also visit for version 1.0, [lifeactuary at github](https://github.com/parcr/lifeactuary) to download the folder *"soa_tables"* containing a set of tables, namely the ones used in the examples in the manual.

For version 1.2, take a look for  [lifeactuary_1.2 at github](https://github.com/parcr/lifeactuary_1.2) to download the folder *"soa_tables"* containing a set of tables, namely the ones used in the examples in the manual.

Version 1.2.1 includes the file **"read_soa_table_xml.py"**, so that you just need to a look at  [lifeactuary_1.2 at github](https://github.com/parcr/lifeactuary_1.2) to download the folder *"soa_tables"* containing a set of tables, namely the ones used in the examples in the manual.
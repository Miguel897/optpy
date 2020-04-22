# OPTimization in PYthon (OPTPY)

This repository compares different alternatives to solve optimization problems in Python

We solve a standard linear programming problem of the form

Min  c*x
s.t. A*x <= b
     x >= 0

where x is a vector with all variables and c, A, b are matrices of appropiate dimension whose elements are randomly generated using normal probability distributions.

## Installation

```python
git clone https://github.com/salvapineda/optpy.git

cd optpy
```

## Method 1: SCIPY [link](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.linprog.html)

Pros: It only requires importing the scipy package
Cons: Optimization problem must be transform into matricial form

```python
  # Import system class
  from optpy import lp

  # Create linear programming probblem with 10 variables and 5 constraints. Further info: help(lp)
  lp1 = lp(nvar=10,ncon=5)

  # Solve linear problem using scipy. Further info: help(lp.solve_scipy)
  obj,x = lp1.solve_scipy(method='simplex')
```

## Method 2: PULP [link](https://pypi.org/project/PuLP/)

Pros: It relies on open-source solvers glpk and cbc. Linear and integer problems can be solved. Intuitive sintax.
Cons: It does not solve non-linear problems.

```python
  # Import system class
  from optpy import lp

  # Create linear programming probblem with 10 variables and 5 constraints. Further info: help(lp)
  lp1 = lp(nvar=10,ncon=5)

  # Solve linear problem using pulp. Further info: help(lp.solve_pulp)
  obj,x = lp1.solve_pulp()
```

## Method 3: PYOMO [link](http://www.pyomo.org/)

Pros: It solves all kind of optimization problems. Intuitive sintax.
Cons: It needs access to solvers, although neos server can be also used.

```python
  # Import system class
  from optpy import lp

  # Create linear programming probblem with 10 variables and 5 constraints. Further info: help(lp)
  lp1 = lp(nvar=10,ncon=5)

  # Solve linear problem using pyomo. Further info: help(lp.solve_pyomo)
  obj,x = lp1.solve_pyomo(neos=True,solver='cplex')
```

## Do you want to contribute?
 
 Any feedback is welcome so feel free to ask or comment anything you want via a Pull Request in this repo. If you need extra help, you can ask Salvador Pineda (spinedamorente@gmail.com).
 

## Developed by 

 * [Salvador Pineda](https://www.researchgate.net/profile/Salvador_Pineda) - spinedamorente@gmail.com

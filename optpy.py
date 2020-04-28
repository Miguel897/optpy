############################ IMPORT ############################

import pdb
import numpy as np
import pulp as pu
import random
import pandas as pd
import pyomo.environ as pe
import pyomo.kernel as pk
from scipy.optimize import linprog

######################### LINEAR PROGRAM  ########################

class lp:
  """
  A class to represent a linear programming problem
  """

  def __init__(self,nvar=10,ncon=5):
    """
    Constructs all the necessary attributes for the following linear programming problem:

    Min  c*x
    s.t. A*x <= b
         x >= 0

    Parameters
    ----------
    nvar (int, default=10): number of variables
    ncon (int, default=5): number of constraints

    """
    self.nvar = nvar
    self.ncon = ncon
    self.c = [round(abs(random.gauss(0,1)),2) for i in range(nvar)]
    self.A = [[round(random.gauss(0,1),2) for i in range(nvar)] for j in range(ncon)]
    self.b = [round(random.gauss(0,1),2) for j in range(ncon)]

  def solve_scipy(self,method='interior-point'):
    """
    Solve the problem using the scipy package

    Parameters
    ----------
    method (str, default:'interior-point'): method used by scipy
        - interior-point
        - revised simplex
        - simplex
    Returns
    -------
    obj (real): objective function
    x (list): optimal solution of variables

    """
    # Solve problem
    res = linprog(self.c, A_ub=self.A, b_ub=self.b)
    print(res)
    # Output
    return round(res.fun,2),np.round(res.x,2).tolist()


  def solve_pulp(self):
    """
    Solve the problem using the pulp package

    Returns
    -------
    obj_fun (real): objective function
    sol (list): optimal solution of variables

    """
    # Model
    m = pu.LpProblem('LinearProblem',pu.LpMinimize)
    # Variables
    x = pu.LpVariable.dicts('x', list(range(self.nvar)), lowBound=0, cat="Continuous")
    # Objective function
    m += sum(self.c[i]*x[i] for i in range(self.nvar))
    # Constraints
    for j in range(self.ncon):
        m += sum(self.A[j][i]*x[i] for i in range(self.nvar)) <= self.b[j]
    # Print problem
    print(m)
    # Solve problem
    m.solve()
    print("Status:", pu.LpStatus[m.status])
    # Output
    return round(pu.value(m.objective),2),[round(x[i].varValue,2) for i in range(self.nvar)]

  def solve_pyomo_environ(self,neos=True,solver='cplex'):
    """
    Solve the problem using the standard environ Pyomo package

    Parameters
    ----------
    neos (boolean, default:True): if True the problem is solved in neos server. Otherwise, it uses local solvers
    solver (str, default:'cplex'): defines the solver used to solve the optimization problem

    Returns
    -------
    obj_fun (real): objective function
    sol (list): optimal solution of variables

    """
    # Model
    m = pe.ConcreteModel()
    # Sets
    m.i = pe.Set(initialize=range(self.nvar),ordered=True)
    m.j = pe.Set(initialize=range(self.ncon),ordered=True)
    # Variables
    m.z = pe.Var()
    m.x = pe.Var(m.i,within=pe.NonNegativeReals)
    # Objective function
    def obj_rule(m):
      return sum(self.c[i]*m.x[i] for i in m.i)
    m.obj = pe.Objective(rule=obj_rule)
    # Constraints
    def con_rule(m,j):
      return sum(self.A[j][i]*m.x[i] for i in m.i) <= self.b[j]
    m.con = pe.Constraint(m.j,rule=con_rule)
    # Print problem
    m.pprint()
    # Solve problem
    if neos:
      res = pe.SolverManagerFactory('neos').solve(m,opt=pe.SolverFactory(solver))
    else:
      res = pe.SolverFactory(solver).solve(m,symbolic_solver_labels=True,tee=True)
    print(res['Solver'][0])
    # Output
    return round(m.obj(),2),[round(m.x[i].value,2) for i in m.i]

  def solve_pyomo_kernel(self,solver='cplex'):
    """
    Solve the problem using the kernel library of the Pyomo package.

    Parameters
    ----------
    solver (str, default:'cplex'): defines the solver used to solve the optimization problem

    Returns
    -------
    obj_fun (real): objective function
    sol (list): optimal solution of variables

    """
    # Model
    m = pk.block()
    # Sets
    m.i = range(self.nvar)
    m.j = range(self.ncon)
    # Variables
    m.x = pk.variable_list()
    for _ in m.i:
      m.x.append(pk.variable(domain=pk.Reals, lb=0))
    # Objective function
    m.obj = pk.objective(pe.quicksum(self.c[i]*m.x[i] for i in m.i), sense=pk.minimize)
    # Constraints
    m.con = pk.constraint_list()
    for j in m.j:
      m.con.append(pk.constraint(body=pe.quicksum(self.A[j][i]*m.x[i] for i in m.i), lb=None, ub=self.b[j]))
    # Solve problem
    res = pe.SolverFactory(solver).solve(m,symbolic_solver_labels=True,tee=True)
    print(res['Solver'][0])
    # Output
    return round(m.obj(),2),[round(m.x[i].value,2) for i in m.i]

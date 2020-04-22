from optpy import lp

lp1 = lp(nvar=10,ncon=5)
obj1,x1 = lp1.solve_scipy(method='simplex')
obj2,x2 = lp1.solve_pulp()
obj3,x3 = lp1.solve_pyomo(neos=True,solver='cplex')





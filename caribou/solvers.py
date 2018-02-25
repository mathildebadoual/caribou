import numpy as np
import cvxpy
import cvxopt

HOURS_PER_DAY = 24

def with_quadprog(h, f, a, b, ae, be):
    """
    solve the following e the following quadratic programm using quadprog:
    minimize
        (1/2) * x.t * h * x + f.t * x
    subject to
        a * x <= b
        ae * x == be
    """
    h_qp = h
    f_qp = -f
    if ae is not None:
        a_qp = -np.concatenate((ae, a), axis=0).T
        b_qp = -np.concatenate((be, b), axis=0)
        meq = ae.shape[0]
    else:
        a_qp = -a.T
        b_qp = -b
        meq = 0
    b_qp = np.reshape(b_qp, (b_qp.shape[0], ))
    f_qp = np.reshape(f_qp, (f_qp.shape[0], ))
    x_result = quadprog.solve_qp(h_qp, f_qp, a_qp, b_qp, meq)[0]
    y_result = quadprog.solve_qp(h_qp, f_qp, a_qp, b_qp, meq)[1]
    return x_result, y_result


def with_cvxpy(h, f, a, b, ae, be, solver='CVXOPT'):
    """
    solve the following e the following quadratic programm using quadprog:
    minimize
        (1/2) * x.t * h * x + f.t * x
    subject to
        a * x <= b
        ae * x == be
    """
    n = f.shape[0]
    x = cvxpy.Variable(n)
    h = cvxpy.Constant(h)
    quadratic_form = (1 / 2) * cvxpy.quad_form(x, h) + f.T * x
    objective = cvxpy.Minimize(quadratic_form)
    constraints = []
    if a is not None:
        constraints.append(a * x <= b)
    if ae is not None:
        constraints.append(ae * x == be)
    prob = cvxpy.Problem(objective, constraints)
    y_result = prob.solve(solver=solver)
    x_result = np.reshape(np.array(x.value), (-1,))
    return x_result, y_result


def with_cvxopt(h, f, a, b, ae, be):
    """
    solve the following e the following quadratic programm using quadprog:
    minimize
        (1/2) * x.t * h * x + f.t * x
    subject to
        a * x <= b
        ae * x == be
    """
    h_qp = cvxopt.matrix(h, h.shape)
    f_qp = cvxopt.matrix(f, f.shape)
    a_qp = cvxopt.matrix(a, (7 * HOURS_PER_DAY, 2 * HOURS_PER_DAY))
    b_qp = cvxopt.matrix(b, (7 * HOURS_PER_DAY, 1))
    ae_qp = cvxopt.matrix(ae, (1, 2 * HOURS_PER_DAY))
    be_qp = cvxopt.matrix(be, (1, 1), tc='d')
    sol = cvxopt.solvers.qp(h_qp, f_qp, a_qp, b_qp, ae_qp, be_qp)
    x_result = np.array(sol['x'])
    y_result = (1 / 2) * np.dot(x_result.T, np.dot(h, x_result)) + np.dot(f.T, x_result)
    return x_result, y_result

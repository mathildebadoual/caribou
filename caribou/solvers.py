import numpy as np
import quadprog
import cvxpy


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


def with_cvxpy(h, f, a, b, ae, be):
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
    y_result = prob.solve()
    x_result = np.reshape(np.array(x.value), (-1,))
    return x_result, y_result

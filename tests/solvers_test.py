import unittest
import numpy as np
import scipy.linalg
import caribou.solvers as solvers


class TestQpSolvers(unittest.TestCase):
    def setUp(self):
        self.sizes = [10, 100, 1000]

    def test_with_quadprog(self):
        for size in self.sizes:
            self.assertEqual(
                self.solve_random_qp(size, solvers.with_quadprog)[0].shape,
                (size, ))

    def test_with_cvxpy(self):
        for size in self.sizes:
            self.assertEqual(
                self.solve_random_qp(size, solvers.with_cvxpy)[0].shape,
                (size, ))

    def solve_random_qp(self, n, solver):
        M, b = np.random.random((n, n)), np.random.random(n)
        P, q = np.dot(M.T, M), np.dot(b, M).reshape((n, ))
        G = scipy.linalg.toeplitz([1., 0., 0.] + [0.] * (n - 3),
                                  [1., 2., 3.] + [0.] * (n - 3))
        h = np.ones(n)
        return solver(P, q, G, h, None, None)

from benchopt import BaseSolver, safe_import_context


with safe_import_context() as ctx:
    import numpy as np
    from scipy.optimize import least_squares


class Solver(BaseSolver):
    """Reparametrization with scipy least squares."""
    name = 'reparam'

    def set_objective(self, X, y, lmbd):
        # The arguments of this function are the results of the
        # `to_dict` method of the objective.
        # They are customizable.
        self.X, self.y = X, y
        self.lmbd = lmbd

    def run(self, n_iter):
        X, y = self.X, self.y

        def func(y):
            return np.hstack((
                X.dot(y**3) - y,
                np.sqrt(self.lam) * y
            ))

        def dfunc(y):
            return np.vstack((
                3 * X * y[None, :]**2,
                np.sqrt(self.lam) * np.eye(len(y))
            ))

        x0 = np.linalg.lstsq(X, y, rcond=None)[0]
        results = least_squares(
            func, np.abs(x0)**(1/3) * np.sign(x0), jac=dfunc,
            method='lm',
            max_nfev=n_iter,
            verbose=1,
        )

        self.w = results.x ** 3

    def get_result(self):
        return self.w

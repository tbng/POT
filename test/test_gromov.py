"""Tests for module gromov  """

# Author: Erwan Vautier <erwan.vautier@gmail.com>
#         Nicolas Courty <ncourty@irisa.fr>
#         Titouan Vayer <titouan.vayer@irisa.fr>
#
# License: MIT License

import numpy as np
import ot

import pytest


def test_gromov():
    n_samples = 50  # nb samples

    mu_s = np.array([0, 0])
    cov_s = np.array([[1, 0], [0, 1]])

    xs = ot.datasets.make_2D_samples_gauss(n_samples, mu_s, cov_s, random_state=4)

    xt = xs[::-1].copy()

    p = ot.unif(n_samples)
    q = ot.unif(n_samples)

    C1 = ot.dist(xs, xs)
    C2 = ot.dist(xt, xt)

    C1 /= C1.max()
    C2 /= C2.max()

    G = ot.gromov.gromov_wasserstein(C1, C2, p, q, 'square_loss', verbose=True)

    # check constraints
    np.testing.assert_allclose(
        p, G.sum(1), atol=1e-04)  # cf convergence gromov
    np.testing.assert_allclose(
        q, G.sum(0), atol=1e-04)  # cf convergence gromov

    Id = (1 / (1.0 * n_samples)) * np.eye(n_samples, n_samples)

    np.testing.assert_allclose(
        G, np.flipud(Id), atol=1e-04)

    gw, log = ot.gromov.gromov_wasserstein2(C1, C2, p, q, 'kl_loss', log=True)

    gw_val = ot.gromov.gromov_wasserstein2(C1, C2, p, q, 'kl_loss', log=False)

    G = log['T']

    np.testing.assert_allclose(gw, 0, atol=1e-1, rtol=1e-1)

    np.testing.assert_allclose(gw, gw_val, atol=1e-1, rtol=1e-1)  # cf log=False

    # check constraints
    np.testing.assert_allclose(
        p, G.sum(1), atol=1e-04)  # cf convergence gromov
    np.testing.assert_allclose(
        q, G.sum(0), atol=1e-04)  # cf convergence gromov


def test_entropic_gromov():
    n_samples = 50  # nb samples

    mu_s = np.array([0, 0])
    cov_s = np.array([[1, 0], [0, 1]])

    xs = ot.datasets.make_2D_samples_gauss(n_samples, mu_s, cov_s, random_state=42)

    xt = xs[::-1].copy()

    p = ot.unif(n_samples)
    q = ot.unif(n_samples)

    C1 = ot.dist(xs, xs)
    C2 = ot.dist(xt, xt)

    C1 /= C1.max()
    C2 /= C2.max()

    G = ot.gromov.entropic_gromov_wasserstein(
        C1, C2, p, q, 'square_loss', epsilon=5e-4, verbose=True)

    # check constraints
    np.testing.assert_allclose(
        p, G.sum(1), atol=1e-04)  # cf convergence gromov
    np.testing.assert_allclose(
        q, G.sum(0), atol=1e-04)  # cf convergence gromov

    gw, log = ot.gromov.entropic_gromov_wasserstein2(
        C1, C2, p, q, 'kl_loss', epsilon=1e-2, log=True)

    G = log['T']

    np.testing.assert_allclose(gw, 0, atol=1e-1, rtol=1e-1)

    # check constraints
    np.testing.assert_allclose(
        p, G.sum(1), atol=1e-04)  # cf convergence gromov
    np.testing.assert_allclose(
        q, G.sum(0), atol=1e-04)  # cf convergence gromov


def test_pointwise_gromov():
    n_samples = 50  # nb samples

    mu_s = np.array([0, 0])
    cov_s = np.array([[1, 0], [0, 1]])

    xs = ot.datasets.make_2D_samples_gauss(n_samples, mu_s, cov_s, random_state=42)

    xt = xs[::-1].copy()

    p = ot.unif(n_samples)
    q = ot.unif(n_samples)

    C1 = ot.dist(xs, xs)
    C2 = ot.dist(xt, xt)

    C1 /= C1.max()
    C2 /= C2.max()

    def loss(x, y):
        return np.abs(x - y)

    G, log = ot.gromov.pointwise_gromov_wasserstein(
        C1, C2, p, q, loss, max_iter=100, log=True, verbose=True, random_state=42)

    # check constraints
    np.testing.assert_allclose(
        p[:, np.newaxis], G.sum(1), atol=1e-04)  # cf convergence gromov
    np.testing.assert_allclose(
        q[np.newaxis, :], G.sum(0), atol=1e-04)  # cf convergence gromov

    assert log['gw_dist_estimated'] == 0.0
    assert log['gw_dist_std'] == 0.0

    G, log = ot.gromov.pointwise_gromov_wasserstein(
        C1, C2, p, q, loss, max_iter=100, alpha=0.1, log=True, verbose=True, random_state=42)

    assert log['gw_dist_estimated'] == 0.10342276348494964
    assert log['gw_dist_std'] == 0.0015952535464736394


def test_sampled_gromov():
    n_samples = 50  # nb samples

    mu_s = np.array([0, 0])
    cov_s = np.array([[1, 0], [0, 1]])

    xs = ot.datasets.make_2D_samples_gauss(n_samples, mu_s, cov_s, random_state=42)

    xt = xs[::-1].copy()

    p = ot.unif(n_samples)
    q = ot.unif(n_samples)

    C1 = ot.dist(xs, xs)
    C2 = ot.dist(xt, xt)

    C1 /= C1.max()
    C2 /= C2.max()

    def loss(x, y):
        return np.abs(x - y)

    G, log = ot.gromov.sampled_gromov_wasserstein(
        C1, C2, p, q, loss, max_iter=100, epsilon=1, log=True, verbose=True, random_state=42)

    # check constraints
    np.testing.assert_allclose(
        p, G.sum(1), atol=1e-04)  # cf convergence gromov
    np.testing.assert_allclose(
        q, G.sum(0), atol=1e-04)  # cf convergence gromov

    assert log['gw_dist_estimated'] == 0.05679474884977278
    assert log['gw_dist_std'] == 0.0005986592106971995


def test_gromov_barycenter():
    ns = 10
    nt = 20

    Xs, ys = ot.datasets.make_data_classif('3gauss', ns, random_state=42)
    Xt, yt = ot.datasets.make_data_classif('3gauss2', nt, random_state=42)

    C1 = ot.dist(Xs)
    C2 = ot.dist(Xt)

    n_samples = 3
    Cb = ot.gromov.gromov_barycenters(n_samples, [C1, C2],
                                      [ot.unif(ns), ot.unif(nt)
                                       ], ot.unif(n_samples), [.5, .5],
                                      'square_loss',  # 5e-4,
                                      max_iter=100, tol=1e-3,
                                      verbose=True)
    np.testing.assert_allclose(Cb.shape, (n_samples, n_samples))

    Cb2 = ot.gromov.gromov_barycenters(n_samples, [C1, C2],
                                       [ot.unif(ns), ot.unif(nt)
                                        ], ot.unif(n_samples), [.5, .5],
                                       'kl_loss',  # 5e-4,
                                       max_iter=100, tol=1e-3)
    np.testing.assert_allclose(Cb2.shape, (n_samples, n_samples))


@pytest.mark.filterwarnings("ignore:divide")
def test_gromov_entropic_barycenter():
    ns = 10
    nt = 20

    Xs, ys = ot.datasets.make_data_classif('3gauss', ns, random_state=42)
    Xt, yt = ot.datasets.make_data_classif('3gauss2', nt, random_state=42)

    C1 = ot.dist(Xs)
    C2 = ot.dist(Xt)

    n_samples = 2
    Cb = ot.gromov.entropic_gromov_barycenters(n_samples, [C1, C2],
                                               [ot.unif(ns), ot.unif(nt)
                                                ], ot.unif(n_samples), [.5, .5],
                                               'square_loss', 1e-3,
                                               max_iter=50, tol=1e-3,
                                               verbose=True)
    np.testing.assert_allclose(Cb.shape, (n_samples, n_samples))

    Cb2 = ot.gromov.entropic_gromov_barycenters(n_samples, [C1, C2],
                                                [ot.unif(ns), ot.unif(nt)
                                                 ], ot.unif(n_samples), [.5, .5],
                                                'kl_loss', 1e-3,
                                                max_iter=100, tol=1e-3)
    np.testing.assert_allclose(Cb2.shape, (n_samples, n_samples))


def test_fgw():

    n_samples = 50  # nb samples

    mu_s = np.array([0, 0])
    cov_s = np.array([[1, 0], [0, 1]])

    xs = ot.datasets.make_2D_samples_gauss(n_samples, mu_s, cov_s, random_state=42)

    xt = xs[::-1].copy()

    ys = np.random.randn(xs.shape[0], 2)
    yt = ys[::-1].copy()

    p = ot.unif(n_samples)
    q = ot.unif(n_samples)

    C1 = ot.dist(xs, xs)
    C2 = ot.dist(xt, xt)

    C1 /= C1.max()
    C2 /= C2.max()

    M = ot.dist(ys, yt)
    M /= M.max()

    G, log = ot.gromov.fused_gromov_wasserstein(M, C1, C2, p, q, 'square_loss', alpha=0.5, log=True)

    # check constraints
    np.testing.assert_allclose(
        p, G.sum(1), atol=1e-04)  # cf convergence fgw
    np.testing.assert_allclose(
        q, G.sum(0), atol=1e-04)  # cf convergence fgw

    Id = (1 / (1.0 * n_samples)) * np.eye(n_samples, n_samples)

    np.testing.assert_allclose(
        G, np.flipud(Id), atol=1e-04)  # cf convergence gromov

    fgw, log = ot.gromov.fused_gromov_wasserstein2(M, C1, C2, p, q, 'square_loss', alpha=0.5, log=True)

    G = log['T']

    np.testing.assert_allclose(fgw, 0, atol=1e-1, rtol=1e-1)

    # check constraints
    np.testing.assert_allclose(
        p, G.sum(1), atol=1e-04)  # cf convergence gromov
    np.testing.assert_allclose(
        q, G.sum(0), atol=1e-04)  # cf convergence gromov


def test_fgw_barycenter():
    np.random.seed(42)

    ns = 50
    nt = 60

    Xs, ys = ot.datasets.make_data_classif('3gauss', ns, random_state=42)
    Xt, yt = ot.datasets.make_data_classif('3gauss2', nt, random_state=42)

    ys = np.random.randn(Xs.shape[0], 2)
    yt = np.random.randn(Xt.shape[0], 2)

    C1 = ot.dist(Xs)
    C2 = ot.dist(Xt)

    n_samples = 3
    X, C = ot.gromov.fgw_barycenters(n_samples, [ys, yt], [C1, C2], [ot.unif(ns), ot.unif(nt)], [.5, .5], 0.5,
                                     fixed_structure=False, fixed_features=False,
                                     p=ot.unif(n_samples), loss_fun='square_loss',
                                     max_iter=100, tol=1e-3)
    np.testing.assert_allclose(C.shape, (n_samples, n_samples))
    np.testing.assert_allclose(X.shape, (n_samples, ys.shape[1]))

    xalea = np.random.randn(n_samples, 2)
    init_C = ot.dist(xalea, xalea)

    X, C = ot.gromov.fgw_barycenters(n_samples, [ys, yt], [C1, C2], ps=[ot.unif(ns), ot.unif(nt)], lambdas=[.5, .5], alpha=0.5,
                                     fixed_structure=True, init_C=init_C, fixed_features=False,
                                     p=ot.unif(n_samples), loss_fun='square_loss',
                                     max_iter=100, tol=1e-3)
    np.testing.assert_allclose(C.shape, (n_samples, n_samples))
    np.testing.assert_allclose(X.shape, (n_samples, ys.shape[1]))

    init_X = np.random.randn(n_samples, ys.shape[1])

    X, C, log = ot.gromov.fgw_barycenters(n_samples, [ys, yt], [C1, C2], [ot.unif(ns), ot.unif(nt)], [.5, .5], 0.5,
                                          fixed_structure=False, fixed_features=True, init_X=init_X,
                                          p=ot.unif(n_samples), loss_fun='square_loss',
                                          max_iter=100, tol=1e-3, log=True)
    np.testing.assert_allclose(C.shape, (n_samples, n_samples))
    np.testing.assert_allclose(X.shape, (n_samples, ys.shape[1]))

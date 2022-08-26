import numpy as np
from scipy.integrate import odeint


class Kuramoto:

    def __init__(self, coupling=1, dt=0.01, T=10, n_nodes=None, base_iter=126, natfreqs=None, half_sync=False):
        '''
        coupling: float
            Coupling strength. Default = 1. Typical values range between 0.4-2
        dt: float
            Delta t for integration of equations.
        T: float
            Total time of simulated activity.
            From that the number of integration steps is T/dt.
        n_nodes: int, optional
            Number of oscillators.
            If None, it is inferred from len of natfreqs.
            Must be specified if natfreqs is not given.
        base_iter: int, optional
            Training iteration.
            This is where the "baseline" concentration is calculated.
        natfreqs: 1D ndarray, optional
            Natural oscillation frequencies.
            If None, then new random values will be generated and kept fixed
            for the object instance.
            Must be specified if n_nodes is not given.
            If given, it overrides the n_nodes argument.
        '''
        if n_nodes is None and natfreqs is None:
            raise ValueError("n_nodes or natfreqs must be specified")

        self.dt = dt
        self.T = T
        self.coupling = coupling
        self.base_iter = base_iter
        self.half_sync = half_sync
        
        if self.half_sync == False: self.concentrated=False
        else: self.concentrated=True

        if natfreqs is not None:
            self.natfreqs = natfreqs
            self.n_nodes = len(natfreqs)
        else:
            self.n_nodes = n_nodes
            self.natfreqs = np.random.normal(size=self.n_nodes)

    def init_angles(self):
        '''
        Random initial random angles (position, "theta").
        '''
        if self.half_sync:
            return np.pi * np.random.random(size=self.n_nodes)
        
        return 2* np.pi * np.random.random(size=self.n_nodes)

    def derivative(self, angles_vec, t, adj_mat, coupling):
        '''
        Compute derivative of all nodes for current state, defined as

        dx_i    natfreq_i + k  sum_j ( Aij* sin (angle_j - angle_i) )
        ---- =             ---
         dt                M_i

        t: for compatibility with scipy.odeint
        '''
        assert len(angles_vec) == len(self.natfreqs) == len(adj_mat), \
            'Input dimensions do not match, check lengths'

        angles_i, angles_j = np.meshgrid(angles_vec, angles_vec)
        interactions = adj_mat * np.sin(angles_j - angles_i)  # Aij * sin(j-i)

        dxdt = self.natfreqs + coupling * interactions.sum(axis=0)  # sum over incoming interactions
        return dxdt

    def integrate(self, angles_vec, adj_mat):
        '''Updates all states by integrating state of all nodes'''
        # Coupling term (k / Mj) is constant in the integrated time window.
        # Compute it only once here and pass it to the derivative function
        n_interactions = (adj_mat != 0).sum(axis=0)  # number of incoming interactions
        coupling = self.coupling / n_interactions  # normalize coupling by number of interactions

        t = np.linspace(0, self.T, int(self.T/self.dt))
        timeseries = odeint(self.derivative, angles_vec, t, args=(adj_mat, coupling))
        return timeseries.T  # transpose for consistency (act_mat:node vs time)

    def run(self, adj_mat=None, angles_vec=None):
        '''
        adj_mat: 2D nd array
            Adjacency matrix representing connectivity.
        angles_vec: 1D ndarray, optional
            States vector of nodes representing the position in radians.
            If not specified, random initialization [0, 2pi].

        Returns
        -------
        act_mat: 2D ndarray
            Activity matrix: node vs time matrix with the time series of all
            the nodes.
        '''
        if angles_vec is None:
            angles_vec = self.init_angles()

        sim = self.integrate(angles_vec, adj_mat) % (2*np.pi)
        
#         def predict_concentration(arr):
#             v1 = []
#             for i in range(len(arr) - 1) :
#                 diff = arr[i + 1] - arr[i]
#                 v1.append(diff)
#             extra_diff = (2*np.pi - arr[len(arr) - 1]) + arr[0]
#             v1.append(extra_diff)
            
#             v1 = np.array(v1)
            
#             width = np.abs(2*np.pi - v1.max())
#             threshold = np.pi
            
#             if width < threshold: 
#                 return True
#             else: 
#                 return False

        def predict_concentration(colors):
            """
            computes width from a color list
            """
            #print(colors)
            ordered = list(np.pi - colors); ordered.sort()
            lordered = len(ordered)
            #print(ordered)
            threshold = np.pi
            if ordered == 0:
                assert("Empty array or logic error.")
            elif lordered == 1:
                return 0
            elif lordered == 2:
                dw = ordered[1]-ordered[0]
                if dw > threshold:
                    return 2*np.pi - dw
                else:
                    return dw
            else:
                widths = [2*np.pi+ordered[0]-ordered[-1]]
                for i in range(lordered-1):
                    widths.append(ordered[i+1]-ordered[i])
                #print(min(widths),'------')
                return np.abs(2*np.pi - max(widths))
        
        ## Baseline iteration concentration
        base_arr = sim.T[self.base_iter]
        self.baseline = (predict_concentration(base_arr) < np.pi)
        
        ## Training iteration concentration
        arr = sim.T[-1]
        self.concentrated = (predict_concentration(arr) < np.pi)
            
        return sim

    @staticmethod
    def phase_coherence(angles_vec):
        '''
        Compute global order parameter R_t - mean length of resultant vector
        '''
        suma = sum([(np.e ** (1j * i)) for i in angles_vec])
        return abs(suma / len(angles_vec))

    def mean_frequency(self, act_mat, adj_mat):
        '''
        Compute average frequency within the time window (self.T) for all nodes
        '''
        assert len(adj_mat) == act_mat.shape[0], 'adj_mat does not match act_mat'
        _, n_steps = act_mat.shape

        # Compute derivative for all nodes for all time steps
        dxdt = np.zeros_like(act_mat)
        for time in range(n_steps):
            dxdt[:, time] = self.derivative(act_mat[:, time], None, adj_mat)

        # Integrate all nodes over the time window T
        integral = np.sum(dxdt * self.dt, axis=1)
        # Average across complete time window - mean angular velocity (freq.)
        meanfreq = integral / self.T
        return meanfreq

"""
A file exporting the tour algorithms.

Any new tour algorithm should be constructed as a function that creates a class
called 'Generator'. The class is to be initialised and passed onto the
'new_geodesic_path' function.
"""

from .grand_tour import grand_tour
from .dependence_tour import dependence_tour
from .little_tour import little_tour
from .local_tour import local_tour
from .guided_tour import guided_tour
from .planned_tour import *
from .indices import *

class Tour:
    """
    A class that controls the tour algorithm framework.

    Attributes
    ----------
    data : ndarray
    proj : ndarray
        The nx3 projection matrix.
    target : ndarray
        The target projection matrix.
    cur_dist : float
        The current distance.
    target_dist : float
        The target distance.
    geodesic : dict
        A dictionary containing the...
    tour_path : function
        A tour algorithm.
    """

    def __init__(self, data, tour_path, start=None):

        self.data = data

        if start is None:
            start = tour_path(None, self.data)

        self.proj = start

        self.target = None

        self.cur_dist = 0
        self.target_dist = 0
        self.geodesic = None

        self.tour_path = tour_path

    def interpolate(self, step_size):
        """
        Method : Calculate the interpolated projection matrix.
        ...
        Parameters
        ----------
        step_size : float
            A floating point number describing the step size of the angle of rotation.

        Return
        ------
        An interpolated projection matrix.
        """

        self.cur_dist += step_size

        #if step_size > 0 and np.isfinite(step_size) and self.cur_dist >= self.target_dist:
        #    self.proj = self.geodesic["interpolate"](1.0)

        if self.cur_dist >= self.target_dist:

            self.geodesic = self.tour_path(self.proj, self.data)

            self.target_dist = self.geodesic["dist"]
            self.target = self.geodesic["Fz"]
            self.cur_dist = 0

            if not np.isfinite(step_size):
                self.cur_dist = self.target_dist

        # The rewind has reached or surpassed the initial point.
        elif self.cur_dist <= 0:
            self.cur_dist = 0

        self.proj = self.geodesic["interpolate"](self.cur_dist / self.target_dist)
        
        return self.proj

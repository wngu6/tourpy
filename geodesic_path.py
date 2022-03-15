from .geodesic import geodesic_path, proj_dist

def new_geodesic_path(generator):
    """
    Constructs a function.

    Parameters
    ----------
    generator : class
        A class with a method named generate.

    Returns
    -------
    A function to generate the interpolation framework.
    """

    def tour_path(current, data):
        """

        Parameters
        ----------
        current : ndarray or None
            A projection matrix.
        data : ndarray
            The data set.

        Returns
        -------
        A dictionary containing all the information required to perform the interpolation.
        """
        if current is None:
            return generator.generate(None, data)

        dist = 0
        tries = 0
        while dist < 1e-3:
            target = generator.generate(current, data)

            if target is None: return None

            tries += 1
            if tries > 10: return None

            dist = proj_dist(current, target)

            # if dist < 1e-2: return None

        return geodesic_path(current, target)

    return tour_path

# (C) British Crown Copyright 2018 - 2019, Met Office
#
# This file is part of iris-grib.
#
# iris-grib is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the
# Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# iris-grib is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with iris-grib.  If not, see <http://www.gnu.org/licenses/>.
"""
Unit tests for :meth:`iris_grib._save_rules.grid_definition_template_20`.

"""

from __future__ import (absolute_import, division, print_function)
from six.moves import (filter, input, map, range, zip)  # noqa

# Import iris_grib.tests first so that some things can be initialised before
# importing anything else.
import iris_grib.tests as tests

from iris.coord_systems import GeogCS, Stereographic
import numpy as np

from iris_grib._save_rules import grid_definition_template_20
from iris_grib.tests.unit.save_rules import GdtTestMixin


class Test(tests.IrisGribTest, GdtTestMixin):
    def setUp(self):
        self.default_ellipsoid = GeogCS(semi_major_axis=6371200.0)
        self.stereo_test_cube = self._make_test_cube(coord_units='m')

        GdtTestMixin.setUp(self)

    def _default_coord_system(self):
        return Stereographic(90.0, 0, ellipsoid=self.default_ellipsoid)

    def test__template_number(self):
        grid_definition_template_20(self.stereo_test_cube, self.mock_grib)
        self._check_key('gridDefinitionTemplateNumber', 20)

    def test__shape_of_earth(self):
        grid_definition_template_20(self.stereo_test_cube, self.mock_grib)
        self._check_key('shapeOfTheEarth', 1)
        self._check_key('scaleFactorOfRadiusOfSphericalEarth', 0)
        self._check_key('scaleFactorOfEarthMajorAxis', 0)
        self._check_key('scaledValueOfEarthMajorAxis', 0)
        self._check_key('scaleFactorOfEarthMinorAxis', 0)
        self._check_key('scaledValueOfEarthMinorAxis', 0)

    def test__grid_shape(self):
        stereo_test_cube = self._make_test_cube(x_points=np.arange(13),
                                                y_points=np.arange(6),
                                                coord_units='m')
        grid_definition_template_20(stereo_test_cube, self.mock_grib)
        self._check_key('Nx', 13)
        self._check_key('Ny', 6)

    def test__grid_points(self):
        stereo_test_cube = self._make_test_cube(x_points=[1e6, 3e6, 5e6, 7e6],
                                                y_points=[4e6, 9e6],
                                                coord_units='m')
        grid_definition_template_20(stereo_test_cube, self.mock_grib)
        self._check_key("latitudeOfFirstGridPoint", 54139565)
        self._check_key("longitudeOfFirstGridPoint", 165963757)
        self._check_key("Dx", 2e9)
        self._check_key("Dy", 5e9)

    def test__template_specifics(self):
        grid_definition_template_20(self.stereo_test_cube, self.mock_grib)
        self._check_key("LaD", 90e6)
        self._check_key("LoV", 0)

    def test__scanmode(self):
        grid_definition_template_20(self.stereo_test_cube, self.mock_grib)
        self._check_key('iScansPositively', 1)
        self._check_key('jScansPositively', 1)

    def test__scanmode_reverse(self):
        stereo_test_cube = \
            self._make_test_cube(x_points=np.arange(7e6, 0, -1e6),
                                 coord_units='m')
        grid_definition_template_20(stereo_test_cube, self.mock_grib)
        self._check_key('iScansPositively', 0)
        self._check_key('jScansPositively', 1)

    def test_projection_centre(self):
        grid_definition_template_20(self.stereo_test_cube, self.mock_grib)
        self._check_key("projectionCentreFlag", 0)

    def test_projection_centre_south_pole(self):
        cs = Stereographic(-90.0, 0, ellipsoid=self.default_ellipsoid)
        stereo_test_cube = self._make_test_cube(cs=cs, coord_units='m')
        grid_definition_template_20(stereo_test_cube, self.mock_grib)
        self._check_key("projectionCentreFlag", 1)

    def test_projection_centre_bad(self):
        cs = Stereographic(0, 0, ellipsoid=self.default_ellipsoid)
        stereo_test_cube = self._make_test_cube(cs=cs, coord_units='m')
        exp_emsg = 'Bipolar and symmetric .* not supported.'
        with self.assertRaisesRegexp(ValueError, exp_emsg):
            grid_definition_template_20(stereo_test_cube, self.mock_grib)


if __name__ == "__main__":
    tests.main()
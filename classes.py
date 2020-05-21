from classes_dir.curve import Curve
from classes_dir.curve_polygonal import PolygonalChain
from classes_dir.curve_interpolation import PolynomialInterpolation
from classes_dir.curve_nifs3 import NIFS3
from classes_dir.curve_oifs3 import OIFS3
from classes_dir.curve_bezier import Bezier

curveTypes = {'Polygonal':PolygonalChain,'Polynomial':PolynomialInterpolation, 'NIFS3':NIFS3, 'OIFS3':OIFS3, 'Bezier':Bezier}

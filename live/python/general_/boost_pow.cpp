#include <boost/python.hpp>
#include "pow.hpp"

BOOST_PYTHON_MODULE(pypow) {
  boost::python::def("hello", snn::hello);
  boost::python::def("sum", snn::sum);
  boost::python::def("pow", snn::pow);
}
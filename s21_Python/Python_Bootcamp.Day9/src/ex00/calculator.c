#include <Python.h>

static PyObject *add(PyObject *self, PyObject *args) {
  double a, b;
  if (!PyArg_ParseTuple(args, "dd", &a, &b)) {
    return NULL;
  }
  return PyFloat_FromDouble(a + b);
}

static PyObject *sub(PyObject *self, PyObject *args) {
  double a, b;
  if (!PyArg_ParseTuple(args, "dd", &a, &b)) {
    return NULL;
  }
  return PyFloat_FromDouble(a - b);
}

static PyObject *mul(PyObject *self, PyObject *args) {
  double a, b;
  if (!PyArg_ParseTuple(args, "dd", &a, &b)) {
    return NULL;
  }
  return PyFloat_FromDouble(a * b);
}

static PyObject *divis(PyObject *self, PyObject *args) {
  double a, b;
  if (!PyArg_ParseTuple(args, "dd", &a, &b)) {
    return NULL;
  }
  if (b == 0) {
    PyErr_SetString(PyExc_TypeError, "Cannot divide by 0.");
    return NULL;
  }
  return PyFloat_FromDouble(a / b);
}

static PyMethodDef CalculatorMethods[] = {
    {"add", add, METH_VARARGS, "Add two numbers."},
    {"sub", sub, METH_VARARGS, "Subtract two numbers."},
    {"mul", mul, METH_VARARGS, "Multiply two numbers."},
    {"divis", divis, METH_VARARGS, "Divide two numbers."},
    {0, 0, 0, 0}};

static struct PyModuleDef calculatormodule = {
    PyModuleDef_HEAD_INIT, "calculator", NULL, -1, CalculatorMethods};

PyMODINIT_FUNC PyInit_calculator(void) {
  return PyModule_Create(&calculatormodule);
}
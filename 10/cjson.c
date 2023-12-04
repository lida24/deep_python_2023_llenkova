#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>

#include <Python.h>


void skip_whitespace(const char* json_str, int* i, int len) {
    while (*i < len && (json_str[*i] == ' ' || json_str[*i] == '\n'))
        (*i)++;
}

char* parse_string(const char* json_str, int* i, int len) {
//    (*i)++;
    int j = 0;
    char *str_value = (char*)malloc((len + 1) * sizeof(char));
    if (str_value == NULL)
        return NULL;
    while (*i < len && json_str[*i] != '"')
        str_value[j++] = json_str[(*i)++];
    if (*i == len || json_str[*i] != '"') {
        free(str_value);
        return NULL;
    }
    (*i)++;
    str_value[j] = '\0';
    return str_value;
}

PyObject* parse_value(const char* json_str, int* i, int len) {
    if (json_str[*i] == '"') {
        (*i)++;
        int j = 0;
        char *str_value = (char*)malloc((len + 1) * sizeof(char));
        if (str_value == NULL)
            return NULL;
        while (*i < len && json_str[*i] != '"')
            str_value[j++] = json_str[(*i)++];
        if (*i == len || json_str[*i] != '"') {
            free(str_value);
            return NULL;
        }
        (*i)++;
        str_value[j] = '\0';
        PyObject* py_str_value = Py_BuildValue("s", str_value);
        free(str_value);
        return py_str_value;
    } else if (isdigit(json_str[*i])) {
        int num = 0;
        while (*i < len && isdigit(json_str[*i])) {
            num = num * 10 + (json_str[*i] - '0');
            (*i)++;
        }
        PyObject* py_num_value = Py_BuildValue("i", num);
        return py_num_value;
    } else {
        return NULL;
    }
}

PyObject* cjson_loads(PyObject* self, PyObject* args) {
    const char *json_str;
    if (!PyArg_ParseTuple(args, "s", &json_str)) {
        PyErr_SetString(PyExc_TypeError, "Expected a string argument");
        return NULL;
    }

   int json_len = strlen(json_str);
   if (json_len == 0) {
        PyErr_SetString(PyExc_TypeError, "Empty JSON string");
        return NULL;
   }

   int i = 0;

   if (json_str[i] != '{') {
        PyErr_SetString(PyExc_TypeError, "Expected an object");
        return NULL;
   }

   i++;


    PyObject *dict = PyDict_New();
    if (dict == NULL) {
        PyErr_SetString(PyExc_RuntimeError, "Failed to create Dict Object");
        return NULL;
    }

    while (i < json_len) {
        skip_whitespace(json_str, &i, json_len);
        if (json_str[i] != '"') {
            PyErr_SetString(PyExc_TypeError, "Expected a key in double quotes");
            Py_DECREF(dict);
            return NULL;
        }

        i++;
        char* key = parse_string(json_str, &i, json_len);
        if (key == NULL) {
            PyErr_SetString(PyExc_TypeError, "Error parsing key");
            Py_DECREF(dict);
            return NULL;
        }
        skip_whitespace(json_str, &i, json_len);
        if (i == json_len || json_str[i] != ':') {
            PyErr_SetString(PyExc_TypeError, "Expected a colon after key");
            free(key);
            Py_DECREF(dict);
            return NULL;
        }
        i++;
        skip_whitespace(json_str, &i, json_len);
        PyObject* value = parse_value(json_str, &i, json_len);
        if (value == NULL) {
            PyErr_SetString(PyExc_TypeError, "Error parsing value");
            free(key);
            Py_DECREF(dict);
            return NULL;
        }
        PyObject* py_key = Py_BuildValue("s", key);
        PyDict_SetItem(dict, py_key, value);
        Py_DECREF(py_key);
        Py_DECREF(value);
        free(key);
        skip_whitespace(json_str, &i, json_len);
        if (i == json_len) {
            break;
        } else if (json_str[i] == ',') {
            i++;
        } else if (json_str[i] == '}') {
            break;
        } else if (isspace(json_str[i])) {
            i++;
        } else {
            PyErr_SetString(PyExc_TypeError, "Expected a comma or closing brace");
            Py_DECREF(dict);
            return NULL;
        }
        skip_whitespace(json_str, &i, json_len);
    }
    return dict;
}

PyObject* cjson_dumps(PyObject* self, PyObject* args) {
    PyObject* dict;
    if (!PyArg_ParseTuple(args, "O", &dict)) {
        PyErr_SetString(PyExc_TypeError, "Expected a dictionary argument");
        return NULL;
    }
    if (!PyDict_Check(dict)) {
        PyErr_SetString(PyExc_TypeError, "Expected a dictionary");
        return NULL;
    }
    Py_ssize_t pos = 0;
    PyObject* key_obj;
    PyObject* value_obj;
    PyObject* result = PyUnicode_FromString("{");
    while (PyDict_Next(dict, &pos, &key_obj, &value_obj)) {
        PyObject* key_str = PyObject_Str(key_obj);
        PyObject* value_str = PyObject_Str(value_obj);
        if (key_str != Py_None && value_str != Py_None) {
            PyObject* format_str;
            if (PyLong_Check(key_obj)) {
                format_str = PyUnicode_FromFormat("%ld: ", PyLong_AsLong(key_obj));
            } else {
                format_str = PyUnicode_FromFormat("\"%S:\": ", key_str);
            }
            result = PyUnicode_Concat(result, format_str);
            if (PyLong_Check(value_obj)) {
                PyObject* value_format_str = PyUnicode_FromFormat("%ld, ", PyLong_AsLong(value_obj));
                result = PyUnicode_Concat(result, value_format_str);
            } else {
                PyObject* value_format_str = PyUnicode_FromFormat("\"%S\": ", value_str);
                result = PyUnicode_Concat(result, value_format_str);
            }
        }
    }
    Py_ssize_t len = PyUnicode_GetLength(result);
    PyObject* new_result = PyUnicode_Substring(result, 0, len - 2);
    PyObject* format_str = PyUnicode_FromString("}");
    new_result =  PyUnicode_Concat(new_result, format_str);
    return new_result;
}

static PyMethodDef methods[] = {
    {"loads", cjson_loads, METH_VARARGS, "method can be used to parse a valid JSON string and convert it into a Python Dictionary"},
    {"dumps", cjson_dumps, METH_VARARGS, "method can be used to convert a subset of Python objects into a json string"},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef module_cjson = {
    PyModuleDef_HEAD_INIT, "cjson", NULL, -1, methods
};

PyMODINIT_FUNC PyInit_cjson()
{
    return PyModule_Create( &module_cjson );
}
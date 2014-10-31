"""
Contains a utility class to perform WCST requests from python
"""
from abc import ABCMeta, abstractmethod
import urllib as url_lib
import xml.etree.ElementTree as XMLProcessor


class WCSTRequest:
    """
    Generic class for WCST requests
    """
    __metaclass__ = ABCMeta
    REQUEST_PARAMETER = "request"

    def get_query_string(self):
        """
        Returns the query string that defines the WCST requests (the get parameters in string format)

        :return: string - containing the request information in KVP syntax
        """
        extra_params = ""
        for key, value in self._get_request_type_parameters().iteritems():
            extra_params += "&" + key + "=" + value
        return self.REQUEST_PARAMETER + "=" + self._get_request_type() + extra_params

    @abstractmethod
    def _get_request_type_parameters(self):
        """
        Returns the request specific parameters

        :return: dict - containing the needed parameters
        """
        pass

    @abstractmethod
    def _get_request_type(self):
        pass


class WCSTInsertRequest(WCSTRequest):
    """
    Class to perform WCST insert requests
    """

    def __init__(self, coverage_ref, generate_id=False):
        """
        Constructor for the class

        :param coverage_ref: string - the name of the coverage in string format
        :param generate_id: bool - true if a new id should be generated, false otherwise
        """
        self.coverage_ref = coverage_ref
        self.generate_id = generate_id

    def _get_request_type(self):
        return self.__REQUEST_TYPE

    def _get_request_type_parameters(self):
        return {
            self.__GENERATE_ID_PARAMETER: self.__GENERATE_ID_TRUE_VALUE if self.generate_id else self.__GENERATE_ID_FALSE_VALUE,
            self.__COVERAGE_REF_PARAMETER: self.coverage_ref
        }

    __GENERATE_ID_TRUE_VALUE = "new"
    __GENERATE_ID_FALSE_VALUE = "existing"
    __GENERATE_ID_PARAMETER = "useId"
    __COVERAGE_REF_PARAMETER = "coverageRef"
    __REQUEST_TYPE = "InsertCoverage"


class WCSTDeleteRequest(WCSTRequest):
    """
    Class to perform WCST delete requests
    """

    def __init__(self, coverage_ref):
        """
        Constructor for the class

        :param coverage_ref: string -  the name of the coverage in string format
        """
        self.coverage_ref = coverage_ref
        pass

    def _get_request_type(self):
        return self.__REQUEST_TYPE

    def _get_request_type_parameters(self):
        return {
            self.__COVERAGE_REF_PARAMETER: self.coverage_ref
        }

    __COVERAGE_REF_PARAMETER = "coverageRef"
    __REQUEST_TYPE = "DeleteCoverage"


class WCSTException(Exception):
    """
    Exception that is thrown when a WCST request has gone wrong
    """

    def __init__(self, exception_code, exception_text):
        self.exception_code = exception_code
        self.exception_text = exception_text

    def __str__(self):
        return "Error Code: " + self.exception_code + "\nError Text: " + self.exception_text


class WCSTExecutor():
    def __init__(self, base_url):
        """
        Constructor class

        :param base_url: string - the base url to the service that supports WCST
        """
        self.base_url = base_url

    @staticmethod
    def __check_request_for_errors(response, namespaces):
        """
        Checks if the WCST request was successful and if not raises an exception with the corresponding error code and
        error message

        :param response: string - the response from the server
        :param namespaces: dict - of namespaces to be used inside the xml parsing
        :return: does not return anything, just raises an exception if errors were detected
        """
        if response.find("ows:ExceptionReport") != -1:
            xml = XMLProcessor.fromstring(response).getRoot()
            error_code = ""
            error_text = ""
            for error in xml.findall("ows:Exception", namespaces):
                error_code = error.attrib["exceptionCode"]

            for error in xml.findall("ows:ExceptionText", namespaces):
                error_text = error.text

            raise WCSTException(error_code, error_text)

    def execute(self, request):
        """
        Executes a WCST request and returns the response to it

        :param request: WCSTRequest - the request to be executed
        :return:  string - result with the response from the WCST service
        """
        service_call = self.base_url + "?" + request.get_query_string()
        response = url_lib.urlopen(service_call).read()
        namespaces = {"ows": "http://www.opengis.net/ows/2.0"}
        self.__check_request_for_errors(response, namespaces)
        return response

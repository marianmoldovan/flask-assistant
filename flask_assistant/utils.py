from __future__ import absolute_import
from typing import Dict, Any
import os
import sys
import logging
from google.auth import jwt
from flask_assistant.core import Assistant
from . import logger


logger.setLevel(logging.INFO)

GOOGLE_PUBLIC_KEY = {
    "8a63fe71e53067524cbbc6a3a58463b3864c0787": "-----BEGIN CERTIFICATE-----\nMIIDJjCCAg6gAwIBAgIIOgLatvPIOogwDQYJKoZIhvcNAQEFBQAwNjE0MDIGA1UE\nAxMrZmVkZXJhdGVkLXNpZ25vbi5zeXN0ZW0uZ3NlcnZpY2VhY2NvdW50LmNvbTAe\nFw0xOTEwMTkxNDQ5MzRaFw0xOTExMDUwMzA0MzRaMDYxNDAyBgNVBAMTK2ZlZGVy\nYXRlZC1zaWdub24uc3lzdGVtLmdzZXJ2aWNlYWNjb3VudC5jb20wggEiMA0GCSqG\nSIb3DQEBAQUAA4IBDwAwggEKAoIBAQDJs8t86KhuRio8l/ZL3xOQ/Rh2/PJKo9IA\n1rVHDxAS1PYjGrZ+7UMU6f3yt7WqNifkdA+Vboe+f//D0maUZ36YqD9cm+8RrzVO\nb60/21OuB+UCLONtMd9f36f00WUpr/VuUngcpifW+SGbCEI+a7Jd5vuwdkEie++O\nXiVpUHdVXCKCqCt5kEXrlqh0xxWQirMH7pXL9Yp5GoBH6w1wl/yx1I285LA89D+D\nDcxDfxKJ6bFVWR+efoBaJyG4Qj3tLbrgi7OA0kXlOKmlM+POMm/6rGKxEOoya9p6\nSLU8J7wJj0QpAnEFZk7LpaVt3LWCbM54uxcRUvkiwXIsZfpOrXaZAgMBAAGjODA2\nMAwGA1UdEwEB/wQCMAAwDgYDVR0PAQH/BAQDAgeAMBYGA1UdJQEB/wQMMAoGCCsG\nAQUFBwMCMA0GCSqGSIb3DQEBBQUAA4IBAQAvsqHib9Zv36Z1u09/B1eUkrZovl9F\n8ZzzxkqNgrff9zBrtwstCPRPsz8LMaGWlDHcIqsLVe2nMbZp9ZGGCtZHoCKhiFnj\nOcNaixgGT8+wP6vn5SaNhZgu2AUNb9u6zc0IA59ggGeahSIkA17DqLqb7mIeLEj2\nTo7HTbEqjWZhl7zq01T/R7PQ5w/++InUL7HrXmwYczgJWCh6h5mU5jpYnuXRr+YI\nXEfZOaELe0HHxOfgtkY7P/f2Wb/ls0fbvYwqklxYN+jXjiopZevCoobWDlrGKZ1Z\nt114KpEaJ9RgL23tfePs32VV1NwVVnEtaWD2lijIO3AyIn+I7JHL7MDD\n-----END CERTIFICATE-----\n",
    "3db3ed6b9574ee3fcd9f149e59ff0eef4f932153": "-----BEGIN CERTIFICATE-----\nMIIDJjCCAg6gAwIBAgIIeBPD3wqfL6EwDQYJKoZIhvcNAQEFBQAwNjE0MDIGA1UE\nAxMrZmVkZXJhdGVkLXNpZ25vbi5zeXN0ZW0uZ3NlcnZpY2VhY2NvdW50LmNvbTAe\nFw0xOTEwMTExNDQ5MzRaFw0xOTEwMjgwMzA0MzRaMDYxNDAyBgNVBAMTK2ZlZGVy\nYXRlZC1zaWdub24uc3lzdGVtLmdzZXJ2aWNlYWNjb3VudC5jb20wggEiMA0GCSqG\nSIb3DQEBAQUAA4IBDwAwggEKAoIBAQDYpym/gLFOh4IoQhfOeGo+DbUyEIA/0Odf\nmzb9R1nVvM5WFHyqKiT8/yPvLxgXYzYlzyvZu18KAkYWWNuS21Vzhe+d4949P6EZ\n/096QjVFSHvKTo94bSQImeZxZiBhfFcvw/RMM0eTeZZPgOXI3YIJyWjAZ9FUslt7\nWoLU0HZFc/JyPRF8M2kinkdYxnzA+MjzCetXlqmhAr+wLPg/QLKwACyRIF2FJHgf\nPsvqaeF7JXo0zHPcGuHUOqXCHon6KiHZF7OC4bzTuTEzVipJTLYy9QUyL4M2L8bQ\nu1ISUSaXhj+i1WT0RDJwqpioOFprVFqqkVvbUW0nXD/x1UA4nvf7AgMBAAGjODA2\nMAwGA1UdEwEB/wQCMAAwDgYDVR0PAQH/BAQDAgeAMBYGA1UdJQEB/wQMMAoGCCsG\nAQUFBwMCMA0GCSqGSIb3DQEBBQUAA4IBAQBr5+4ZvfhP436NdJgN0Jn7iwwVArus\nXUn0hfuBbCoj1DhuRkP9wyLCpOo6cQS0T5bURVZzirsKc5sXP4fNYXqbfLaBpc7n\njTUtTOIqoA4LKPU7/FH6Qt/UfZ4DQIsKaD3087KdY3ePatSn/HTxvT8Ghqy/JGjf\nLXZehQnlyyCRaCMqv1gEOMiY/8LG3d1hLL7CMphnb4ASk0YMKrWkKhIoa6NWU2Rd\nqp01F4iG44ABpea+ymXAGmWBVPnep51kr/wIPIzr9WvNFAAZW2Enk3+kUWNupuz+\npdXq9KnegVsCs4G7QcTPqwc/vMu7uGq/pruDEOYVOd9Rm+rr0wlMgkcf\n-----END CERTIFICATE-----\n",
}


def import_with_3(module_name, path):
    import importlib.util

    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def import_with_2(module_name, path):
    import imp

    return imp.load_source(module_name, path)


def get_assistant(filename):
    """Imports a module from filename as a string, returns the contained Assistant object"""

    agent_name = os.path.splitext(filename)[0]

    try:
        agent_module = import_with_3(agent_name, os.path.join(os.getcwd(), filename))

    except ImportError:
        agent_module = import_with_2(agent_name, os.path.join(os.getcwd(), filename))

    for name, obj in agent_module.__dict__.items():
        if isinstance(obj, Assistant):
            return obj


def decode_token(token, client_id):
    decoded = jwt.decode(token, certs=GOOGLE_PUBLIC_KEY, verify=True, audience=client_id)
    return decoded

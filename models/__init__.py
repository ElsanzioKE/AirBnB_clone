#!/usr/bin/python3
"""This module instantentiates an object of class FileStrorage"""
from models.engine import file_storage

storage = file_storage.FileStorage()

storage.reload()

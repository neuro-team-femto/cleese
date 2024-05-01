#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
CLEESE toolbox v2.0
jan 2022, Lara Kermarec <lara.git@kermarec.bzh> for CNRS

CLEESE's engines API interface
'''

from abc import ABC, abstractmethod


class Engine(ABC):

    @staticmethod
    @abstractmethod
    def load_file(file_name):
        raise NotImplementedError()

    @staticmethod
    @abstractmethod
    def process(data, config, **kwargs):
        raise NotImplementedError()

    @staticmethod
    @abstractmethod
    def generate_stimuli(data, config, **kwargs):
        raise NotImplementedError()

    @staticmethod
    @abstractmethod
    def name():
        raise NotImplementedError()

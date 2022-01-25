#!/usr/bin/env python

from abc import ABC, abstractmethod


class Engine(ABC):

    @staticmethod
    @abstractmethod
    def load_file(filename):
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

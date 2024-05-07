from collections.abc import Iterable

import flask_login
import sirope
import random


class Note:
    def __init__(self, titulo, contenido, creador, editores):
        self._titulo = titulo
        self._contenido = contenido
        self._creador = creador
        self._editores = editores

    @property
    def titulo(self):
        return self._titulo

    @titulo.setter
    def titulo(self, titulo):
        self._titulo = titulo

    @property
    def contenido(self):
        return self._contenido

    @contenido.setter
    def contenido(self, contenido):
        self._contenido = contenido

    @property
    def creador(self):
        return self._creador

    @creador.setter
    def creador(self, creador):
        self._creador = creador

    @property
    def editores(self):
        return self._editores

    @editores.setter
    def editores(self, editores):
        self._editores = editores

    def get_id(self):
        return self.__oid__

    def get_safe_id(self, srp: sirope.Sirope):
        return srp.safe_from_oid(self.__oid__)

    @staticmethod
    def get_all_notes(srp: sirope.Sirope, user):
        notes = []
        for thisNote in srp.load_all(Note):
            if thisNote.creador == user.username:
                notes.append(thisNote)
        return notes

    @staticmethod
    def find(srp: sirope.Sirope, oid: sirope.OID) -> "Note":
        return srp.find_first(Note, lambda u: u.__oid__ == oid)

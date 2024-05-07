from collections.abc import Iterable
from typing import List

import flask_login
import sirope
import random


class Folder:
    def __init__(self, nombre: str, notas, usuarios):
        self._nombre = nombre,
        self._notas = notas
        self._usuarios = usuarios

    @property
    def nombre(self) -> str:
        if not isinstance(self._nombre, str):
            return self._nombre[0]
        else:
            return self._nombre

    @nombre.setter
    def nombre(self, nombre):
        self._nombre = nombre

    @property
    def notas(self):
        return self._notas

    @notas.setter
    def notas(self, notas):
        self._notas = notas

    @property
    def usuarios(self):
        return self._usuarios

    @usuarios.setter
    def usuarios(self, usuarios):
        self._usuarios = usuarios

    def get_id(self):
        return self.__oid__

    @staticmethod
    def find(srp: sirope.Sirope, oid: sirope.OID) -> "Folder":
        return srp.find_first(Folder, lambda u: u.__oid__ == oid)

    @staticmethod
    def get_all_folders(srp: sirope.Sirope, user):
        folders = []
        for thisFolder in srp.load_all(Folder):
            if user.username in thisFolder.usuarios:
                folders.append(thisFolder)
        return folders

    @staticmethod
    def delete_note_from_folders(srp: sirope.Sirope, noteOID):
        allFolders: Iterable[Folder] = srp.load_all(Folder)
        for thisFolder in allFolders:
            if noteOID in thisFolder.notas or str(noteOID) in thisFolder.notas:
                thisFolder.notas.remove(noteOID)
                srp.save(thisFolder)

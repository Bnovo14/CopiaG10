from uuid import UUID
from sqlmodel import Session
from fastapi import Depends, HTTPException
from . import model
from exceptions import NotFoundException
import logging




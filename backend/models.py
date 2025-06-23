from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, DECIMAL
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import List, Optional
from database import Base
import datetime


class Pays(Base):
    __tablename__ = "pays"

    id_pays: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nom_pays: Mapped[str] = mapped_column(String(100), nullable=False)
    region: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    sous_region: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    # Relations
    population_hiv: Mapped[List["PopulationHIV"]] = relationship(
        "PopulationHIV", back_populates="pays"
    )
    mortalite: Mapped[List["Mortalite"]] = relationship(
        "Mortalite", back_populates="pays"
    )
    transmission: Mapped[List["TransmissionMereEnfant"]] = relationship(
        "TransmissionMereEnfant", back_populates="pays"
    )
    traitement: Mapped[List["Traitement"]] = relationship(
        "Traitement", back_populates="pays"
    )
    statistiques: Mapped[List["Statistique"]] = relationship(
        "Statistique", back_populates="pays"
    )


class Unite(Base):
    __tablename__ = "unite"

    id_unite: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nom_unite: Mapped[str] = mapped_column(String(50), nullable=False)


class PopulationHIV(Base):
    __tablename__ = "population_hiv"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    id_pays: Mapped[int] = mapped_column(Integer, ForeignKey("pays.id_pays"))
    annee: Mapped[int] = mapped_column(Integer, nullable=False)
    valeur: Mapped[float] = mapped_column(DECIMAL(10, 2), nullable=False)
    id_unite: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("unite.id_unite"), nullable=True)

    pays: Mapped["Pays"] = relationship("Pays", back_populates="population_hiv")
    unite: Mapped["Unite"] = relationship("Unite")


class Mortalite(Base):
    __tablename__ = "mortalite"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    id_pays: Mapped[int] = mapped_column(Integer, ForeignKey("pays.id_pays"))
    annee: Mapped[int] = mapped_column(Integer, nullable=False)
    valeur: Mapped[float] = mapped_column(DECIMAL(10, 2), nullable=False)
    id_unite: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("unite.id_unite"), nullable=True)

    pays: Mapped["Pays"] = relationship("Pays", back_populates="mortalite")
    unite: Mapped["Unite"] = relationship("Unite")


class TransmissionMereEnfant(Base):
    __tablename__ = "transmission_mere_enfant"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    id_pays: Mapped[int] = mapped_column(Integer, ForeignKey("pays.id_pays"))
    valeur: Mapped[float] = mapped_column(DECIMAL(10, 2), nullable=False)
    id_unite: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("unite.id_unite"), nullable=True)

    pays: Mapped["Pays"] = relationship("Pays", back_populates="transmission")
    unite: Mapped["Unite"] = relationship("Unite")


class Traitement(Base):
    __tablename__ = "traitement"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    id_pays: Mapped[int] = mapped_column(Integer, ForeignKey("pays.id_pays"))
    valeur: Mapped[float] = mapped_column(DECIMAL(10, 2), nullable=False)
    id_unite: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("unite.id_unite"), nullable=True)
    id_type_traitement: Mapped[int] = mapped_column(
        Integer, ForeignKey("type_traitement.id_type_traitement")
    )

    pays: Mapped["Pays"] = relationship("Pays", back_populates="traitement")
    unite: Mapped["Unite"] = relationship("Unite")
    type_traitement: Mapped["TypeTraitement"] = relationship("TypeTraitement")


class Statistique(Base):
    __tablename__ = "statistique"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    id_pays: Mapped[int] = mapped_column(Integer, ForeignKey("pays.id_pays"))
    annee: Mapped[int] = mapped_column(Integer, nullable=False)
    valeur: Mapped[float] = mapped_column(DECIMAL(10, 2), nullable=False)
    id_unite: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("unite.id_unite"), nullable=True)
    id_type_statistique: Mapped[int] = mapped_column(
        Integer, ForeignKey("type_statistique.id_type_statistique")
    )

    pays: Mapped["Pays"] = relationship("Pays", back_populates="statistiques")
    unite: Mapped["Unite"] = relationship("Unite")
    type_statistique: Mapped["TypeStatistique"] = relationship("TypeStatistique")


class TypeStatistique(Base):
    __tablename__ = "type_statistique"

    id_type_statistique: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True
    )
    nom_type_statistique: Mapped[str] = mapped_column(String(100), nullable=False)


class TypeTraitement(Base):
    __tablename__ = "type_traitement"

    id_type_traitement: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True
    )
    nom_type_traitement: Mapped[str] = mapped_column(String(100), nullable=False)

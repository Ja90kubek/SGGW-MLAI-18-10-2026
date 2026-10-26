
import random
from datetime import datetime
from pathlib import Path

from sqlalchemy import (
    Boolean,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    create_engine,
    func,
    select,
    Table,
    Column,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    Session,
    mapped_column,
    relationship,
)


BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = BASE_DIR / "experiments.db"

engine = create_engine(
    f"sqlite:///{DATABASE_PATH.as_posix()}",
    echo=False,
)


class Base(DeclarativeBase):
    pass

experiment_subjects = Table(
    "experiment_subjects",
    Base.metadata,
    Column(
        "experiment_id",
        ForeignKey("experiments.id"),
        primary_key=True,
    ),
    Column(
        "subject_id",
        ForeignKey("subjects.id"),
        primary_key=True,
    ),
)

class Experiment(Base):
    __tablename__ = "experiments"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True
    )

    title: Mapped[str] = mapped_column(
        String, nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now
    )

    type: Mapped[int] = mapped_column(
        Integer, nullable=False
    )

    finished: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )

    data_points: Mapped[list["DataPoint"]] = relationship(
        back_populates="experiment"
    )

    subjects: Mapped[list["Subject"]] = relationship(
        secondary=experiment_subjects,
        back_populates="experiments",
    )


class DataPoint(Base):
    __tablename__ = "data_points"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True
    )

    real_value: Mapped[float] = mapped_column(
        Float, nullable=False
    )

    target_value: Mapped[float] = mapped_column(
        Float, nullable=False
    )

    experiment_id: Mapped[int] = mapped_column(
        ForeignKey("experiments.id"),
        nullable=False,
    )

    experiment: Mapped["Experiment"] = relationship(
        back_populates="data_points"
    )

class Subject(Base):
    __tablename__ = "subjects"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    gdpr_accepted: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    experiments: Mapped[list["Experiment"]] = relationship(
        secondary=experiment_subjects,
        back_populates="subjects",
    )


def dodaj_dane():

    with Session(engine) as session:

        experiment_1 = Experiment(
            title="Eksperyment ML 1",
            type=1,
            finished=False,
        )

        experiment_2 = Experiment(
            title="Eksperyment ML 2",
            type=2,
            finished=False,
        )

        for i in range(10):
            point = DataPoint(
                real_value=random.random(),
                target_value=random.random(),
            )
            experiment_1.data_points.append(point)

        for i in range(10):
            point = DataPoint(
                real_value=random.random(),
                target_value=random.random(),
            )
            experiment_2.data_points.append(point)

        session.add_all([experiment_1, experiment_2])
        session.commit()

        print("Dodano 2 eksperymenty i 20 punktow danych.")

def sprawdz_relacje():

    with Session(engine) as session:

        experiments = session.scalars(
            select(Experiment).order_by(Experiment.id)
        ).all()

        print("\nWERYFIKACJA RELACJI 1:N")

        for experiment in experiments:

            print(
                f"\nEksperyment: {experiment.title} "
                f"(ID: {experiment.id})"
            )

            print(
                f"Liczba punktow: {len(experiment.data_points)}"
            )

            for point in experiment.data_points:
                print(
                    f"  ID: {point.id}, "
                    f"Real: {point.real_value:.4f}, "
                    f"Target: {point.target_value:.4f}, "
                    f"Experiment ID: {point.experiment_id}"
                )

        total_points = session.scalar(
            select(func.count()).select_from(DataPoint)
        )

        print(f"\nLaczna liczba DataPoints: {total_points}")


def oblicz_agregacje():

    print("\nCWICZENIE 5: AGREGACJE")

    with Session(engine) as session:

        statement = (
            select(
                Experiment.id,
                Experiment.title,
                func.count(DataPoint.id).label("liczba_punktow"),
                func.sum(DataPoint.real_value).label("suma_real"),
                func.avg(DataPoint.real_value).label("srednia_real"),
                func.sum(DataPoint.target_value).label("suma_target"),
                func.avg(DataPoint.target_value).label("srednia_target"),
            )
            .join(DataPoint, Experiment.id == DataPoint.experiment_id)
            .group_by(Experiment.id, Experiment.title)
            .order_by(Experiment.id)
        )

        results = session.execute(statement).all()

        for row in results:

            print(
                f"\nEksperyment: {row.title} (ID: {row.id})"
            )

            print(f"Liczba punktow: {row.liczba_punktow}")

            print(f"Suma real_value: {row.suma_real:.4f}")
            print(f"Srednia real_value: {row.srednia_real:.4f}")

            print(f"Suma target_value: {row.suma_target:.4f}")
            print(f"Srednia target_value: {row.srednia_target:.4f}")

def main():

    print("SGGW - PROJEKT 2")
    print("Cwiczenie 5 - Agregacje SQLAlchemy")

    oblicz_agregacje()

if __name__ == "__main__":
    main()

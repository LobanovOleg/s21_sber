from sqlalchemy.orm import (  # type: ignore
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
)
from sqlalchemy import (  # type: ignore
    Integer,
    Float,
    String,
    Boolean,
    ARRAY,
    ForeignKeyConstraint,
    CheckConstraint,
    PrimaryKeyConstraint,
    UniqueConstraint,
)


class Base(DeclarativeBase):
    """Base class for ORM models"""

    pass


class Class(Base):
    """The table with classnames"""
    __tablename__ = "classes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String)


class Person(Base):
    """The table stores NPC data"""
    __tablename__ = "persons"

    id: Mapped[str] = mapped_column(String)
    save_id: Mapped[int] = mapped_column(Integer)
    name: Mapped[str] = mapped_column(String)
    hp: Mapped[int] = mapped_column(Integer)
    level: Mapped[int] = mapped_column(Integer)
    location_id: Mapped[int] = mapped_column(Integer)
    __pos: Mapped[list[int]] = mapped_column(ARRAY(Integer))
    class_id: Mapped[int] = mapped_column(Integer)
    is_protagonist: Mapped[bool] = mapped_column(Boolean)
    pursuit_time: Mapped[int] = mapped_column(Integer, nullable=True)
    appearance: Mapped[str] = mapped_column(String)
    weapon: Mapped[str] = mapped_column(String)
    armor: Mapped[str] = mapped_column(String)

    items: Mapped[list["Person_Item"]] = relationship(
        argument="Person_Item", back_populates="person"
    )
    buff_items: Mapped[list["Person_BuffItem"]] = relationship(
        argument="Person_BuffItem", back_populates="person"
    )
    weapons: Mapped[list["Person_Weapon"]] = relationship(
        argument="Person_Weapon", back_populates="person"
    )
    quests: Mapped[list["Person_Quest"]] = relationship(
        argument="Person_Quest", back_populates="person"
    )

    __table_args__ = (
        PrimaryKeyConstraint("id", "save_id", name="person_save"),
        ForeignKeyConstraint(["save_id"], ["saves.id"], ondelete="CASCADE"),
        ForeignKeyConstraint(["class_id"], ["classes.id"], ondelete="CASCADE"),
    )


class Item(Base):
    """The items belongs to NPCs"""
    __tablename__ = "items"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    name: Mapped[str] = mapped_column(String)
    is_tradable: Mapped[bool] = mapped_column(Boolean)
    is_usable: Mapped[bool] = mapped_column(Boolean)
    is_armor: Mapped[bool] = mapped_column(Boolean, nullable=True)
    description: Mapped[str] = mapped_column(String, nullable=True)
    buff_parameter: Mapped[int] = mapped_column(Integer, nullable=True)
    buff_reusable: Mapped[bool] = mapped_column(Boolean, nullable=True)
    buff: Mapped[int] = mapped_column(Integer, nullable=True)
    debuff: Mapped[int] = mapped_column(Integer, nullable=True)
    duration: Mapped[int] = mapped_column(Integer, nullable=True)
    cost: Mapped[int] = mapped_column(Integer, nullable=True)

    persons: Mapped[list["Person_Item"]] = relationship(
        argument="Person_Item", back_populates="item"
    )
    buffs: Mapped[list["Person_BuffItem"]] = relationship(
        argument="Person_BuffItem", back_populates="item"
    )


class Weapon(Base):
    """The weapons belongs to NPCs"""
    __tablename__ = "weapons"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    name: Mapped[str] = mapped_column(String)
    range: Mapped[int] = mapped_column(Integer, CheckConstraint("range > 0"))
    dmg_min: Mapped[int] = mapped_column(Integer)
    dmg_max: Mapped[int] = mapped_column(Integer)
    is_tradable: Mapped[bool] = mapped_column(Boolean)
    cost: Mapped[int] = mapped_column(Integer, nullable=True)

    persons: Mapped[list["Person_Weapon"]] = relationship(
        argument="Person_Weapon", back_populates="weapon"
    )


class Quest(Base):
    """The quests belongs by NPCs"""
    __tablename__ = "quests"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    brief: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)
    reward: Mapped[int] = mapped_column(Integer)
    kind: Mapped[int] = mapped_column(Integer)
    condition: Mapped[str] = mapped_column(String)
    is_done: Mapped[bool] = mapped_column(Boolean)
    start_condition: Mapped[str] = mapped_column(String, nullable=True)
    reward_item: Mapped[str] = mapped_column(String, nullable=True)
    reward_item_quantity: Mapped[int] = mapped_column(Integer, nullable=True)
    pos: Mapped[list[int]] = mapped_column(ARRAY(Integer), nullable=True)
    item: Mapped[str] = mapped_column(String, nullable=True)
    quantity: Mapped[int] = mapped_column(Integer, nullable=True)
    location_id: Mapped[int] = mapped_column(Integer, nullable=True)
    giving_npc_id: Mapped[str] = mapped_column(String, nullable=True)
    receiving_npc_id: Mapped[str] = mapped_column(String, nullable=True)
    class_id: Mapped[int] = mapped_column(Integer, nullable=True)

    persons: Mapped[list["Person_Quest"]] = relationship(
        argument="Person_Quest", back_populates="quest"
    )


class Person_Item(Base):
    """The items belongs to NPCs"""
    __tablename__ = "persons_items"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    person_id: Mapped[str] = mapped_column(String)
    save_id: Mapped[int] = mapped_column(Integer)
    item_id: Mapped[int] = mapped_column(Integer)
    quantity: Mapped[int] = mapped_column(Integer)

    person: Mapped[list["Person"]] = relationship(
        argument="Person", back_populates="items"
    )
    item: Mapped[list["Item"]] = relationship(
        argument="Item", back_populates="persons"
    )

    __table_args__ = (
        UniqueConstraint("person_id", "save_id", "item_id"),
        ForeignKeyConstraint(
            ["person_id", "save_id"],
            ["persons.id", "persons.save_id"],
            ondelete="CASCADE",
        ),
        ForeignKeyConstraint(["item_id"], ["items.id"], ondelete="CASCADE"),
    )


class Person_BuffItem(Base):
    """The items with boost effects belongs to NPCs

    Items that enhance the player and have not lost their effect time
    at the time of saving
    """

    __tablename__ = "persons_buff_items"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    person_id: Mapped[str] = mapped_column(String)
    save_id: Mapped[int] = mapped_column(Integer)
    item_id: Mapped[int] = mapped_column(Integer)
    duration: Mapped[int] = mapped_column(Integer)

    person: Mapped[list["Person"]] = relationship(
        argument="Person", back_populates="buff_items"
    )
    item: Mapped[list["Item"]] = relationship(
        argument="Item", back_populates="buffs"
    )

    __table_args__ = (
        ForeignKeyConstraint(
            ["person_id", "save_id"],
            ["persons.id", "persons.save_id"],
            ondelete="CASCADE",
        ),
        ForeignKeyConstraint(["item_id"], ["items.id"], ondelete="CASCADE"),
    )


class Person_Weapon(Base):
    """The weapons belongs to NPCs"""
    __tablename__ = "persons_weapons"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    person_id: Mapped[str] = mapped_column(String)
    save_id: Mapped[int] = mapped_column(Integer)
    weapon_id: Mapped[int] = mapped_column(Integer)

    person: Mapped[list["Person"]] = relationship(
        argument="Person", back_populates="weapons"
    )
    weapon: Mapped[list["Weapon"]] = relationship(
        argument="Weapon", back_populates="persons"
    )

    __table_args__ = (
        UniqueConstraint("person_id", "save_id", "weapon_id"),
        ForeignKeyConstraint(
            ["person_id", "save_id"],
            ["persons.id", "persons.save_id"],
            ondelete="CASCADE",
        ),
        ForeignKeyConstraint(
            ["weapon_id"], ["weapons.id"], ondelete="CASCADE"
        ),
    )


class Person_Quest(Base):
    """The persons id and belongs them quests"""
    __tablename__ = "persons_quests"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    person_id: Mapped[str] = mapped_column(String)
    save_id: Mapped[int] = mapped_column(Integer)
    quest_id: Mapped[int] = mapped_column(Integer)
    is_done: Mapped[bool] = mapped_column(Boolean)

    person: Mapped[list["Person"]] = relationship(
        argument="Person", back_populates="quests"
    )
    quest: Mapped[list["Quest"]] = relationship(
        argument="Quest", back_populates="persons"
    )

    __table_args__ = (
        UniqueConstraint("person_id", "save_id", "quest_id"),
        ForeignKeyConstraint(
            ["person_id", "save_id"],
            ["persons.id", "persons.save_id"],
            ondelete="CASCADE",
        ),
        ForeignKeyConstraint(["quest_id"], ["quests.id"], ondelete="CASCADE"),
    )


class Save(Base):
    """The game saves tables"""
    __tablename__ = "saves"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    description: Mapped[str] = mapped_column(String)
    time: Mapped[float] = mapped_column(Float)

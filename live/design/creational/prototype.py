"""
THE PROTOTYPE DESIGN
====================
The Prototype pattern allows creating
new objects by copying an existing object,
known as the prototype. In this example,
the Prototype class defines a 'clone'
method that uses the 'copy' module to
create a deep copy of the object. The
ConcretePrototype class extends Prototype
and adds a value attribute. The client code
demonstrates how prototypes can be cloned
to create independent instances."""


import copy
from typing import Any, Callable, Generic, Protocol, Self, TypeGuard, TypeVar

T = TypeVar("T")


class SupportsClonable(Protocol):
    def __clone__(self):
        ...


def _clonable_typecheck(obj: Any) -> TypeGuard[SupportsClonable]:
    return hasattr(obj, "__clone__") and callable(obj.__clone__)


def clone(obj: T) -> T:
    if _clonable_typecheck(obj):
        return obj.__clone__()
    return copy.deepcopy(obj)


class Position:
    def __init__(self, column: int = -1, row: int = -1) -> None:
        self._row = row
        self._column = column

    @property
    def row(self):
        return self._row

    @property
    def column(self):
        return self._column

    def __clone__(self):
        return Position(self.column, self.row)

    def move(self, column: int, row: int):
        self._row, self._column = row, column

    def __str__(self) -> str:
        return f"({self.column}, {self.row})"

    def __eq__(self, position: "Position") -> bool:
        return self.column == position.column and self.row == position.row

    def __hash__(self) -> int:
        col = -1 if self.column < 0 else self.column
        row = -1 if self.row < 0 else self.row
        return hash(f"{col, row}")

    __repr__ = __str__


class Cell(Generic[T]):
    def __init__(
        self, value: T | None = None, position: Position | None = None
    ) -> None:
        self.position = position or Position()
        self.value = value

    def __str__(self) -> str:
        return f"<Cell(value={self.value!r}, {self.position})>"

    def __clone__(self) -> Self:
        return self.__class__(clone(self.value), clone(self.position))

    def __hash__(self) -> int:
        return hash(self.position)

    __repr__ = __str__


class Row:
    def __init__(self, table: "Table", row_index: int = -1) -> None:
        self.row_index = row_index
        self.table = table

    def __iter__(self):
        return self.table.get_row(self.row_index)

    def __reversed__(self):
        return self.table.get_row(self.row_index, True)

    def insert(self, *cells: Cell):
        for cell in cells:
            cell.position._row = self.row_index
        self.table.insert(*cells)

    def __clone__(self):
        return self.__class__(self.table, self.row_index)


class Column(Generic[T]):
    def __init__(self, table: "Table", column_index: int = -1) -> None:
        self.column_index = column_index
        self.table = table

    def __iter__(self):
        return self.table.get_column(self.column_index)

    def insert(self, *cells: Cell):
        for cell in cells:
            cell.position._column = self.column_index
        self.table.insert(*cells)

    def __clone__(self):
        return self.__class__(self.table, self.column_index)


class Table:
    def __init__(self, *cells) -> None:
        self.cell_store = set(cells)

    def get_cell(self, position: Position, default_cell: Cell | None = None):
        for cell in self.cell_store:
            if position == cell.position:
                return cell
        if default_cell:
            default_cell.position = position
            self.insert(default_cell)
        return default_cell

    def insert(self, *cells: Cell):
        for cell in cells:
            self._insert_cell(cell)

    def _insert_cell(self, cell: Cell):
        if cell in self.cell_store:
            self.cell_store.remove(cell)
        self.cell_store.add(cell)

    def _filter_cells(
        self,
        pred: Callable[[Cell], bool],
        key: Callable[[Cell], int],
        revese: bool = False,
    ):
        return iter(sorted(filter(pred, self.cell_store), key=key, reverse=revese))

    def get_column(self, index: int, reverse: bool = False):
        _filter_col = lambda cell: cell.position.column == index
        _get_column = lambda cell: cell.position.row
        return self._filter_cells(_filter_col, _get_column, reverse)

    def get_row(self, index: int, reverse: bool = False):
        _filter_row = lambda cell: cell.position.row == index
        _get_row = lambda cell: cell.position.column
        return self._filter_cells(_filter_row, _get_row, reverse)

    def get_row_indices(self, reverse=False):
        return sorted({cell.position.row for cell in self.cell_store}, reverse=reverse)

    def get_column_indices(self, reverse=False):
        return sorted(
            {cell.position.column for cell in self.cell_store}, reverse=reverse
        )

    def iter_rows(self, reverse=False):
        for row_index in self.get_row_indices(reverse):
            yield Row(self, row_index)  # type:ignore

    def _iter(self, reverse: bool = False):
        _prepare = lambda row: reversed(row) if reverse else row
        for row in self.iter_rows(reverse):
            for cell in _prepare(row):
                yield cell

    def __iter__(self):
        return self._iter()

    def __reversed__(self):
        return self._iter(True)

    def iter_columns(self, reverse=False):
        for column_index in self.get_column_indices(reverse):
            yield Column(self, column_index)  # type:ignore

    def __clone__(self):
        return Table(clone(cell) for cell in self.cell_store)


column_heads = [
    Cell("Name", Position(0, 0)),
    Cell("Age", Position(1, 0)),
    Cell("Email", Position(2, 0)),
    Cell("Simon Nganga", Position(0, 1)),
    Cell("20", Position(1, 1)),
    Cell("simongash@gmail.com", Position(2, 1)),
    Cell("Faith Njeri", Position(0, 2)),
    Cell("10", Position(1, 2)),
    Cell("faithnjeri@gmail.com", Position(2, 2)),
]


table = Table(*column_heads)

for cell in reversed(table):
    print(cell)


"""
In this example of the prototype design pattern,
the Table object is very expensive and can be
very big containing hundreds of cells. For the Row,
Column, Cells and Position objects, they are trivial
and their very purpose is to hold some metadata
about something, eg Cells to value and position,
Row to row_index and referenced table etc.
When we clone a Row or Column object, we needn't
clone the table so the Objects come with their
own implementation of how they they should be
copied/cloned and with this, the Row objects can
prevent cloning the Table, only the row index and
give the newly cloned Row the same table as the original
one. The function clone is used to clone objects
in this application. If an object does not implement
the SupportsClonable Interface, then it is deep
copied hence creating a completely new copy with no tie to
the original.


***EACH OBJECT SPECIFIES HOW IT CAN BE CLONED***

+--------------+
|              | # The heavy object clone is the same
|              | # as the original but its cloning process
|              | # did not take as long as creating a new one.
| HEAVY OBJECT | <---------+
|              |           |
|              |           |
|              |           |
+--------------+         clone
                           | # The heavy object specifies how it is cloned.
+--------------+           |
|              | <---------+
|              |          +---------+
|              | <--------| TRIVIAL |
| HEAVY OBJECT |          +---------+
|              |          +---------+
|              | <--------| TRIVIAL |
|              |          +---------+
+--------------+              |
        ^                     |
        |                   clone
    +---------+               | # we only copy the properties of the trivial object
    | TRIVIAL | <-------------+ # and pass a reference to the heavy object to the cloned object.
    +---------+
"""
